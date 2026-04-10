provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {
  description = "The GCP Project ID"
  type        = string
}

variable "region" {
  description = "The GCP Region"
  type        = string
  default     = "us-central1"
}

variable "image_uri" {
  description = "The URI of the container image to deploy"
  type        = string
}

resource "google_cloud_run_v2_service" "a2a_agent" {
  name     = "sample-a2a-agent"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = var.image_uri
      ports {
        container_port = 8080
      }
      env {
        name  = "GOOGLE_GENAI_USE_VERTEXAI"
        value = "TRUE"
      }
      env {
        name  = "GOOGLE_CLOUD_PROJECT"
        value = var.project_id
      }
    }
  }
}

# Allow public access (Security is handled at the app level via OAuth in A2A)
resource "google_cloud_run_v2_service_iam_member" "public_access" {
  name     = google_cloud_run_v2_service.a2a_agent.name
  location = google_cloud_run_v2_service.a2a_agent.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

output "service_url" {
  value = google_cloud_run_v2_service.a2a_agent.uri
}
