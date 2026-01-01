# Helper: Enable APIs first
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

# --- Shared Resources (Storage / Artifacts) ---

# Artifact Registry
resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = var.app_name
  description   = "Docker repository for ${var.app_name}"
  format        = "DOCKER"

  depends_on = [google_project_service.apis]
}

# Cloud Storage (Media)
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

# Terraform State Bucket (Already exists via backend config but ensuring managed)
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

# --- Module Calls ---

module "networking" {
  source = "./modules/networking"

  app_name = var.app_name
  region   = var.region

  depends_on = [google_project_service.apis]
}

module "database" {
  source = "./modules/database"

  project_id             = var.project_id
  region                 = var.region
  app_name               = var.app_name
  db_password            = var.db_password
  db_activation_policy   = var.db_activation_policy
  network_id             = module.networking.network_id
  private_vpc_connection = module.networking.private_vpc_connection

  depends_on = [module.networking]
}

module "iam" {
  source = "./modules/iam"

  project_id  = var.project_id
  github_repo = "umwinter/outputudy" # Hardcoded or could be variable

  depends_on = [google_project_service.apis]
}

module "cloudrun" {
  source = "./modules/cloudrun"

  project_id    = var.project_id
  region        = var.region
  app_name      = var.app_name
  db_password   = var.db_password
  network_name  = module.networking.network_name
  subnet_name   = module.networking.subnet_name
  db_private_ip = module.database.private_ip_address
  secret_key    = var.secret_key

  depends_on = [module.database, module.networking]
}
