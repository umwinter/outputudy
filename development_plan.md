# Outputudy 開発計画（案）

## 1. プロジェクト概要

*   **プロダクト名**: Outputudy (Output + Study)
*   **コンセプト**: 学習特化型ブログプラットフォーム。インプット（学習）とアウトプット（記録）を統合し、AIによるサポートで定着を図る。
*   **技術スタック**:
    *   Frontend: Next.js (App Router), TypeScript, Tailwind CSS v4, shadcn/ui
    *   Backend: FastAPI, Python 3.12, PostgreSQL (Async), SQLAlchemy
    *   Infra: Docker Compose

## 2. 現状確認 (Current Status)

*   **実装済み/進行中**:
    *   プロジェクト基盤構築（Docker, Makefile, CI）
    *   認証機能（Signup, Login, Password Reset）- `auth_router`, `user_router`
    *   API ドキュメント基盤 (MkDocs + Swagger UI)
*   **未実装**:
    *   学習ログ（Post）の投稿・閲覧・編集・削除機能
    *   リソース（URL）の紐付け管理
    *   AI連携機能（要約・レビュー）
    *   UI/UX の洗練（ホーム画面、ダッシュボード等）

## 3. 開発ロードマップ

### Phase 0: Initial Deployment (最優先)
まずは現状のアプリケーション (Auth機能のみ) を本番環境 (GCP) にデプロイし、CI/CD パイプラインを確立します。これにより、以降の開発は即座に本番反映される状態を作ります。

#### Phase 0.1: GCP 基盤構築 (IaC)
*   [ ] **Infrastructure**: Terraform で以下の構成をコード化
    *   Cloud Run (Frontend / Backend)
    *   Cloud SQL (PostgreSQL)
    *   Cloud Storage (User Content)
    *   Secret Manager
*   [ ] **Network**: 独自ドメイン設定 (Optional), SSL 化

#### Phase 0.2: CI/CD & Production Release
*   [ ] **Container**: `Dockerfile` の本番最適化 (Multi-stage build)
*   [ ] **CI/CD**: GitHub- [x] Application CI/CD Workflow (`deploy.yml`)
    - [x] Build & Deploy Automation
    - [ ] **Refactor Docker for Production (Multi-stage)** <!-- Issue #8 -->
        - [ ] Frontend: Builder vs Runner stages
        - [ ] Backend: Prod vs Dev configurations
        - [ ] Update `docker-compose.yml` to target dev stages
    *   Build & Push to Artifact Registry
    *   Deploy to Cloud Run
*   [ ] **Verification**: 本番環境での Signup/Login 動作確認

### Phase 1: Core MVP (個人学習ログ機能)
デプロイ基盤が整った上で、コア機能を実装・リリースしていきます。

#### Phase 1.1: データ基盤 & API 実装
*   [ ] **Database**: `posts`, `resources` テーブル作成
*   [ ] **API**: Post CRUD, Resource 紐付け API の実装
*   [ ] **Backend Test**: 基本的な Unit/Functional Test の追加

#### Phase 1.2: フロントエンド実装 (Basic UI)
*   [ ] **Markdown Editor**: 記事作成・編集 UI (Shimditor or equivalents)
*   [ ] **Post Viewer**: 記事詳細表示, 記事一覧 (Pagination)
*   [ ] **Resource Preview**: OGP 展開表示

### Phase 2: 認可制御 (Public Alpha)
「誰が何をできるか」を制御し、安全に公開できる状態にします。

#### Phase 2.1: ソーシャル認証 (Google Login)
認可の設定を行う前に、ユーザー登録のハードルを下げるための Google ログインを導入します。

*   [ ] **OAuth2**: Google OAuth プロバイダの設定
*   [ ] **Frontend**: NextAuth.js (Auth.js) Google Provider 設定
*   [ ] **Backend**: ID Token 検証 & ユーザー作成ロジックの実装

#### Phase 2.2: 認可システム (RBAC)
*   [ ] **Database**: User Role (`admin` / `user`) の定義
*   [ ] **Authorization**:
    *   他人の記事を編集・削除できない制御
    *   管理者権限の実装

### Phase 3: 管理機能 & 運用安定化
サービスの健全な運営を維持するための機能セットです。

#### Phase 3.1: 管理者ダッシュボード
*   [ ] **User Management**: ユーザー一覧, Ban/Activate 機能
*   [ ] **Content Moderation**: 全投稿の閲覧・強制削除機能
*   [ ] **SQL Client**: 本番 DB で SQL を実行できる簡易クライアント機能 (開発者用)
*   [ ] **System Status**: 簡易的なシステムメトリクス表示

#### Phase 3.2: 運用監視 (Observability)
*   [ ] **Logging**: Cloud Logging への構造化ログ出力設定
*   [ ] **Monitoring**: エラー通知 (Sentry or Cloud Monitoring)

### Phase 4: AI 機能統合
Outputudy の独自性（差別化要素）を実装します。

#### Phase 4.1: 自動要約システム
*   [ ] **Scraper**: URL からのコンテンツ抽出機能
*   [ ] **AI Integration**: OpenAI/Gemini API による要約生成
*   [ ] **UI Integration**: 投稿画面での「自動要約」ボタン実装

#### Phase 4.2: AI 学習詳細レビュー
*   [ ] **Review Engine**: 記事内容と参考元の比較ロジック
*   [ ] **Feedback UI**: AI からの改善提案表示 UI

### Phase 5: ソーシャル & 通知機能
学習の継続率を高めるためのコミュニティ機能と、アクティビティを伝える通知基盤を構築します。

*   [ ] **Profile & Stats**: 学習ヒートマップ (GitHub Like)
*   [ ] **Social**: いいね (LGTM), コメント, フォロー機能
*   [ ] **Notifications**: 通知センター (In-app) & メール通知 (SendGrid / Mailgun)

### Phase 6: ゲーミフィケーション (継続の仕組み)
「楽しさ」を取り入れ、ユーザーのモチベーションを維持します。

*   [ ] **XP & Leveling**: 投稿やアクションに応じた経験値システム
*   [ ] **Streaks**: 連続投稿日数の記録と表示
*   [ ] **Badges**: 特定条件達成によるバッジ付与

### Phase 7: エコシステム拡大 (Mobile & API)
PC 以外のデバイスや他サービスとの連携を強化します。

*   [ ] **PWA (Progressive Web App)**: スマホでのアプリライクな体験, オフライン対応
*   [ ] **Responsive UI**: モバイル向けビューの最適化
*   [ ] **Data Portability**: Markdown 一括エクスポート, Qiita/Zenn へのクロスポスト機能
*   [ ] **Public API**: ユーザーが自分のデータを取得できる API の公開

## 6. さらなる機能拡張案 (New Ideas)

Outputudy の「学習 + アウトプット」というテーマをさらに深めるための追加アイデアです。

*   **AI 暗記カード (Flashcards)**
    *   投稿した内容から AI が重要なポイントを抜き出し、自動で「一問一答」を作成。復習に活用できます。
*   **学習ロードマップ (Study Plans)**
    *   「React 完全マスター」のようなロードマップを作成し、各ステップに自分の投稿を紐付ける機能。進捗可視化。
*   **音声入力 & 文字起こし (Voice Output)**
    *   散歩中などに「学んだこと」を喋って記録すると、AI が整理されたテキスト記事に変換してくれる機能。

## 7. 直近のネクストアクション (Phase 0)

まずは **Phase 0: Initial Deployment** に全力を注ぎます。

1.  **Containerize**: `Dockerfile` が本番運用（サイズ、セキュリティ）に耐えうるか確認・修正
2.  **IaC**: Terraform プロジェクトのセットアップ (`/infra` ディレクトリ作成)
3.  **Deploy**: まずは手動 (`gcloud`) で Cloud Run へのデプロイを成功させる


---
*Created by Antigravity*
