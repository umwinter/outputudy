# 1. Service Account for GitHub Actions
resource "google_service_account" "github_actions" {
  account_id   = "github-actions-sa"
  display_name = "Service Account for GitHub Actions"
}

# 2. Grant Editor role to the Service Account (to manage infra)
resource "google_project_iam_member" "github_actions_editor" {
  project = var.project_id
  role    = "roles/editor" # Strong permission for Terraform Apply
  member  = "serviceAccount:${google_service_account.github_actions.email}"
}

# 3. Workload Identity Pool
resource "google_iam_workload_identity_pool" "pool" {
  workload_identity_pool_id = "github-actions-pool"
  display_name              = "GitHub Actions Pool"
  description               = "Identity pool for GitHub Actions"
  disabled                  = false
}

# 4. Workload Identity Provider
resource "google_iam_workload_identity_pool_provider" "provider" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.pool.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-provider"
  display_name                       = "GitHub Provider"
  description                        = "OIDC Identity Provider for GitHub Actions"
  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.repository" = "assertion.repository"
  }
  attribute_condition = "assertion.repository == '${var.github_repo}'"
  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}
