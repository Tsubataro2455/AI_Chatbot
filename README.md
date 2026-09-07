# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## このプロジェクトについて

Streamlit + LangChain + Anthropic Claude を使用したチャットアプリ。会話履歴をセッション状態で管理し、モデル選択（Haiku/Sonnet）と temperature 調整が可能。ストリーミング対応で、LLM からの応答がリアルタイムで表示される。

`.env` に `ANTHROPIC_API_KEY` が設定されていることが前提。LangChain を通じて Claude API と統合している。

## コマンド

Docker Compose が想定された開発手順（`env_file` で `.env` が読み込まれ、プロジェクトディレクトリが `/app` にバインドマウントされるため編集がホットリロードされる）:

```bash
docker compose up --build     # 初回 / requirements.txt 変更後
docker compose up             # 2回目以降
```

アプリは http://localhost:8501 で起動する。

ホスト側で直接動かす場合:

```bash
pip install -r requirements.txt
streamlit run src/main.py
```

## Docker の注意点

`Dockerfile` の `WORKDIR` は `/app` で、`COPY . .` によりプロジェクトルートの中身が `/app` 直下に展開される（`/app/app` ではない）。したがって `CMD` のスクリプトパスはプロジェクトルートからの相対パス、つまり `src/main.py` と書く。`/src/main.py` や `app/src/main.py` と書くと解決できず `File does not exist` で起動に失敗する。

## アーキテクチャ

### 状態管理

`st.session_state` を使用して以下を保持:
- `messages`: LangChain の `SystemMessage`/`HumanMessage`/`AIMessage` のリスト。会話履歴として機能
- `costs`: 将来的な使用量追跡用（現在は未使用）

### LLM インテグレーション

- `ChatAnthropic` (from `langchain_anthropic`) で Claude モデルを初期化
- ストリーミング対応: `model.stream()` で応答をリアルタイム取得し、`st.write_stream()` で表示
- `SystemMessage` で AI のふるまいを定義（プロンプトテンプレート）
- モデル選択: `claude-haiku-4-5`（軽量）と `claude-sonnet-4-6`（高性能）から選択可能

### サイドバー UI

- モデル選択ラジオボタン
- Temperature スライダー（0.0～1.0、精度重視～創造性重視）
- 会話クリアボタン

## 規約

- `requirements.txt` の依存は推移的依存も含めて全て厳密なバージョン固定になっており、`pip freeze` のスナップショットのような形になっている。**現在、`langchain-anthropic` と `langchain-community` がバージョン未指定になっており、修正が必要**。再生成・追記する際もこのスタイルを維持すること。
- 設定ファイル内のコメントは日本語で書かれている（`docker-compose.yml` を参照）。ユーザーは日本語で作業している。
- `.env` は gitignore されておらず、このディレクトリは git リポジトリではない。git を初期化する場合は、まず `.env` を除外すること。

## 既知の課題・注意点

- **LangChain バージョン互換性**: `langchain-anthropic` と `langchain-core` のバージョン指定には注意。依存グラフが複雑で、不適切なバージョン組み合わせでインストール失敗または実行時エラーが発生する可能性がある
- **StreamlitCallbackHandler**: import パスは `langchain_community.callbacks.streamlit` を使用。`langchain.callback` は古いパス
- **UI レイアウト**: 入力フォーム（form）と以前の出力の間にスペースが生じる既知の課題がある（コード内の改善点コメント参照）
