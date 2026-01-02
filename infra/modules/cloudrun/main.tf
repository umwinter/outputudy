# Cloud Run (Backend)
resource "google_cloud_run_v2_service" "backend" {
  name     = "${var.app_name}-backend"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    vpc_access {
      network_interfaces {
        network    = var.network_name
        subnetwork = var.subnet_name
      }
      egress = "PRIVATE_RANGES_ONLY"
    }

    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello"


      env {
        name  = "DATABASE_URL"
        value = "postgresql+asyncpg://outputudy_user:${var.db_password}@${var.db_private_ip}/${var.app_name}"
      }
      env {
        name  = "SECRET_KEY"
        value = var.secret_key
      }
    }
  }

  lifecycle {
    ignore_changes = [
      client,
      client_version,
      template[0].containers[0].image
    ]
  }
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

  lifecycle {
    ignore_changes = [
      client,
      client_version,
      template[0].containers[0].image
    ]
  }
}



# Cloud Run Job (DB Migration)
resource "google_cloud_run_v2_job" "migration" {
  name     = "${var.app_name}-migration"
  location = var.region

  template {
    template {
      vpc_access {
        network_interfaces {
          network    = var.network_name
          subnetwork = var.subnet_name
        }
        egress = "PRIVATE_RANGES_ONLY"
      }

      containers {
        image = "us-docker.pkg.dev/cloudrun/container/hello"

        env {
          name = "DATABASE_URL"
          # Use synchronous driver (psycopg2) for Alembic migrations
          value = "postgresql+asyncpg://outputudy_user:${var.db_password}@${var.db_private_ip}/${var.app_name}"
        }
        env {
          name  = "SECRET_KEY"
          value = var.secret_key
        }

        # Override CMD to run migration
        command = ["alembic", "upgrade", "head"]
      }
    }
  }

  lifecycle {
    ignore_changes = [
      client,
      client_version,
      template[0].template[0].containers[0].image
    ]
  }
}

# Allow public access to Backend (RESTORED)
resource "google_cloud_run_service_iam_binding" "backend_noauth" {
  location = var.region
  service  = google_cloud_run_v2_service.backend.name
  role     = "roles/run.invoker"
  members = [
    "allUsers"
  ]
}

# Allow public access to Frontend (RESTORED)
resource "google_cloud_run_service_iam_binding" "frontend_noauth" {
  location = var.region
  service  = google_cloud_run_v2_service.frontend.name
  role     = "roles/run.invoker"
  members = [
    "allUsers"
  ]
}
