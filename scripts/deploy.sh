#!/bin/bash
set -e

# Load configuration from central config file
SCRIPT_DIR=$(dirname "$0")
PROJECT_ROOT=$(cd "$SCRIPT_DIR/.." >/dev/null 2>&1 && pwd)
CONFIG_FILE="$PROJECT_ROOT/config/deploy.toml"

get_config_value() {
    local key=$1
    grep -E "^${key}[[:space:]]*=" "$CONFIG_FILE" | sed -E 's/.*=[[:space:]]*"(.*)".*/\1/'
}

SERVICE_NAME=$(get_config_value "service_name")
REGION=$(get_config_value "region")
SECRET_NAME=$(get_config_value "secret_name")
REPO_NAME=$(get_config_value "repo_name")
PROJECT_ID=$(get_config_value "project_id")
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
SERVICE_ACCOUNT="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

echo "�� Starting Deployment Process..."

# 1. Upload Secrets
echo "--- Step 1: Uploading Secrets & Granting Access ---"
./scripts/update_cloud_run_secrets.sh

# 2. Ensure Artifact Registry Repository exists
echo "--- Step 2: Ensuring Artifact Registry Repository exists ---"
gcloud artifacts repositories describe $REPO_NAME --location=$REGION --project=$PROJECT_ID >/dev/null 2>&1 || \
gcloud artifacts repositories create $REPO_NAME \
    --repository-format=docker \
    --location=$REGION \
    --description="Repository for Cloud Run images" \
    --project=$PROJECT_ID

# 3. Grant Cloud Build permission to Run
echo "--- Step 3: Granting Cloud Build permissions ---"
# Give Cloud Build standard service account access to Run the service
CLOUDBUILD_SA="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$CLOUDBUILD_SA" \
    --role="roles/run.admin" \
    --quiet >/dev/null

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$CLOUDBUILD_SA" \
    --role="roles/iam.serviceAccountUser" \
    --quiet >/dev/null


# 4. Trigger build
echo "--- Step 4: Submitting manual build to emulate CD trigger ---"
gcloud builds submit \
    --project=$PROJECT_ID \
    --config cloudbuild.yaml \
    --substitutions=_REGION=$REGION,_SERVICE_NAME=$SERVICE_NAME,_REPO_NAME=$REPO_NAME,_SECRET_NAME=$SECRET_NAME,TAG_NAME=latest .

echo "✅ Manual deployment complete! The continuous deployment trigger should use identical steps."
