output "connection_name" {
  value = google_sql_database_instance.master.connection_name
}

output "private_ip_address" {
  value = google_sql_database_instance.master.private_ip_address
}

output "instance_name" {
  value = google_sql_database_instance.master.name
}

# Pass through for consistency if needed
output "db_user" {
  value = google_sql_user.users.name
}
