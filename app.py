import streamlit as st
import pandas as pd
from utils.cleaning import standardize_product_name
from utils.exact_match import perform_exact_match
from utils.fuzzy_match import perform_fuzzy_matching
from utils.gpt_match import validate_with_gpt
from utils.fuzzy_gpt_match import perform_fuzzy_gpt_matching

st.set_page_config(page_title="Product Matching App", layout="wide")
st.title("PRODUCT MATCHING APPLICATION")

# Upload Section
st.header("1. Upload Product Files")
external_file = st.file_uploader("Upload External Product CSV", type=["csv"])
internal_file = st.file_uploader("Upload Internal Product CSV", type=["csv"])

if external_file and internal_file:
    external_df = pd.read_csv(external_file)
    internal_df = pd.read_csv(internal_file)

    st.success("Files uploaded successfully!")

    # Cleaning (String-based only)
    external_df['cleaned_name'] = external_df['PRODUCT_NAME'].apply(standardize_product_name)
    internal_df['cleaned_long_name'] = internal_df['LONG_NAME'].apply(standardize_product_name)

    st.header("2. Preview Cleaned Data")
    with st.expander("External Products"):
        st.dataframe(external_df[['PRODUCT_NAME', 'cleaned_name']].head())
    with st.expander("Internal Products"):
        st.dataframe(internal_df[['LONG_NAME', 'cleaned_long_name']].head())

    # Matching Options
    st.header("3. Choose Matching Logic")
    match_option = st.radio("Select a Matching Method:", ["Exact Match", "Fuzzy Match","Fuzzy + GPT Match"])

    if match_option == "Exact Match":
        result = perform_exact_match(external_df, internal_df)
        st.subheader("Exact Match Results")
        st.dataframe(result)

    elif match_option == "Fuzzy Match":
        threshold = st.slider("Fuzzy Matching Threshold", min_value=70, max_value=100, value=90)
        result = perform_fuzzy_matching(external_df, internal_df, threshold)
        st.subheader("Fuzzy Match Results")
        st.dataframe(result)

    elif match_option == "Fuzzy + GPT Match":
        st.info("Running Fuzzy + GPT validation combined...")
        result = perform_fuzzy_gpt_matching(external_df, internal_df)
        st.subheader("Fuzzy + GPT Match Results")
        st.dataframe(result)

    # Export
    st.header("4. Download Results")
    csv = result.to_csv(index=False).encode('utf-8')
    st.download_button("Download Matched Results", csv, "matched_results.csv", "text/csv")

else:
    st.warning("Please upload both External and Internal product files to begin.")
