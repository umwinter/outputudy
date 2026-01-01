variable "project_id" {
  description = "The GCP Project ID"
  type        = string
}

variable "region" {
  description = "The GCP Region"
  type        = string
  default     = "asia-northeast1"
}

variable "app_name" {
  description = "Application name"
  type        = string
  default     = "outputudy"
}

variable "db_password" {
  description = "The password for the Cloud SQL database user"
  type        = string
  sensitive   = true
}

variable "db_activation_policy" {
  description = "Cloud SQL activation policy: ALWAYS (running) or NEVER (stopped)"
  type        = string
  default     = "ALWAYS"
}

variable "secret_key" {
  description = "The secret key for the application"
  type        = string
  sensitive   = true
}
