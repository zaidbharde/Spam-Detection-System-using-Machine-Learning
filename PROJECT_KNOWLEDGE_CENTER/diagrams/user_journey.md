# User Journey Diagram Source

```mermaid
journey
  title User Completes Email Classification
  section Open App
    Launch Streamlit App: 5: User
  section Analyze Email
    Paste Message: 5: User
    System Cleans Text: 5: System
    Show Prediction: 5: User
  section Batch Mode
    Upload MBOX: 5: User
    Process Archive: 5: System
    Download CSV: 5: User
```
