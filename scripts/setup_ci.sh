#!/bin/bash
set -e

# --- Configuration ---
PROJECT_ID="outputudy-446716"
REGION="asia-northeast1"
GITHUB_REPO="umwinter/outputudy"

# Service Account for CI
SA_NAME="github-actions-sa"
SA_DISPLAY_NAME="Service Account for GitHub Actions"

# Workload Identity
POOL_NAME="github-actions-pool"
POOL_DISPLAY_NAME="GitHub Actions Pool"
PROVIDER_NAME="github-provider"
PROVIDER_DISPLAY_NAME="GitHub Provider"

# Terraform State Bucket
TF_STATE_BUCKET="${PROJECT_ID}-tfstate"

# --- Main Execution ---

echo "🚀 Starting CI Setup for Project: ${PROJECT_ID}"
gcloud config set project ${PROJECT_ID}

# 1. Enable APIs
echo "📦 Enabling necessary APIs..."
gcloud services enable iam.googleapis.com \
    cloudresourcemanager.googleapis.com \
    iamcredentials.googleapis.com \
    sts.googleapis.com

# 2. Create Service Account
if ! gcloud iam service-accounts describe "${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" > /dev/null 2>&1; then
    echo "👤 Creating Service Account: ${SA_NAME}..."
    gcloud iam service-accounts create "${SA_NAME}" \
        --display-name="${SA_DISPLAY_NAME}"
else
    echo "✅ Service Account ${SA_NAME} already exists."
fi

SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

# 3. Grant Editor Role to SA
echo "🔑 Granting Editor role to ${SA_EMAIL}..."
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/editor" > /dev/null

# 4. Create Workload Identity Pool
if ! gcloud iam workload-identity-pools describe "${POOL_NAME}" --location="global" > /dev/null 2>&1; then
    echo "🏊 Creating Workload Identity Pool: ${POOL_NAME}..."
    gcloud iam workload-identity-pools create "${POOL_NAME}" \
        --location="global" \
        --display-name="${POOL_DISPLAY_NAME}"
else
    echo "✅ Workload Identity Pool ${POOL_NAME} already exists."
fi

# 5. Create Workload Identity Provider
if ! gcloud iam workload-identity-pools providers describe "${PROVIDER_NAME}" \
    --workload-identity-pool="${POOL_NAME}" \
    --location="global" > /dev/null 2>&1; then
    echo "🔌 Creating Workload Identity Provider: ${PROVIDER_NAME}..."
    gcloud iam workload-identity-pools providers create-oidc "${PROVIDER_NAME}" \
        --workload-identity-pool="${POOL_NAME}" \
        --location="global" \
        --display-name="${PROVIDER_DISPLAY_NAME}" \
        --issuer-uri="https://token.actions.githubusercontent.com" \
        --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
        --attribute-condition="assertion.repository == '${GITHUB_REPO}'"
else
    echo "✅ Workload Identity Provider ${PROVIDER_NAME} already exists."
fi

# 6. Bind SA to Workload Identity
echo "🔗 Binding Service Account to GitHub Repo..."
WORKLOAD_IDENTITY_USER="principalSet://iam.googleapis.com/projects/$(gcloud projects describe ${PROJECT_ID} --format='value(projectNumber)')/locations/global/workloadIdentityPools/${POOL_NAME}/attribute.repository/${GITHUB_REPO}"

gcloud iam service-accounts add-iam-policy-binding "${SA_EMAIL}" \
    --role="roles/iam.workloadIdentityUser" \
    --member="${WORKLOAD_IDENTITY_USER}" > /dev/null

# 7. Create Terraform State Bucket (if not exists)
if ! gcloud storage buckets describe "gs://${TF_STATE_BUCKET}" > /dev/null 2>&1; then
    echo "🪣 Creating Terraform State Bucket: ${TF_STATE_BUCKET}..."
    gcloud storage buckets create "gs://${TF_STATE_BUCKET}" --location="${REGION}"
else
    echo "✅ Terraform State Bucket ${TF_STATE_BUCKET} already exists."
fi

echo "🎉 CI Setup Completed Successfully!"
echo "---------------------------------------------------"
echo "Project ID: ${PROJECT_ID}"
echo "Service Account: ${SA_EMAIL}"
echo "Workload Identity Provider: projects/$(gcloud projects describe ${PROJECT_ID} --format='value(projectNumber)')/locations/global/workloadIdentityPools/${POOL_NAME}/providers/${PROVIDER_NAME}"
echo "---------------------------------------------------"
