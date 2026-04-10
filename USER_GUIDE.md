# User Guide: Deploying the Sample A2A + MCP Agent

This guide provides step-by-step instructions to get the Sample A2A Agent and MCP Server up and running in your Google Cloud environment.

## Overview

This deliverable contains:
- **Code**: A sample A2A agent (`a2a_agent.py`) and simulated MCP server (`mcp_server.py`).
- **Containerization**: A `Dockerfile` to package them together.
- **Infrastructure**: Terraform scripts (`terraform/main.tf`) to deploy to Google Cloud Run.
- **Tests**: Scripts to validate the setup and simulate the end-to-end flow.

## Prerequisites

Before you begin, ensure you have the following installed and configured:
1.  **Google Cloud SDK (gcloud)**: Authenticated to your GCP project.
2.  **Docker**: To build and push the container image.
3.  **Terraform**: To provision the infrastructure.
4.  **Python 3.12+**: To run local tests.

---

## Step 1: Build and Push the Container

We recommend using Google Artifact Registry to store your container image.

1.  **Create a repository** in Artifact Registry (if you don't have one):
    ```bash
    gcloud artifacts repositories create sample-repo \
        --repository-format=docker \
        --location=us-central1
    ```

2.  **Authenticate Docker** to the repository:
    ```bash
    gcloud auth configure-docker us-central1-docker.pkg.dev
    ```

3.  **Build the Docker image**:
    From the root directory of this project, run:
    ```bash
    docker build -t us-central1-docker.pkg.dev/[YOUR_PROJECT_ID]/sample-repo/a2a-agent:latest .
    ```
    *Replace `[YOUR_PROJECT_ID]` with your actual GCP project ID.*

4.  **Push the image**:
    ```bash
    docker push us-central1-docker.pkg.dev/[YOUR_PROJECT_ID]/sample-repo/a2a-agent:latest
    ```

---

## Step 2: Deploy with Terraform

Now we will deploy the container to Cloud Run using Terraform.

1.  Navigate to the `terraform` directory:
    ```bash
    cd terraform
    ```

2.  Initialize Terraform:
    ```bash
    terraform init
    ```

3.  Apply the configuration:
    ```bash
    terraform apply \
        -var="project_id=[YOUR_PROJECT_ID]" \
        -var="image_uri=us-central1-docker.pkg.dev/[YOUR_PROJECT_ID]/sample-repo/a2a-agent:latest"
    ```
    *Review the plan and type `yes` to confirm.*

4.  **Note the Output**: Terraform will output the `service_url`. This is the public URL of your A2A agent.

---

## Step 3: Verify the Deployment

1.  Test the **Agent Card** endpoint:
    Open a browser or use `curl` to hit:
    ```bash
    curl [YOUR_SERVICE_URL]/a2a/sample_a2a_head/.well-known/agent.json
    ```
    You should receive the JSON description of the agent.

---

## Step 4: Run Automated Tests

You can run these tests locally to verify the logic before or after deployment.

1.  **Validate Agent Card**:
    ```bash
    python3 test_agent_card.py
    ```
    This checks that `agent.json` exists and is valid.

2.  **Simulate E2E Orchestration**:
    ```bash
    python3 test_e2e_simulation.py
    ```
    This simulates a request from Gemini Enterprise and verifies that the A2A agent calls the mock MCP tools in the correct sequence to generate the campaign.

---

## Step 5: Next Steps (Marketplace Integration)

Now that your agent is running publicly, you need to:
1.  Configure **OAuth 2.0** to secure the endpoints.
2.  Publish the Agent Card URL to the **Gemini Enterprise** team or Marketplace.

For detailed steps on security and Marketplace listing, please refer to the [MARKETPLACE_GUIDE.md](../MARKETPLACE_GUIDE.md) included in this package.
