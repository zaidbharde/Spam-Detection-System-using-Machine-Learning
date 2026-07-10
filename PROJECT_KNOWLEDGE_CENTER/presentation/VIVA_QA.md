# Viva / Defense Questions

## 20 Likely Questions With Model Answers
1. What problem does the project solve?
The project classifies email text as spam or ham so users can quickly filter messages.
2. Why use Streamlit?
It gives a simple browser UI without needing a separate front-end stack.
3. Why use TF-IDF?
It turns text into numeric features that classical ML models can learn from.
4. Why are multiple models trained?
To compare candidates and choose the strongest performer.
5. What model won?
SVM won in the latest saved run.
6. Why is the dataset imbalanced?
The source data has many more ham messages than spam messages.
7. How is the data split?
The code uses a 70/30 train/test split with stratification.
8. How is confidence calculated?
By using predicted probabilities when available, or a decision-margin heuristic otherwise.
9. Why save the vectorizer?
The inference path must use the same vocabulary as training.
10. Why save the model?
So the app can predict without retraining on every run.
11. What is the biggest operational risk?
Hardcoded artifact paths can break inference when a new training run is created.
12. Why use pickle?
It is convenient for saving scikit-learn objects.
13. Is pickle safe?
Only for trusted files; it should not be loaded from untrusted sources.
14. Why no database?
The project is file-backed and does not need one for its current scope.
15. Why no API layer?
Streamlit is serving the direct user interaction layer.
16. What is the main bottleneck?
Grid search during training.
17. What is the main testing gap?
No automated tests were found.
18. What metric matters most here?
Weighted F1 is a good primary metric for this imbalanced classification problem.
19. What would you improve first?
Stable artifact management and tests.
20. What makes the current system useful?
It is simple, local, and already has a complete train-and-predict flow.

## 10 Curveball Questions
1. Why should anyone trust the confidence score?
They should treat it as a helpful signal, not a calibrated guarantee, especially when it comes from a decision margin.
2. What happens if the dataset schema changes?
Training will likely fail or produce incorrect behavior unless validation is added.
3. Could spam wording drift over time?
Yes, and that is one reason retraining should be planned.
4. Why not use deep learning?
A classical TF-IDF plus scikit-learn approach is simpler and strong enough for this scope.
5. Why not use SHAP or LIME?
They are not implemented, but they could improve explainability.
6. What if the best model artifact gets deleted?
Inference fails until artifacts are regenerated or the config is updated.
7. Could the app be deployed publicly as-is?
Only with extra hardening, especially around access control and artifact management.
8. What if the mailbox file has unusual encodings?
The cleaning logic helps, but some content may still degrade.
9. Why not split parsing and prediction more cleanly?
That would improve testability; the current code prioritizes simplicity.
10. What if class imbalance worsens?
The evaluation should add minority-class metrics and possibly resampling.

## 5 What Would You Do Differently?
1. I would add a small test suite before expanding features.
2. I would replace hardcoded model paths with a stable alias or manifest.
3. I would separate mailbox parsing from prediction orchestration.
4. I would add calibration or clearer wording around confidence scores.
5. I would remove unused dependencies and keep the environment smaller.
