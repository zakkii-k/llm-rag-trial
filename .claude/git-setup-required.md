# Git リモートアクセス設定手順

このコンテナには SSH 鍵が存在しないため、GitHub へのプッシュができません。
以下のいずれかの方法で設定してください。

---

## 方法A: SSH 鍵を生成して GitHub に登録する（推奨）

```bash
# 1. SSH 鍵を生成
ssh-keygen -t ed25519 -C "your_email@example.com"
# → ~/.ssh/id_ed25519 と ~/.ssh/id_ed25519.pub が生成される

# 2. 公開鍵を表示してコピー
cat ~/.ssh/id_ed25519.pub

# 3. GitHub に登録
#    https://github.com/settings/keys → "New SSH key" → 貼り付け

# 4. 接続確認
ssh -T git@github.com
# → "Hi zakkii-k! You've successfully authenticated..." と表示されれば成功

# 5. リポジトリ初期化とリモート設定（/app で実行）
cd /app
git init
git remote add origin git@github.com:zakkii-k/llm-rag-trial.git
git branch -M main
```

---

## 方法B: HTTPS + Personal Access Token を使う

```bash
# 1. GitHub でトークンを発行
#    https://github.com/settings/tokens → "Generate new token (classic)"
#    スコープ: repo にチェック

# 2. リポジトリ初期化とリモート設定（/app で実行）
cd /app
git init
git remote add origin https://<YOUR_TOKEN>@github.com/zakkii-k/llm-rag-trial.git
git branch -M main
```

---

## 設定完了後の初回プッシュ

```bash
cd /app
git add .
git commit -m "feat: initial project setup"
git push -u origin main
```

---

設定が完了したら、その後の push は Claude Code が自動で行います。
