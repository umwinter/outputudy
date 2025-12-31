output "backend_url" {
  value = google_cloud_run_v2_service.backend.uri
}

output "frontend_url" {
  value = google_cloud_run_v2_service.frontend.uri
}

output "migration_job_name" {
  value = google_cloud_run_v2_job.migration.name
}
