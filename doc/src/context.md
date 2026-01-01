# プロジェクト概要
**Outputudy** (Output + Study) は、学習特化型のブログプラットフォームです。
ユーザーが日々の学習内容（インプット）をアウトプットとして記録し、定着を促すことを目的としています。

## Tech Stack

### Frontend
- **Framework**: [Next.js](https://nextjs.org/) (App Router)
- **UI**: [Tailwind CSS v4](https://tailwindcss.com/) + [shadcn/ui](https://ui.shadcn.com/)
- **Icons**: Lucide React
- **Language**: TypeScript

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Language**: Python 3.12
- **Database**: PostgreSQL (via SQLAlchemy / Alembic)

### Infrastructure
- **Containerization**: Docker / Docker Compose
- **Tools**: Adminer (DB GUI), Mailpit (Email testing)

### Documentation
- **Tool**: [MkDocs](https://www.mkdocs.org/) (Material Theme)
- **API Spec**: OpenAPI (Swagger UI / ReDoc)

## Architecture
```mermaid
graph TD
    User[User] -->|Browser| Frontend[Frontend (Next.js)]
    User -->|Browser| Doc[Documentation (MkDocs)]
    Frontend -->|API Request| Backend[Backend (FastAPI)]
    Backend -->|Read/Write| DB[(PostgreSQL)]
    Backend -->|SMTP| Mailpit[Mailpit]
    Doc -->|Fetch openapi.json| Backend
```

## Key Decisions (ADR)

### 1. API Documentation Flow
- **Decision**: Backend から `openapi.json` を生成・取得し、MkDocs 内で [Swagger UI](http://localhost:8001/api) と [ReDoc](http://localhost:8001/api_redoc) を表示する。
- **Reasoning**:
  - ドキュメントと API 仕様を 1 箇所 (MkDocs) に集約するため。
  - `mkdocs-swagger-ui-tag` と `mkdocs-redoc-tag` プラグインを使用し、簡易に埋め込みを実現。
- **Note**: `doc/src/openapi.json` は `scripts/generate_static.py` を実行して Backend から取得・更新する運用。

### 2. Frontend Framework & Components
- **Decision**: Next.js + Tailwind CSS v4 + shadcn/ui を採用。
- **Reasoning**:
  - モダンで開発効率が高い構成のため。
  - shadcn/ui はコードベースにコンポーネント実体を持つため、カスタマイズが容易で、かつ AI (LLM) との親和性も高い（実コードを参照できるため）。
- **Note**: 色や基本スタイルは `globals.css` の CSS Variables で管理。Shadcn UI はこれを参照する。

### 3. Docker Volume & Dependencies
- **Issue**: `docker-compose.yml` で `node_modules` をボリュームマウントしているため、`Dockerfile` で `npm install` してもホスト側の古い依存関係が優先されてしまう。
- **Solution**: 依存関係を変更した際は、コンテナ内で `pnpm install` を実行するか、ボリュームを再作成 (`down -v`) する必要がある。
