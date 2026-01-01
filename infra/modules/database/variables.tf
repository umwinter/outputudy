variable "project_id" {
  type = string
}

variable "region" {
  type = string
}

variable "app_name" {
  type = string
}

variable "db_password" {
  type      = string
  sensitive = true
}

variable "db_activation_policy" {
  type = string
}

variable "network_id" {
  description = "VPC Network ID for Private IP"
  type        = string
}

variable "private_vpc_connection" {
  description = "Dependency for private VPC connection"
  type        = any
}
