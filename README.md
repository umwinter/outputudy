# Outputudy

"Outputudy" (Output + Study) をテーマにした、学習特化型ブログプラットフォーム。

## コンセプト
新しい技術や知識を学ぶ際、公式ドキュメントや教材は膨大で難解なことが多く、初学者が「どこをどう読んで、何を理解したのか」を整理するのは困難です。また、他の学習者がどのようなプロセスで学んだかも可視化されていません。

**Outputudy** は、日々の学習における「気づき」や「学んだこと」を逐一投稿（アウトプット）しながら学習を進めるためのサービスです。インプットとアウトプットをセットにすることで、より深い定着を目指します。

## 主な機能（構想）
- **学習ログの投稿**: 学んだ内容をリアルタイムで記録・公開。
- **リソース連携**: 学習に使用したWebサイトやドキュメントのURLを紐付け。
- **AI サポート**:
    - **自動要約**: 紐付けられた参考サイトの内容をAIが要約。
    - **学習レビュー**: ユーザーの投稿内容と参考サイトを照らし合わせ、解釈に誤りがないかAIがレビュー・フィードバック。

## ディレクトリ構成

- **[frontend](./frontend)**: Next.js + shadcn/ui アプリケーション
- **[backend](./backend)**: FastAPI アプリケーション
- **[doc](./doc)**: プロジェクトドキュメント
    - [Context](./doc/src/context.md)
- **docker-compose.yml**: インフラ構成

## セットアップ

### クイックスタート (推奨)

プロジェクトのルートディレクトリで以下のコマンドを実行してください。環境変数の設定、Docker コンテナの起動、データベースの初期化、Git Hooks のインストールを自動で行います。

```bash
make setup
```

または直接スクリプトを実行することも可能です：

```bash
./scripts/setup.sh
```

### 開発用コマンド (Makefile)

日常的な操作には `Makefile` のコマンドを利用できます：

| コマンド | 内容 |
| :--- | :--- |
| `make dev` | Docker コンテナを起動します (バックグラウンド) |
| `make stop` | Docker コンテナを停止します |
| `make ps` | コンテナのステータスを確認します |
| `make logs` | コンテナのログを表示します |
| `make lint` | バックエンド/フロントエンドの Lint チェックを実行します |
| `make format` | コードの自動フォーマットを実行します |
| `make type-check` | 静的型チェックを実行します |

---

### 個別セットアップ (開発者向け)

### Documentation
ドキュメントサーバーは `http://localhost:8001` で起動します。

- **URL**: [http://localhost:8001](http://localhost:8001)
- **機能**: Project Docs + API Reference (Swagger UI & ReDoc)
- **OpenAPI Update**:
  Backend の変更をドキュメントに反映するには、以下のコマンドで定義ファイル (`doc/src/openapi.json`) を更新してください。
  ```bash
  docker-compose run --rm --entrypoint "" document python /docs/scripts/generate_static.py
  ```

> [!NOTE] Specification
> 開発環境 (`docker-compose up`) では `mkdocs serve` が動作しており、ドキュメントのビルドはメモリ上で行われます。
> そのため、`doc/site` ディレクトリにはファイルが出力されません。
> 静的ファイルとして出力したい場合（デプロイ用など）は、明示的にビルドを実行してください：
> `docker-compose run --rm document mkdocs build`
