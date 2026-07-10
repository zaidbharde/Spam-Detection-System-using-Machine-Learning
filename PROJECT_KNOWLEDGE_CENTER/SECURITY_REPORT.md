# Security Report

## OWASP Top 10 Assessment
- A01 Broken Access Control: not applicable; no auth layer exists.
- A02 Cryptographic Failures: no cryptographic storage or transport layer found.
- A03 Injection: low risk in current code because there is no database or shell execution path.
- A04 Insecure Design: medium risk because model artifacts are loaded from disk without integrity checks.
- A05 Security Misconfiguration: medium risk because the app depends on hardcoded local paths.
- A06 Vulnerable and Outdated Components: unknown; no pinned vulnerability scan was available.
- A07 Identification and Authentication Failures: not applicable; no auth layer exists.
- A08 Software and Data Integrity Failures: medium risk due to untrusted pickle loading.
- A09 Security Logging and Monitoring Failures: medium risk because only basic file logs are present.
- A10 SSRF: not applicable; no network fetch logic was found.

## Secrets and Credentials Scan
- No committed `.env` file was found.
- No API keys, tokens, or credentials were discovered in the inspected source.
- The `.gitignore` excludes `.env` and similar environment files.

## Dependency Vulnerabilities
- Not scanned in this pass.
- Declared packages should still be reviewed with `pip-audit` or equivalent before release.

## Findings

### 🟠 High Finding: Untrusted pickle artifact loading
**Location**: [src/pipeline/prediction_pipeline.py](../src/pipeline/prediction_pipeline.py)
**Description**: The inference path loads `vectorizer.pkl` and `SVM_model.pkl` with `pickle.load`.
**Exploit Scenario**: If an attacker can replace those files, arbitrary code execution may occur during startup.
**Fix**: Restrict write access to the artifact directory, verify hashes/signatures before loading, or switch to a safer serialization strategy where possible.
**References**: OWASP A08

### 🟡 Medium Finding: Hardcoded model artifact paths
**Location**: [src/config/config.py](../src/config/config.py)
**Description**: The inference config points to a single timestamped output directory.
**Exploit Scenario**: The app can fail or load the wrong model if the directory is absent or replaced.
**Fix**: Use an environment variable or stable symlink for active artifacts, and validate the path on startup.
**References**: OWASP A05

### 🟡 Medium Finding: No authentication or access control
**Location**: [app.py](../app.py)
**Description**: The Streamlit interface has no authentication barrier.
**Exploit Scenario**: Anyone with access to the deployed app can submit arbitrary content and download outputs.
**Fix**: Add auth at the hosting layer or a login gate if the app is exposed publicly.
**References**: OWASP A01

### 🔵 Low Finding: Prediction exports may leak sensitive mail content
**Location**: [src/pipeline/prediction_pipeline.py](../src/pipeline/prediction_pipeline.py)
**Description**: Batch processing preserves subject, recipients, body, and direction fields in the exported CSV.
**Exploit Scenario**: A user could inadvertently share message content beyond their intended audience.
**Fix**: Document data-handling expectations and offer redaction options before export.
**References**: Data handling best practice
