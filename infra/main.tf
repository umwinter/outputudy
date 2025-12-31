resource "google_project_service" "apis" {
  for_each = toset([
    "run.googleapis.com",
    "compute.googleapis.com",
    "servicenetworking.googleapis.com",
    "sqladmin.googleapis.com",
    "iam.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "storage.googleapis.com",
    "secretmanager.googleapis.com",
    "artifactregistry.googleapis.com",
    "cloudscheduler.googleapis.com",
  ])
  service            = each.key
  disable_on_destroy = false
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

  depends_on = [google_project_service.apis]
}

# Artifact Registry
resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = var.app_name
  description   = "Docker repository for ${var.app_name}"
  format        = "DOCKER"

  depends_on = [google_project_service.apis]
}

# Cloud Storage
resource "google_storage_bucket" "media" {
  name          = "${var.project_id}-media"
  location      = var.region
  force_destroy = false

  uniform_bucket_level_access = true

  cors {
    origin          = ["*"]
    method          = ["GET", "HEAD", "PUT", "POST", "DELETE"]
    response_header = ["*"]
    max_age_seconds = 3600
  }

  depends_on = [google_project_service.apis]
}

# Terraform State Bucket
resource "google_storage_bucket" "tfstate" {
  name                        = "${var.project_id}-tfstate"
  location                    = var.region
  force_destroy               = false
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
  depends_on = [google_project_service.apis]
}

# VPC Network
resource "google_compute_network" "vpc" {
  name                    = "${var.app_name}-vpc"
  auto_create_subnetworks = false
  depends_on              = [google_project_service.apis]
}

resource "google_compute_subnetwork" "subnet" {
  name          = "${var.app_name}-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.vpc.id
}

# Private Service Access (for Cloud SQL Private IP)
resource "google_compute_global_address" "private_ip_address" {
  name          = "${var.app_name}-private-ip"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.vpc.id
}

resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.vpc.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]
  depends_on              = [google_project_service.apis]
}

# Cloud SQL
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
      private_network = google_compute_network.vpc.id
    }

    disk_autoresize = true
    disk_size       = 10
    disk_type       = "PD_HDD"
  }

  deletion_protection = false

  depends_on = [
    google_project_service.apis,
    google_service_networking_connection.private_vpc_connection
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

# Cloud Run (Placeholder Service)
resource "google_cloud_run_v2_service" "backend" {
  name     = "${var.app_name}-backend"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    vpc_access {
      network_interfaces {
        network    = google_compute_network.vpc.name
        subnetwork = google_compute_subnetwork.subnet.name
      }
      egress = "ALL_TRAFFIC"
    }

    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello"

      env {
        name = "DATABASE_URL"
        # Connection via Private IP (No auth proxy needed usually, but standard simple connection string works)
        # Note: Ideally usage of Cloud SQL Auth Proxy sidecar even with Private IP is recommended for encryption/auth, 
        # but for simple setup we can use direct IP. However, Cloud Run needs to know the IP. 
        # 'google_sql_database_instance.master.private_ip_address'
        value = "postgresql+asyncpg://outputudy_user:${var.db_password}@${google_sql_database_instance.master.private_ip_address}/${var.app_name}"
      }
    }
  }

  depends_on = [google_project_service.apis, google_sql_database_instance.master]
}

resource "google_cloud_run_v2_service_iam_binding" "backend_noauth" {
  location = google_cloud_run_v2_service.backend.location
  name     = google_cloud_run_v2_service.backend.name
  role     = "roles/run.invoker"
  members = [
    "allUsers"
  ]
}

# Cloud Run (Frontend)
resource "google_cloud_run_v2_service" "frontend" {
  name     = "${var.app_name}-frontend"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello"
      # In future, we will add ENV vars here (e.g. NEXT_PUBLIC_API_URL)
    }
  }

  depends_on = [google_project_service.apis]
}

resource "google_cloud_run_v2_service_iam_binding" "frontend_noauth" {
  location = google_cloud_run_v2_service.frontend.location
  name     = google_cloud_run_v2_service.frontend.name
  role     = "roles/run.invoker"
  members = [
    "allUsers"
  ]
}

# --- CI/CD & Workload Identity Federation ---

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
  attribute_condition = "assertion.repository == 'umwinter/outputudy'"
  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

# 5. Allow GitHub Actions (from specific repo) to impersonate the Service Account
resource "google_service_account_iam_member" "workload_identity_user" {
  service_account_id = google_service_account.github_actions.name
  role               = "roles/iam.workloadIdentityUser"

  # Limit access to this specific repository
  member = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.pool.name}/attribute.repository/umwinter/outputudy"
}
