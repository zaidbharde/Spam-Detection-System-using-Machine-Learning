import streamlit as st
import pandas as pd
import tempfile
import os
import time
from src.pipeline.prediction_pipeline import PredictionPipeline

st.set_page_config(
    page_title="Spam Email Classifier",
    page_icon="📧",
    layout="centered"
)

@st.cache_resource
def get_pipeline():
    return PredictionPipeline(load_models=True)

try:
    pipeline = get_pipeline()
except Exception as e:
    st.error(f"Error loading models: {str(e)}")
    st.info("Run `python -m src.pipeline.training_pipeline` to train a model first.")
    st.stop()

st.title("📧 Spam Email Classifier")
st.markdown("Classify emails as **Spam** or **Ham** (Clean) using Machine Learning.")

tab1, tab2 = st.tabs(["📩 Single Email", "📁 Batch MBOX Processing"])

with tab1:
    st.header("Check a Single Email")
    email_text = st.text_area(
        "Paste the email content below:",
        height=200,
        placeholder="Type or paste an email here..."
    )

    if st.button("Classify Email", type="primary"):
        if email_text.strip():
            with st.spinner("Analyzing..."):
                try:
                    result = pipeline.predict_single_email(email_text)
                    prediction = result['prediction']
                    prob_spam = result.get('prob_spam_pct')
                    prob_ham = result.get('prob_ham_pct')
                    top_words = result.get('top_words', [])
                    threshold = result.get('threshold', 0.5)

                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if prediction == "Spam":
                            st.error(f"🚨 **SPAM**")
                        else:
                            st.success(f"✅ **HAM (Safe)**")

                    with col2:
                        if prob_spam is not None:
                            st.metric("Decision Threshold", f"{threshold:.0%}")

                    if prob_spam is not None:
                        st.subheader("Prediction Probabilities")
                        prob_col1, prob_col2 = st.columns(2)
                        with prob_col1:
                            spam_color = "inverse" if prediction == "Spam" else "normal"
                            st.metric(
                                "Spam Probability",
                                f"{prob_spam:.1f}%",
                                delta_color=spam_color
                            )
                        with prob_col2:
                            ham_color = "normal" if prediction == "Ham" else "inverse"
                            st.metric(
                                "Ham Probability",
                                f"{prob_ham:.1f}%",
                                delta_color=ham_color
                            )

                        prob_bar_val = prob_spam / 100.0
                        st.progress(prob_bar_val)
                        st.caption(
                            f"← Ham (0%) {'─' * 40} Spam (100%) →"
                        )

                    if top_words:
                        st.subheader("Top Influential Words")
                        word_data = []
                        for word, score in top_words:
                            direction = "→ Spam" if score > 0 else "→ Ham"
                            word_data.append({
                                "Word": f"`{word}`",
                                "Influence": f"{score:+.4f}",
                                "Direction": direction
                            })
                        st.dataframe(
                            pd.DataFrame(word_data),
                            hide_index=True,
                            use_container_width=True
                        )
                        st.caption(
                            "Positive influence = pushes toward Spam, "
                            "Negative influence = pushes toward Ham"
                        )
                    else:
                        st.info("Feature importance not available for this model type.")

                except Exception as e:
                    st.error(f"Error analyzing email: {str(e)}")
        else:
            st.warning("Please enter some text to classify.")

with tab2:
    st.header("Process MBOX File")
    uploaded_file = st.file_uploader("Upload an MBOX file", type=['mbox', 'txt'])

    if uploaded_file is not None:
        if st.button("Process File"):
            with st.spinner("Processing file... this may take a moment"):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mbox') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name

                    try:
                        df = pipeline.predict_mbox_file(tmp_path)

                        col1, col2, col3 = st.columns(3)
                        spam_count = len(df[df['Prediction'] == 'Spam'])
                        ham_count = len(df[df['Prediction'] == 'Ham'])

                        col1.metric("Total Emails", len(df))
                        col2.metric("Spam Found", spam_count, delta_color="inverse")
                        col3.metric("Ham", ham_count)

                        st.subheader("Results Preview")
                        preview_cols = [c for c in ['Time', 'Subject', 'Prediction', 'Spam Prob', 'Ham Prob'] if c in df.columns]
                        st.dataframe(df[preview_cols].head(10), hide_index=True, use_container_width=True)

                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download Full Results (CSV)",
                            data=csv,
                            file_name=f"predictions_{int(time.time())}.csv",
                            mime="text/csv",
                        )

                    finally:
                        if os.path.exists(tmp_path):
                            try:
                                os.unlink(tmp_path)
                            except OSError:
                                pass

                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")
