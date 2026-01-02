#!/bin/bash
set -e

# --- Configuration ---
# Load .env if exists
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
elif [ -f "../.env" ]; then
    export $(grep -v '^#' ../.env | xargs)
fi

PROJECT_ID="${PROJECT_ID:-outputudy}"
REGION="${REGION:-asia-northeast1}"
GITHUB_REPO="${GITHUB_REPO:-umwinter/outputudy}"

# Bootstrap Settings
SA_CI_NAME="github-actions-sa"
SA_CI_DISPLAY="Service Account for GitHub Actions"
POOL_NAME="github-actions-pool"
PROVIDER_NAME="github-provider"
TF_STATE_BUCKET="${PROJECT_ID}-tfstate"

# App Config Settings
APP_NAME="outputudy"
SA_SCHEDULER_EMAIL="${APP_NAME}-scheduler-sa@${PROJECT_ID}.iam.gserviceaccount.com"
SERVICES=("${APP_NAME}-frontend" "${APP_NAME}-backend")

# --- Start ---
echo "🚀 Starting GCP Setup for Project: ${PROJECT_ID}"
gcloud config set project ${PROJECT_ID}
echo "---------------------------------------------------"

# --- PART 1: Bootstrap (CI Environment) ---
echo "📦 [Bootstrap] Ensuring APIs are enabled..."
gcloud services enable iam.googleapis.com \
    cloudresourcemanager.googleapis.com \
    iamcredentials.googleapis.com \
    sts.googleapis.com \
    sqladmin.googleapis.com \
    run.googleapis.com \
    cloudscheduler.googleapis.com > /dev/null 2>&1
echo "   ✅ APIs enabled."

echo "👤 [Bootstrap] Managing CI Service Account..."
if ! gcloud iam service-accounts describe "${SA_CI_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" > /dev/null 2>&1; then
    gcloud iam service-accounts create "${SA_CI_NAME}" --display-name="${SA_CI_DISPLAY}"
    echo "   ✅ Created SA: ${SA_CI_NAME}"
else
    echo "   ✅ SA exists: ${SA_CI_NAME}"
fi

SA_CI_EMAIL="${SA_CI_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

echo "🔑 [Bootstrap] ensuring Editor role for CI SA..."
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
    --member="serviceAccount:${SA_CI_EMAIL}" \
    --role="roles/editor" > /dev/null
echo "   ✅ Editor role verified."

echo "🏊 [Bootstrap] Managing Workload Identity..."
if ! gcloud iam workload-identity-pools describe "${POOL_NAME}" --location="global" > /dev/null 2>&1; then
    gcloud iam workload-identity-pools create "${POOL_NAME}" --location="global" --display-name="GitHub Actions Pool"
    echo "   ✅ Pool created."
else
    echo "   ✅ Pool exists."
fi

if ! gcloud iam workload-identity-pools providers describe "${PROVIDER_NAME}" --workload-identity-pool="${POOL_NAME}" --location="global" > /dev/null 2>&1; then
    gcloud iam workload-identity-pools providers create-oidc "${PROVIDER_NAME}" \
        --workload-identity-pool="${POOL_NAME}" --location="global" --display-name="GitHub Provider" \
        --issuer-uri="https://token.actions.githubusercontent.com" \
        --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
        --attribute-condition="assertion.repository == '${GITHUB_REPO}'"
    echo "   ✅ Provider created."
else
    echo "   ✅ Provider exists."
fi

WORKLOAD_IDENTITY_USER="principalSet://iam.googleapis.com/projects/$(gcloud projects describe ${PROJECT_ID} --format='value(projectNumber)')/locations/global/workloadIdentityPools/${POOL_NAME}/attribute.repository/${GITHUB_REPO}"
gcloud iam service-accounts add-iam-policy-binding "${SA_CI_EMAIL}" \
    --role="roles/iam.workloadIdentityUser" \
    --member="${WORKLOAD_IDENTITY_USER}" > /dev/null
echo "   ✅ Bound SA to GitHub Repo."

echo "🪣 [Bootstrap] Managing Terraform State Bucket..."
if ! gcloud storage buckets describe "gs://${TF_STATE_BUCKET}" > /dev/null 2>&1; then
    gcloud storage buckets create "gs://${TF_STATE_BUCKET}" --location="${REGION}"
    echo "   ✅ Bucket created: ${TF_STATE_BUCKET}"
else
    echo "   ✅ Bucket exists."
fi

# --- PART 2: Configuration (Post-Terraform) ---
echo "---------------------------------------------------"
echo "🔧 [Config] Applying App-Specific IAM Settings..."

# Scheduler SA
if gcloud iam service-accounts describe "${SA_SCHEDULER_EMAIL}" > /dev/null 2>&1; then
    echo "🤖 [Config] Granting Cloud SQL Admin to Scheduler SA..."
    gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
        --member="serviceAccount:${SA_SCHEDULER_EMAIL}" \
        --role="roles/cloudsql.admin" > /dev/null
    echo "   ✅ Permission granted."
else
    echo "⚠️  [Config] Scheduler SA not found. (Terraform hasn't run yet? Skipped.)"
fi

# Cloud Run Services
for SERVICE in "${SERVICES[@]}"; do
    if gcloud run services describe "${SERVICE}" --region="${REGION}" > /dev/null 2>&1; then
        echo "🌍 [Config] Making ${SERVICE} public..."
        gcloud run services add-iam-policy-binding "${SERVICE}" \
            --region="${REGION}" \
            --member="allUsers" \
            --role="roles/run.invoker" > /dev/null
        echo "   ✅ Public access granted."
    else
        echo "⚠️  [Config] Service ${SERVICE} not found. (Terraform hasn't run yet? Skipped.)"
    fi
done

echo "---------------------------------------------------"
echo "🎉 GCP Setup Completed!"
