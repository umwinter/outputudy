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

output "bucket_name" {
  description = "The name of the GCS bucket"
  value       = google_storage_bucket.media.name
}
