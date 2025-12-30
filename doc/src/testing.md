# Testing in Outputudy

Outputudy では、品質担保のためにバックエンドおよびフロントエンドでテストを自動実行しています。

## Backend Testing

バックエンド（FastAPI）では `pytest` を使用したテストスイートを構築しています。

### テスト構成

1.  **Unit Tests (`tests/unit/`)**:
    *   単一の関数やクラス（Service, Security 等）のロジックを確認します。
    *   外部依存関係（DB, 外部ライブラリ）は可能な限り Mock を使用します。
2.  **Functional Tests (`tests/functional/`)**:
    *   API エンドポイント（Router）に対して実際にリクエストを投げ、レスポンスを確認します。
    *   OAuth2 (JWT) による認証・認可フローも含めて検証します。
    *   テスト用の SQLite データベースを使用し、DB との連携を含めた挙動を確認します。

### 並列実行の仕組み

テストの実行時間を短縮するため、`pytest-xdist` を使用して並列実行を可能にしています。

*   **データベースの並列化**: 各ワーカープロセス（`gw0`, `gw1` 等）ごとに個別の SQLite データベースファイル（`test_gw0.db` 等）を作成することで、テストデータの干渉を完全に防いでいます。
*   **設定**: `tests/conftest.py` がワーカー ID を検知し、適切な接続先を自動的に振り分けます。

### テストの実行方法

プロジェクトルートで以下のコマンドを実行してください：

```bash
# Docker 内で並列テストを実行 (推奨)
make test

# 手動で実行する場合
docker-compose exec backend pytest -n auto
```

## Frontend Testing

フロントエンド（Next.js）では `Vitest` と `React Testing Library` を使用しています。

### テスト構成

1.  **Unit Tests**:
    *   ユーティリティ関数やバリデーションロジック、カスタムフック等を検証します。
2.  **Component Tests**:
    *   React Testing Library を使用し、UI コンポーネントがユーザーの操作（入力、クリック等）に対して正しく振る舞うかを確認します。
    *   `src/test/setup.ts` にて `jest-dom` の拡張マッチャーを導入しており、直感的なアサーションが可能です。

### 設定ファイル
*   **`vitest.config.ts`**: `jsdom` 環境、パスエイリアス（`@/`）、セットアップファイルの指定を行っています。

### テストの実行方法

```bash
# プロジェクト全体 (Backend と同時)
make test

# フロントエンドのみ
docker-compose exec frontend pnpm test
```
