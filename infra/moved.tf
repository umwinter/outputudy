# Networking Moves
moved {
  from = google_compute_network.vpc
  to   = module.networking.google_compute_network.vpc
}

moved {
  from = google_compute_subnetwork.subnet
  to   = module.networking.google_compute_subnetwork.subnet
}

moved {
  from = google_compute_global_address.private_ip_address
  to   = module.networking.google_compute_global_address.private_ip_address
}

moved {
  from = google_service_networking_connection.private_vpc_connection
  to   = module.networking.google_service_networking_connection.private_vpc_connection
}

# Database Moves (CRITICAL: Prevents Data Loss)
moved {
  from = google_sql_database_instance.master
  to   = module.database.google_sql_database_instance.master
}

moved {
  from = google_sql_database.database
  to   = module.database.google_sql_database.database
}

moved {
  from = google_sql_user.user
  to   = module.database.google_sql_user.users
}

# IAM Moves
moved {
  from = google_service_account.github_actions
  to   = module.iam.google_service_account.github_actions
}

moved {
  from = google_iam_workload_identity_pool.pool
  to   = module.iam.google_iam_workload_identity_pool.pool
}

moved {
  from = google_iam_workload_identity_pool_provider.provider
  to   = module.iam.google_iam_workload_identity_pool_provider.provider
}

# Cloud Run Moves (Optional but cleaner)
moved {
  from = google_cloud_run_v2_service.backend
  to   = module.cloudrun.google_cloud_run_v2_service.backend
}

moved {
  from = google_cloud_run_v2_service.frontend
  to   = module.cloudrun.google_cloud_run_v2_service.frontend
}

moved {
  from = google_cloud_run_v2_job.migration
  to   = module.cloudrun.google_cloud_run_v2_job.migration
}
