# My Great ChatGPT 🤗

Streamlit + LangChain + Anthropic Claude を使用したリアルタイムチャットアプリケーション。

Claude モデルの選択、温度調整が可能で、会話履歴をセッション内で自動管理します。ストリーミング対応により、LLM からの応答がリアルタイムで表示されます。

## ✨ 機能

- **複数モデル対応** — Haiku（軽量・低コスト）と Sonnet（高性能）から選択可能
- **リアルタイムストリーミング** — Claude からの応答を Token-by-Token で受信・表示
- **会話履歴管理** — セッション状態で自動保存、「会話をクリア」で初期化可能
- **温度調整** — 0.0（決定的）～1.0（創造的）の範囲でスライダーで設定
- **簡単セットアップ** — Docker Compose で環境構築、ホットリロード対応

## 🚀 クイックスタート

### 前提条件

- Docker & Docker Compose
- Anthropic API キー（[こちら](https://console.anthropic.com/)から取得）

### セットアップ

1. リポジトリをクローン

```bash
git clone <repository-url>
cd create_streamlit_app
```

2. `.env` ファイルを作成し API キーを設定

```bash
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
```

3. Docker で実行

```bash
docker compose up --build
```

4. ブラウザで http://localhost:8501 にアクセス

## 💻 ローカル実行（Docker なし）

```bash
pip install -r requirements.txt
streamlit run src/main.py
```

その後 http://localhost:8501 にアクセス。

## 📋 使用方法

1. **サイドバー**でモデルを選択（Haiku / Sonnet）
2. **Temperature スライダー**で応答の創造性を調整
3. テキストエリアに質問を入力し「send」ボタンをクリック
4. Claude からの応答がリアルタイムに表示されます
5. 「Clear Conversation」で会話履歴をリセット

## 🏗️ アーキテクチャ

```
ユーザー入力
    ↓
Streamlit UI
    ↓
LangChain (ChatAnthropic)
    ↓
Anthropic Claude API
    ↓
ストリーミング応答 → セッション状態に保存
```

### 主要コンポーネント

- **`src/main.py`** — UI ロジック、ユーザー入力処理、LLM 統合
- **`requirements.txt`** — 依存ライブラリ（厳密なバージョン固定）
- **`docker-compose.yml`** — コンテナ設定（ホットリロード対応）
- **`.env`** — API キー等の環境変数（git に含めない）

## 📦 依存ライブラリ

- **Streamlit** — Web UI フレームワーク
- **LangChain** — LLM ラッパー・連携フレームワーク
- **Anthropic Claude** — LLM API

詳細は `requirements.txt` を参照。

## ⚙️ 設定オプション

### モデル選択

サイドバーの「Choose a model:」から選択：
- `claude-haiku-4-5` — 軽量・低コスト・高速
- `claude-sonnet-4-6` — 高性能・高精度

### Temperature

スライダーで 0.0 ～ 1.0 の範囲で設定：
- **0.0** — 決定的（同じ入力に対して同じ出力）
- **1.0** — 創造的（バリエーション豊か）

## 🐛 既知の課題

- **UI レイアウト** — 入力フォーム下にスペースが生じる場合あり（Streamlit の form 仕様）
- **初回起動時** — 依存をインストール中のため起動に時間がかかる場合あり

## 🔄 開発

### 依存の追加

新しいライブラリを追加する場合：

```bash
pip install <package-name>
pip freeze > requirements.txt
docker compose up --build
```

### ホットリロード

Docker Compose では、ホスト側でファイルを編集するとコンテナ内で自動的にリロードされます。

## 📝 ライセンス

MIT License

## 🤝 貢献

バグ報告・機能リクエストは [Issues](https://github.com/yourusername/repo/issues) から。
Pull Request も歓迎です。

## 📞 サポート

問題が発生した場合は [GitHub Issues](https://github.com/yourusername/repo/issues) で報告してください。

---

**Created with Claude Code** ✨
