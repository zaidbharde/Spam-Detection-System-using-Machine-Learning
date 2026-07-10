# Deployment Guide

## Prerequisites
- Python 3.13 or compatible environment.
- Installed dependencies from `pyproject.toml` or `requirements.txt`.
- Trained artifacts in `outputs/<timestamp>/models/`.

## Environment Variables
No required environment variables were declared in the source tree.

| Variable | Required | Default | Description | Example |
|----------|----------|---------|-------------|---------|
| none detected | No | N/A | The project currently uses hardcoded paths in `src/config/config.py`. | N/A |

## Local Development Setup
1. Create and activate a virtual environment.
2. Install dependencies.
3. Ensure `data/dataset/dataset.csv` exists.
4. Run training if the artifact paths do not already point to a valid model.
5. Launch Streamlit with `streamlit run app.py`.

## Docker Setup
No Docker configuration was found.

## CI/CD Pipeline Explanation
No CI/CD pipeline was detected.

## Production Deployment Checklist
- Confirm the model artifact path resolves correctly.
- Verify logs can be written to the runtime filesystem.
- Confirm the deployed user has read access to the artifact directory.
- Add authentication if the app is exposed publicly.

## Rollback Procedure
- Restore the previous `outputs/<timestamp>/models/` artifact set.
- Update `src/config/config.py` or the runtime alias to point back to the previous model.

## Health Check Endpoints
None detected.

## Monitoring and Alerting Setup
- Current monitoring is limited to file logs.
- For production, forward logs to a centralized system and add a basic uptime check around the Streamlit service.

## Backup Strategy
- Back up the dataset, trained artifacts, and generated observation CSVs.
- Preserve the log directory if audit history matters.

## Scaling Considerations
- Inference is lightweight and suitable for a small single-instance deployment.
- Training is CPU-bound and may take longer as the hyperparameter grid expands.
- If usage increases, move artifact management and serving into a more explicit service layer.
