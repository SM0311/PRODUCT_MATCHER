from rapidfuzz import process, fuzz

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

def perform_fuzzy_matching(df_external, df_internal, threshold=80):
    internal_names = df_internal['cleaned_long_name'].dropna().unique().tolist()

    df_external = df_external.copy()
    df_external['Internal_Product_Name'], df_external['Fuzzy_Score'] = zip(*df_external['cleaned_name'].apply(
        lambda x: fuzzy_match_product(x, internal_names, threshold)
    ))

    df_external['Internal_Product_Name'] = df_external['Internal_Product_Name'].fillna('NULL')
    return df_external
