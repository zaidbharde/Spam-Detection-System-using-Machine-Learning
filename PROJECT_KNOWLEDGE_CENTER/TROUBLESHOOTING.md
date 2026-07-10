# Troubleshooting

## App Will Not Start
- Check that the saved model and vectorizer files exist at the configured paths.
- Confirm the virtual environment is active.
- Verify the installed Python version matches the project metadata closely enough to run the dependencies.

## Training Fails on CSV Load
- Confirm `data/dataset/dataset.csv` exists.
- Check that the file has `Category` and `Message` columns.
- Make sure the category labels are `spam` and `ham` in lowercase, as the current transform logic expects.

## Batch MBOX Processing Fails
- Ensure the uploaded file is a valid MBOX archive.
- Check that the mailbox file can be opened by the Python `mailbox` module.
- Verify the message bodies are decodable.

## Predictions Look Wrong
- Confirm the app is loading the intended model artifact version.
- Regenerate artifacts if the current model is stale.
- Inspect the cleaning step if the message contains unusual HTML or encoding.

## Confidence Is Missing
- Some classifiers may not expose calibrated probability estimates.
- The current fallback uses a decision-margin heuristic, not a true probability.
