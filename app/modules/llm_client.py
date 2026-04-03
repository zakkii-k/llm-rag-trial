"""
llm_client.py — Ollama / Gemini API 統一 LLM クライアント

model_name が "gemini-" で始まる場合は Google AI Studio API を使用。
それ以外は Ollama を使用。
"""

import os
import time
from dataclasses import dataclass

import requests

from app.modules.env_utils import get_ollama_url


@dataclass
class GenerateResult:
    text: str
    prompt_tokens: int
    completion_tokens: int


# ── Gemini 無料枠レート制限 ────────────────────────────────────────────────────
# https://ai.google.dev/gemini-api/docs/models
GEMINI_LIMITS: dict[str, dict] = {
    "gemini-1.5-flash": {"rpm": 15,  "rpd": 1_500, "tpm": 1_000_000},
    "gemini-1.5-pro":   {"rpm": 2,   "rpd": 50,    "tpm":    32_000},
    "gemini-2.0-flash": {"rpm": 15,  "rpd": 1_500, "tpm": 1_000_000},
}


class GeminiQuotaTracker:
    """セッション内の Gemini API 使用量を追跡し、残余上限を stdout に表示する"""

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.limits = GEMINI_LIMITS.get(model_name, {"rpm": "?", "rpd": "?", "tpm": "?"})
        self.session_requests = 0
        self.session_tokens_in = 0
        self.session_tokens_out = 0
        self._minute_timestamps: list[float] = []

    def record(self, prompt_tokens: int, completion_tokens: int) -> None:
        now = time.time()
        self.session_requests += 1
        self.session_tokens_in += prompt_tokens
        self.session_tokens_out += completion_tokens
        self._minute_timestamps.append(now)
        # 1分以上前のエントリを除去
        self._minute_timestamps = [t for t in self._minute_timestamps if now - t < 60]

    def print_status(self) -> None:
        rpm_limit = self.limits["rpm"]
        rpd_limit = self.limits["rpd"]
        tpm_limit = self.limits["tpm"]

        current_rpm = len(self._minute_timestamps)
        used_tokens  = self.session_tokens_in + self.session_tokens_out

        rpm_rem = (rpm_limit - current_rpm) if isinstance(rpm_limit, int) else "?"
        rpd_rem = (rpd_limit - self.session_requests) if isinstance(rpd_limit, int) else "?"
        tpm_rem = (tpm_limit - used_tokens) if isinstance(tpm_limit, int) else "?"  # 概算

        tpm_rem_str = f"{tpm_rem:,}" if isinstance(tpm_rem, int) else tpm_rem
        tpm_lim_str = f"{tpm_limit:,}" if isinstance(tpm_limit, int) else tpm_limit

        print(
            f"  [Gemini quota] "
            f"RPM残り: {rpm_rem}/{rpm_limit}  "
            f"RPD残り: {rpd_rem}/{rpd_limit}  "
            f"TPM残り(概算): {tpm_rem_str}/{tpm_lim_str}"
        )


class LLMClient:
    """Ollama / Gemini を統一インターフェースで扱う LLM クライアント"""

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.is_gemini = model_name.startswith("gemini-")

        if self.is_gemini:
            import google.generativeai as genai
            api_key = os.getenv("GOOGLE_API_KEY", "")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY 環境変数が設定されていません")
            genai.configure(api_key=api_key)
            self._genai = genai.GenerativeModel(model_name)
        else:
            self._ollama_url = get_ollama_url()

    def invoke(self, prompt: str) -> str:
        """プロンプトを渡して回答テキストを返す"""
        return self.generate(prompt).text

    def generate(self, prompt: str) -> GenerateResult:
        """回答テキストとトークン数を返す"""
        if self.is_gemini:
            response = self._genai.generate_content(prompt)
            usage = response.usage_metadata
            return GenerateResult(
                text=response.text,
                prompt_tokens=usage.prompt_token_count,
                completion_tokens=usage.candidates_token_count,
            )
        else:
            from langchain_ollama import OllamaLLM
            llm = OllamaLLM(model=self.model_name, base_url=self._ollama_url)
            text = llm.invoke(prompt)
            pt, ct = _ollama_token_counts(self._ollama_url, self.model_name, prompt, text)
            return GenerateResult(text=text, prompt_tokens=pt, completion_tokens=ct)


def validate_gemini_api_key(model_name: str) -> tuple[bool, str]:
    """
    Gemini API キーの有効性を確認する。
    Returns: (is_valid, error_message)
    """
    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        return False, "GOOGLE_API_KEY が .env に設定されていません"
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        resp = model.generate_content("Hi")
        _ = resp.text  # アクセスしてエラーを早期検出
        return True, ""
    except Exception as e:
        return False, str(e)


def _ollama_token_counts(base_url: str, model: str, prompt: str, response: str):
    try:
        resp = requests.post(
            f"{base_url}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False,
                  "options": {"num_predict": 1}},
            timeout=60,
        )
        data = resp.json()
        return data.get("prompt_eval_count", 0), data.get("eval_count", 0)
    except Exception:
        return max(1, int(len(prompt) * 0.6)), max(1, int(len(response) * 0.6))
