import pandas as pd
from rapidfuzz import process, fuzz
from utils.gpt_match import validate_with_gpt

def fuzzy_match_product(external_name, internal_names, threshold=80):
    result = process.extractOne(
        external_name,
        internal_names,
        scorer=fuzz.token_sort_ratio,
        score_cutoff=threshold
    )
    if result:
        return result[0], result[1]
    return None, None

def perform_fuzzy_gpt_matching(df_external, df_internal, threshold=80):
    df_external = df_external.copy()
    internal_names = df_internal['cleaned_long_name'].dropna().unique().tolist()

    df_external['Internal_Product_Name'], df_external['Fuzzy_Score'] = zip(*df_external['cleaned_name'].apply(
        lambda x: fuzzy_match_product(x, internal_names, threshold)
    ))

    df_external['Internal_Product_Name'] = df_external['Internal_Product_Name'].fillna('NULL')

    df_external['Match_Status'] = df_external.apply(
        lambda row: validate_with_gpt(row['PRODUCT_NAME'], row['Internal_Product_Name'])
        if row['Internal_Product_Name'] != 'NULL' else 'NO MATCH',
        axis=1
    )

    final_df = df_external[['PRODUCT_NAME', 'Internal_Product_Name', 'Fuzzy_Score', 'Match_Status']].rename(columns={
        'PRODUCT_NAME': 'External_Product_Name'
    })
    return final_df
