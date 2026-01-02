# Workload Identity 設定手順

GitHub ActionsがGoogle Cloudのリソースを操作するために必要な「Workload Identity 連携」の設定手順です。
この設定は、Terraform管理から除外されているため、新しい環境セットアップ時やリポジトリ変更時に手動で実行する必要があります。

## 前提条件

- `gcloud` CLIがインストールされ、認証済みであること。
- プロジェクトオーナーまたはIAM管理者の権限を持っていること。

## 設定手順

### 環境変数の設定

```bash
# プロジェクトID
PROJECT_ID="your-project-id"

# GitHubリポジトリ (例: umwinter/outputudy)
GITHUB_REPO="umwinter/outputudy"

# サービスアカウント名 (Terraformで作成されたもの)
SA_NAME="github-actions-sa"
```

### 権限の付与

GitHub Actionsからの特定のリポジトリのリクエストに対して、サービスアカウントへのなりすまし（Impersonation）を許可します。

```bash
# プロジェクトIDを取得 (設定済みなら不要)
PROJECT_ID=$(gcloud config get-value project)

# Workload Identity Pool名を取得
POOL_NAME="github-actions-pool" # Terraformで設定した名前

# サービスアカウントのメールアドレス
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

# IAMポリシーバインディングの追加 (Workload Identity)
gcloud iam service-accounts add-iam-policy-binding "${SA_EMAIL}" \
  --project="${PROJECT_ID}" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/$(gcloud projects describe ${PROJECT_ID} --format='value(projectNumber)')/locations/global/workloadIdentityPools/${POOL_NAME}/attribute.repository/${GITHUB_REPO}"

# プロジェクト編集者権限の付与 (Terraform実行用)
# ※ これがないとTerraformでリソースを作成できません
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/editor"

# Cloud Scheduler用サービスアカウントへの権限付与
# (DB停止などのためにCloud SQL Admin権限が必要)
SCHEDULER_SA="${APP_NAME}-scheduler-sa@${PROJECT_ID}.iam.gserviceaccount.com"
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
  --member="serviceAccount:${SCHEDULER_SA}" \
  --role="roles/cloudsql.admin"
```

## 確認方法

以下のコマンドを実行し、バインディングが含まれていることを確認します。

```bash
gcloud iam service-accounts get-iam-policy "${SA_EMAIL}"
```

出力に `roles/iam.workloadIdentityUser` と対象のリポジトリが含まれていれば成功です。
