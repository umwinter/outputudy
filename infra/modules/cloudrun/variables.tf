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

variable "network_name" {
  type = string
}

variable "subnet_name" {
  type = string
}

variable "db_private_ip" {
  type = string
}

variable "secret_key" {
  type      = string
  sensitive = true
}
