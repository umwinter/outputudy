# CI/CD環境セットアップガイド

このプロジェクトのCI/CD（GitHub Actions）を稼働させるために必要なGoogle Cloud環境のセットアップ手順です。
Terraformで管理できない「権限自体の管理」や「初期ブートストラップ」について記述します。

## 1. 環境セットアップ (Bootstrap & Config)

`scripts/setup_gcp.sh` スクリプトを使用して、必要なGCPリソースと権限を一括設定します。
このスクリプトは**いつでも何度でも実行可能**です。

- **初回実行時**: CI用のアカウントとGitHub連携を作成します。
- **Terraform実行後**: アプリケーション（Cloud Run, Scheduler）に必要な権限を追加適用します。

```bash
# 権限を持つユーザー（オーナーなど）でログインしておく
gcloud auth login

# セットアップスクリプト実行
mise run setup-gcp
```

---

## 2. GitHub Secretsの設定 (GitHub上)

スクリプト実行後、GitHubリポジトリの `Settings > Secrets and variables > Actions` に以下の値を設定してください。

| Secret Name | Value Example | Description |
|---|---|---|
| `GCP_PROJECT_ID` | `outputudy` (あるいは `.env` の値) | プロジェクトID |
| `GCP_SA_EMAIL` | `github-actions-sa@...` | 作成されたSAのメールアドレス |
| `GCP_WIF_PROVIDER` | `projects/.../providers/github-provider` | Workload Identity Providerの完全パス |
| `DB_PASSWORD` | (自由なパスワード) | DBユーザー用パスワード |
| `SECRET_KEY` | (ランダム文字列) | アプリケーションの秘密鍵 |

---
