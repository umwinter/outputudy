output "network_name" {
  value = google_compute_network.vpc.name
}

output "network_id" {
  value = google_compute_network.vpc.id
}

output "subnet_name" {
  value = google_compute_subnetwork.subnet.name
}

output "subnet_id" {
  value = google_compute_subnetwork.subnet.id
}

output "private_vpc_connection" {
  # Allowing other resources to depend on this explicitly
  value = google_service_networking_connection.private_vpc_connection
}
