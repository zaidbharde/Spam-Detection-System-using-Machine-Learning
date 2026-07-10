# Deployment Diagram Source

```mermaid
graph TB
  Browser --> StreamlitApp
  StreamlitApp --> LocalFS[(Local File System)]
  StreamlitApp --> Logs[(logs/)]
  StreamlitApp --> Outputs[(outputs/)]
```
