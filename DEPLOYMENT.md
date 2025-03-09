# Google Cloud deployment

1.  Set the GCP project ID as an environment variable.

    ```shell
    export PROJECT_ID={google project id}
    export PROJECT_NUMBER={google project number}
    export OPEN_AI_KEY={api key}
    export FLASK_SECRET_KEY={flask secret key}
    export GITHUB_CLIENT_SECRET={github client secret}
    ```

1.  Create a service account for the pipeline.

    ```shell
    gcloud auth login
    gcloud config set project ${PROJECT_ID}
    gcloud auth application-default login
    gcloud services enable \
     iamcredentials.googleapis.com \
     run.googleapis.com \
     cloudbuild.googleapis.com \
     artifactregistry.googleapis.com \
     cloudresourcemanager.googleapis.com \
     compute.googleapis.com \
     secretmanager.googleapis.com \
     --project "${PROJECT_ID}"
    gcloud iam service-accounts create github-service-account --project "${PROJECT_ID}"
    ```

1.  Create a workload identity pool.

    ```shell
    gcloud iam workload-identity-pools create github-pool \
      --project="${PROJECT_ID}" \
      --location="global" \
      --display-name=github-pool
    gcloud iam workload-identity-pools describe github-pool \
      --project="${PROJECT_ID}" \
      --location="global" \
      --format="value(name)"
    ```

1.  Set the workload identity pool ID from the output of the last command.

    ```shell
    export WORKLOAD_IDENTITY_POOL_ID={previous command output}
    ```

1.  Create a workload identity pool provider.

    ```shell
    gcloud iam workload-identity-pools providers create-oidc github-provider \
      --project="${PROJECT_ID}" \
      --location="global" \
      --workload-identity-pool=github-pool \
      --display-name=github-provider \
      --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
      --attribute-condition="assertion.repository_owner=='initialcapacity' && assertion.ref=='refs/heads/main'" \
      --issuer-uri="https://token.actions.githubusercontent.com"
    gcloud iam service-accounts add-iam-policy-binding "github-service-account@${PROJECT_ID}.iam.gserviceaccount.com" \
      --project="${PROJECT_ID}" \
      --role="roles/iam.workloadIdentityUser" \
      --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/initialcapacity/ai-weekend-agents"
    gcloud iam workload-identity-pools providers describe github-provider \
      --project="${PROJECT_ID}" \
      --location="global" \
      --workload-identity-pool=github-pool \
      --format="value(name)"
    ```

1.  Give api permissions to the service account.

    ```shell
    gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:github-service-account@${PROJECT_ID}.iam.gserviceaccount.com" \
        --role="roles/artifactregistry.admin"
    gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:github-service-account@${PROJECT_ID}.iam.gserviceaccount.com" \
        --role="roles/run.admin"
    gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:github-service-account@${PROJECT_ID}.iam.gserviceaccount.com" \
        --role="roles/viewer"
    gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:github-service-account@${PROJECT_ID}.iam.gserviceaccount.com" \
        --role="roles/iam.serviceAccountUser"
    gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:github-service-account@${PROJECT_ID}.iam.gserviceaccount.com" \
        --role="roles/cloudbuild.builds.viewer"
    gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:github-service-account@${PROJECT_ID}.iam.gserviceaccount.com" \
        --role="roles/cloudbuild.builds.builder"
    gcloud projects get-iam-policy $PROJECT_ID --flatten="bindings[].members" \
        --format='table(bindings.role)' \
        --filter="bindings.members:github-service-account@${PROJECT_ID}.iam.gserviceaccount.com"
    ```

1.  Create secrets.
    ```shell
    echo -n "$OPEN_AI_KEY" | gcloud secrets create OPEN_AI_KEY --data-file=-
    echo -n "$FLASK_SECRET_KEY" | gcloud secrets create FLASK_SECRET_KEY --data-file=-
    echo -n "$GITHUB_CLIENT_SECRET" | gcloud secrets create GITHUB_CLIENT_SECRET --data-file=-
    ```

1.  Allow the default service account to access secrets.
    ```shell
    gcloud projects add-iam-policy-binding "$PROJECT_ID" \
        --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
        --role='roles/secretmanager.secretAccessor'
    ```

## Variables

Repository variables for pipeline

```shell
GCP_PROJECT_ID=${PROJECT_ID}
GCP_WORKLOAD_IDENTITY_POOL_ID=${WORKLOAD_IDENTITY_POOL_ID}/providers/github-provider
GCP_SERVICE_ACCOUNT=github-service-account@${PROJECT_ID}.iam.gserviceaccount.com
```
