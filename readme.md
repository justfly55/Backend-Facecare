## Prerequisites

**Before you begin, make sure you have the following installed on your system**:
- Python
- Visual Studio Code
- Cloud SDK
- Google Cloud Run (in Google Cloud Platform)

## Steps
### 1. Clone the Repository
``` 
git clone https://github.com/justfly55/Backend-Facecare
```
### 2. Setup Google Cloud 
- Create new project
- Activate Cloud Run API and Cloud Build API

### 3. Install and init Google Cloud SDK
- https://cloud.google.com/sdk/docs/install

### 4. Cloud build & deploy
```
gcloud builds submit --tag gcr.io/<project_id>/<function_name>
gcloud run deploy --image gcr.io/<project_id>/<function_name> --platform managed
```
