output "backend_url" {
  description = "The URL of the Backend Cloud Run service"
  value       = google_cloud_run_v2_service.backend.uri
}

output "frontend_url" {
  description = "The URL of the Frontend Cloud Run service"
  value       = google_cloud_run_v2_service.frontend.uri
}

output "database_connection_name" {
  description = "The connection name of the Cloud SQL instance"
  value       = google_sql_database_instance.master.connection_name
}

output "wif_provider_name" {
  description = "Workload Identity Provider resource name"
  value       = google_iam_workload_identity_pool_provider.provider.name
}

output "service_account_email" {
  description = "Service Account email for GitHub Actions"
  value       = google_service_account.github_actions.email
}



output "bucket_name" {
  description = "The name of the GCS bucket"
  value       = google_storage_bucket.media.name
}
