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

### Frontend
```bash
cd frontend
pnpm install
pnpm dev
```

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

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
