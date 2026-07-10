# Architecture Reconstruction

## 4.1 Architecture Layers
```text
┌─────────────────────────────────────────┐
│             CLIENT LAYER                │
│   Streamlit browser interface in app.py │
├─────────────────────────────────────────┤
│          GATEWAY / BFF LAYER            │
│      None detected; Streamlit acts      │
│      as the direct UI-to-pipeline shim  │
├─────────────────────────────────────────┤
│         APPLICATION LAYER               │
│  app.py, TrainingPipeline,              │
│  PredictionPipeline                     │
├─────────────────────────────────────────┤
│          BUSINESS LOGIC                  │
│  data cleaning, TF-IDF, model search,   │
│  confidence estimation                   │
├─────────────────────────────────────────┤
│            DATA ACCESS                   │
│  CSV ingestion, MBOX parsing, pickle    │
│  artifact loading                        │
├─────────────────────────────────────────┤
│         PERSISTENCE LAYER                │
│  data/dataset, outputs/, logs/          │
└─────────────────────────────────────────┘
```

## Architecture Summary
The project is a single-process local ML application. The UI talks directly to the inference pipeline; there is no separate API tier, database, cache, or message broker.

Training and inference are intentionally decoupled by artifacts. Training writes the vectorizer and best model to `outputs/`, and inference reads those serialized files back into memory.

## System Architecture
```mermaid
graph TB
  User[User] --> Streamlit[Streamlit app.py]
  Streamlit --> Predict[PredictionPipeline]
  Predict --> Vectorizer[TF-IDF Vectorizer]
  Predict --> Model[Saved SVM Model]
  Predict --> Result[Spam / Ham Result]

  Train[TrainingPipeline] --> Ingest[DataIngestion]
  Ingest --> Transform[DataTransformation]
  Transform --> TrainModels[ModelTraining]
  TrainModels --> Artifacts[outputs/: pkl + csv]
  Artifacts --> Predict
```

## Request Lifecycle Flow
```mermaid
sequenceDiagram
  participant User
  participant UI as Streamlit UI
  participant Pipe as PredictionPipeline
  participant Prep as Text Cleanup
  participant Model as Saved Classifier
  participant View as Result Panel

  User->>UI: Paste email or upload MBOX
  UI->>Pipe: Send text / file path
  Pipe->>Prep: Clean body and parse mailbox metadata
  Prep-->>Pipe: Normalized text records
  Pipe->>Model: Vectorize and predict
  Model-->>Pipe: Label and confidence signal
  Pipe-->>UI: Prediction payload
  UI-->>User: Render spam / ham outcome
```

## Component Dependency Graph
```mermaid
graph LR
  app[app.py] --> pp[PredictionPipeline]
  tp[TrainingPipeline] --> di[DataIngestion]
  tp --> dt[DataTransformation]
  tp --> mt[ModelTraining]
  pp --> eu[email_utils]
  pp --> cfg[Config]
  mt --> cfg
  mt --> state[TrainingState]
  dt --> state
  di --> state
```

## User Journey Map
```mermaid
journey
  title User Classifies Email
  section Onboarding
    Open App: 5: User
    Load Model Artifacts: 3: System
  section Core Flow
    Paste Email or Upload MBOX: 5: User
    System Cleans and Predicts: 5: System
    Review Spam/Ham Output: 5: User
```

## Deployment Architecture
```mermaid
graph TB
  subgraph Local Machine
    Browser[Browser]
    App[Streamlit Process]
    FS[(Local File System)]
    Logs[(logs/)]
    Outputs[(outputs/)]
  end

  Browser --> App
  App --> FS
  App --> Logs
  App --> Outputs
```

## Key Architectural Notes
- No external network service is required for inference.
- The design is artifact-driven: model files are part of the runtime contract.
- The main seam for future refactoring is separating parsing, preprocessing, and prediction into independently testable modules.
