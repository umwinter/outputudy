output "backend_url" {
  description = "The URL of the Backend Cloud Run service"
  value       = module.cloudrun.backend_url
}

output "frontend_url" {
  description = "The URL of the Frontend Cloud Run service"
  value       = module.cloudrun.frontend_url
}

output "database_connection_name" {
  description = "The connection name of the Cloud SQL instance"
  value       = module.database.connection_name
}

output "wif_provider_name" {
  description = "Workload Identity Provider resource name"
  value       = module.iam.wif_provider_name
}

output "service_account_email" {
  description = "Service Account email for GitHub Actions"
  value       = module.iam.service_account_email
}

output "bucket_name" {
  description = "The name of the GCS bucket"
  value       = google_storage_bucket.media.name
}
