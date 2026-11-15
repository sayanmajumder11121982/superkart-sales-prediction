# SuperKart Sales Prediction

Sales forecasting for SuperKart: a Flask backend that serves a tuned Random Forest model, and a Streamlit frontend.

- `backend/` - Flask API (`/`, `/v1/predict`, `/v1/predictbatch`), model file, Dockerfile (port 7860)
- `frontend/` - Streamlit app for single and batch predictions, Dockerfile (port 8501)

## Run in a GitHub Codespace

```bash
bash start.sh
```

Then set port 7860 to **Public** in the Ports tab and open port 8501 for the app.
