# CI/CD環境セットアップガイド

このプロジェクトのCI/CD（GitHub Actions）を稼働させるために必要なGoogle Cloud環境のセットアップ手順です。
Terraformで管理できない「権限自体の管理」や「初期ブートストラップ」について記述します。

## 1. 初期セットアップ (Bootstrap)

まず、Terraformを実行するためのサービスアカウントと、GitHub連携（Workload Identity）を作成します。
プロジェクトルートで以下のスクリプトを実行してください。

```bash
# 権限を持つユーザー（オーナーなど）でログインしておく
gcloud auth login

# セットアップスクリプト実行
bash scripts/setup_ci.sh
```

### スクリプトの実行内容
- サービスアカウント作成: `github-actions-sa`
- 権限付与: `roles/editor` (編集者)
- GitHub連携設定: `github-actions-pool` / `github-provider`
- Terraform用バケット作成: `outputudy-tfstate`

---

## 2. GitHub Secretsの設定 (GitHub上)

スクリプト実行後、GitHubリポジトリの `Settings > Secrets and variables > Actions` に以下の値を設定してください。
（スクリプトの出力結果をコピー推奨）

| Secret Name | Value Example | Description |
|---|---|---|
| `GCP_PROJECT_ID` | `outputudy-446716` | プロジェクトID |
| `GCP_SA_EMAIL` | `github-actions-sa@...` | 作成されたSAのメールアドレス |
| `GCP_WIF_PROVIDER` | `projects/.../providers/github-provider` | Workload Identity Providerの完全パス |
| `DB_PASSWORD` | (自由なパスワード) | DBユーザー用パスワード |
| `SECRET_KEY` | (ランダム文字列) | アプリケーションの秘密鍵 |

---

## 3. Terraform実行後の追加設定 (Post-Deployment)

Terraformによるリソース作成（CI実行）が完了した後、以下の権限を手動で付与する必要があります。これらはTerraformから実行できません。

### Cloud Scheduler用権限 (DB停止機能)
Cloud SchedulerがCloud SQLを停止するために、`cloudsql.admin` 権限が必要です。

```bash
# 変数設定 (適宜変更)
export PROJECT_ID="outputudy-446716"
export APP_NAME="outputudy"
export SCHEDULER_SA="${APP_NAME}-scheduler-sa@${PROJECT_ID}.iam.gserviceaccount.com"

# 権限付与
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
  --member="serviceAccount:${SCHEDULER_SA}" \
  --role="roles/cloudsql.admin"
```

### フロントエンド公開設定 (Public Access)
Cloud Runのフロントエンドをインターネット公開（未認証アクセス許可）にします。

```bash# フロントエンド・バックエンドの公開設定 (未認証アクセス許可)
# ※ APIをクライアントから直接呼ぶ場合、バックエンドも公開が必要です。
SERVICE_NAMES=("${APP_NAME}-frontend" "${APP_NAME}-backend")

for SERVICE in "${SERVICE_NAMES[@]}"; do
  gcloud run services add-iam-policy-binding "${SERVICE}" \
    --region="asia-northeast1" \
    --member="allUsers" \
    --role="roles/run.invoker"
done
```
