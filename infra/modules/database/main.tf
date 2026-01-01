resource "google_sql_database_instance" "master" {
  name             = "${var.app_name}-db"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier              = "db-f1-micro" # Shared Core
    availability_type = "ZONAL"       # No HA

    activation_policy = var.db_activation_policy

    ip_configuration {
      ipv4_enabled    = false
      private_network = var.network_id
    }

    disk_autoresize = true
    disk_size       = 10
    disk_type       = "PD_HDD"
  }

  deletion_protection = true

  depends_on = [
    var.private_vpc_connection
  ]
}

resource "google_sql_database" "database" {
  name     = var.app_name
  instance = google_sql_database_instance.master.name
}

resource "google_sql_user" "users" {
  name     = "outputudy_user"
  instance = google_sql_database_instance.master.name
  password = var.db_password
}

# Service Account for Cloud Scheduler
resource "google_service_account" "scheduler_sa" {
  account_id   = "${var.app_name}-scheduler-sa"
  display_name = "Cloud Scheduler Service Account"
}

resource "google_project_iam_member" "scheduler_sql_admin" {
  project = var.project_id
  role    = "roles/cloudsql.admin" # Required to stop instance
  member  = "serviceAccount:${google_service_account.scheduler_sa.email}"
}

# Cloud Scheduler to Stop DB (Every 4 hours)
resource "google_cloud_scheduler_job" "db_stopper" {
  name        = "${var.app_name}-db-stopper"
  description = "Stop Cloud SQL instance every 4 hours to save cost"
  schedule    = "0 */4 * * *" # Every 4 hours at minute 0
  time_zone   = "Asia/Tokyo"
  region      = var.region

  http_target {
    http_method = "PATCH"
    # Call Cloud SQL Admin API to update settings
    uri = "https://sqladmin.googleapis.com/sql/v1beta4/projects/${var.project_id}/instances/${google_sql_database_instance.master.name}"

    body = base64encode(jsonencode({
      settings = {
        activationPolicy = "NEVER"
      }
    }))

    oauth_token {
      service_account_email = google_service_account.scheduler_sa.email
    }
  }
}
