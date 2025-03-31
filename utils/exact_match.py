import pandas as pd
import numpy as np
import re


def perform_exact_match(df_external, df_internal):
    merged_df = df_external.merge(
        df_internal,
        how='left',
        left_on='cleaned_name',
        right_on='cleaned_long_name',
        suffixes=('_ext', '_int')
    )

    merged_df['Match_Status'] = merged_df['LONG_NAME'].apply(
        lambda x: 'MATCHED' if pd.notnull(x) else 'NO MATCH'
    )

    final_output = merged_df[['PRODUCT_NAME', 'LONG_NAME', 'Match_Status']].rename(columns={
        'PRODUCT_NAME': 'External_Product_Name',
        'LONG_NAME': 'Internal_Product_Name'
    })
    return final_output
