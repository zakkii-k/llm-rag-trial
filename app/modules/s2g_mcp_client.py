"""
s2g_mcp_client.py – source2graph MCP クライアント

source2graph MCP サーバーに接続し、ツール一覧取得・呼び出しを行う。
Ollama のツール呼び出し（function calling）フォーマットに変換して返す。

使用例:
    async with S2GClient("/path/to/repo") as s2g:
        tools = s2g.get_ollama_tools()
        result = await s2g.call_tool("query_nodes", {"label": "Class"})
"""

import json
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# source2graph CLI のデフォルトパス（Docker 内 /app/source2graph/）
DEFAULT_S2G_CLI = "/app/source2graph/dist/cli/index.js"


class S2GClient:
    """source2graph MCP サーバーへの非同期クライアント"""

    def __init__(self, repo_path: str, s2g_cli: str = DEFAULT_S2G_CLI):
        self.repo_path = repo_path
        self.s2g_cli = s2g_cli
        self._session: ClientSession | None = None
        self._tools: list = []
        self._cm = None
        self._session_cm = None

    async def __aenter__(self) -> "S2GClient":
        server_params = StdioServerParameters(
            command="node",
            args=[self.s2g_cli, "serve", "--repo", self.repo_path],
        )
        self._cm = stdio_client(server_params)
        read, write = await self._cm.__aenter__()
        self._session_cm = ClientSession(read, write)
        self._session = await self._session_cm.__aenter__()
        await self._session.initialize()
        result = await self._session.list_tools()
        self._tools = result.tools
        return self

    async def __aexit__(self, *args: Any) -> None:
        if self._session_cm:
            await self._session_cm.__aexit__(*args)
        if self._cm:
            await self._cm.__aexit__(*args)

    # ── ツール操作 ────────────────────────────────────────────────

    def get_ollama_tools(self) -> list[dict]:
        """Ollama / OpenAI フォーマットのツール定義リストを返す"""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.inputSchema or {
                        "type": "object",
                        "properties": {},
                    },
                },
            }
            for tool in self._tools
        ]

    async def call_tool(self, name: str, arguments: dict) -> str:
        """ツールを呼び出して結果を文字列で返す"""
        assert self._session, "セッションが初期化されていません"
        result = await self._session.call_tool(name, arguments)
        if result.content:
            return "\n".join(
                c.text if hasattr(c, "text") else json.dumps(c, ensure_ascii=False)
                for c in result.content
            )
        return "(結果なし)"

    @property
    def tool_names(self) -> list[str]:
        return [t.name for t in self._tools]
