# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## このプロジェクトについて

Streamlit + LangChain + Anthropic Claude を使用したチャットアプリ。会話履歴をセッション状態で管理し、モデル選択（Haiku/Sonnet）と temperature 調整が可能。ストリーミング対応で、LLM からの応答がリアルタイムで表示される。

`.env` に `ANTHROPIC_API_KEY` が設定されていることが前提。LangChain を通じて Claude API と統合している。

## コマンド

### Docker での実行（推奨）

`env_file` で `.env` が読み込まれ、プロジェクトディレクトリが `/app` にバインドマウントされるため、ホスト側での編集がコンテナ内でホットリロードされる：

```bash
docker compose up --build     # 初回またはrequirements.txt変更後（イメージを再構築）
docker compose up             # 2回目以降（既存イメージを使用）
docker compose down           # コンテナを停止・削除
```

アプリは http://localhost:8501 にアクセス可能。

### ホスト側での直接実行

```bash
pip install -r requirements.txt
streamlit run src/main.py
```

その後 http://localhost:8501 にアクセス。

### 依存のアップデート

```bash
pip freeze > requirements.txt  # 現在の環境をスナップショット化（バージョン未指定の修正時に使用）
```

## Docker の注意点

`Dockerfile` の `WORKDIR` は `/app` で、`COPY . .` によりプロジェクトルートの中身が `/app` 直下に展開される（`/app/app` ではない）。したがって `CMD` のスクリプトパスはプロジェクトルートからの相対パス、つまり `src/main.py` と書く。`/src/main.py` や `app/src/main.py` と書くと解決できず `File does not exist` で起動に失敗する。

## アーキテクチャ

### 全体フロー

```
ユーザー入力 → Streamlit UI → LangChain → Claude API (Anthropic)
      ↑                                          ↓
      ←━━━━ Session State で会話履歴を保持 ←━━━
```

**単一ファイル構成** (`src/main.py`):
- UI レイアウト、ユーザー入力処理、LLM 呼び出し、応答表示が1つのファイルに集約されている
- 将来的な拡張の際は、LLM ロジックや UI 要素をモジュール化することを検討

### 状態管理

`st.session_state` を使用してスクリーン再描画間で状態を保持:
- `messages`: LangChain の `SystemMessage`/`HumanMessage`/`AIMessage` のリスト。会話履歴として機能し、モデルへの context となる
- `costs`: 将来的な使用量追跡用（現在は未使用）

セッションがクリアされるか "Clear Conversation" ボタンが押されると、初期 `SystemMessage` のみの状態にリセット。

### LLM インテグレーション

**モデル初期化**:
- `ChatAnthropic` (from `langchain_anthropic`) で Claude モデルをインスタンス化
- モデル選択: `claude-haiku-4-5`（低コスト、軽量）と `claude-sonnet-4-6`（高性能）から選択可能
- `temperature` はスライダーで動的に設定（0.0 = 決定的、1.0 = 創造的）

**ストリーミング応答**:
- `model.stream(messages)` で Claude からの応答を Token-by-Token で取得
- Streamlit の `st.write_stream()` で受信と同時にリアルタイム表示
- Callback ハンドラは現在コメントアウト（`StreamlitCallbackHandler` の version 互換性問題）

**プロンプト**:
- `SystemMessage(content="You are a helpful assistant.")` で AI のキャラクターを定義
- ユーザー入力は `HumanMessage`、LLM 応答は `AIMessage` でラッピングして history に追加

### UI 構成

**レイアウト**: 
- メイン領域：会話表示（過去メッセージと新規入力フォーム）
- サイドバー：設定パネル

**サイドバー要素**:
- モデル選択ラジオボタン（Haiku/Sonnet）
- Temperature スライダー（0.0～1.0、刻み 0.01）
- "Clear Conversation" ボタン

## 規約

- `requirements.txt` の依存は推移的依存も含めて全て厳密なバージョン固定になっており、`pip freeze` のスナップショットのような形になっている。**現在、`langchain-anthropic` と `langchain-community` がバージョン未指定になっており、修正が必要**。再生成・追記する際もこのスタイルを維持すること。
- 設定ファイル内のコメントは日本語で書かれている（`docker-compose.yml` を参照）。ユーザーは日本語で作業している。
- `.env` は gitignore されておらず、このディレクトリは git リポジトリではない。git を初期化する場合は、まず `.env` を除外すること。

## 既知の課題・注意点

- **LangChain バージョン互換性**: `langchain-anthropic` と `langchain-core` のバージョン指定には注意。依存グラフが複雑で、不適切なバージョン組み合わせでインストール失敗または実行時エラーが発生する可能性がある（例：`langchain-anthropic==0.3.0` は `langchain-core<0.4.0` に依存し、1.6.1 と互換しない）
- **StreamlitCallbackHandler**: import パスは `langchain_community.callbacks.streamlit` を使用。古いパス `langchain.callback` は非推奨
- **UI レイアウト**: 入力フォーム（form）と以前の出力の間にスペースが生じる既知の課題。Streamlit の form 仕様による制限（コード内のコメント参照）
- **未実装**: テストスイート、Linter 設定、CI/CD パイプライン。将来追加される可能性あり

## 開発上の注意

### 依存管理

`requirements.txt` は `pip freeze` スタイルで厳密なバージョン固定。新しい依存を追加する際:
1. ホスト環境で `pip install <package>` してテスト
2. 互換性問題がないことを確認してから `pip freeze > requirements.txt`
3. または Docker コンテナ内で確認後、出力をコピーして requirements.txt に追加

LangChain 周辺は特に互換性が複雑なため、major バージョン変更時は慎重に。

### コード スタイル

- ファイル内のコメントは日本語で統一（ユーザーが日本語で作業しているため）
- `src/main.py` は単一モジュール。機能が増える場合は適切に分割を検討

### 環境変数

- `.env` に `ANTHROPIC_API_KEY` が必須。Docker Compose の `env_file` で読み込まれる
- git リポジトリ化時は `.env` を `.gitignore` に追加すること（現在は非 git リポジトリ）
