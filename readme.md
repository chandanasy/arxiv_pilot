## Ask multiple pdfs

First set the local python version and activate virtualenv

### Run locally without docker

`streamlit run src/app.py`

### Run with docker locally

- _Build_ : `docker build -t streamlitapp .`
- _Run_ : `docker run -p 8501:8501 streamlitapp`

### Run docker image using k8s

`docker build --platform linux/amd64 -t gcr.io/$GCP_PROJECT_ID/k8s-streamlit:test .`
`gcloud auth configure-docker`
`docker push gcr.io/$GCP_PROJECT_ID/k8s-streamlit:test`
