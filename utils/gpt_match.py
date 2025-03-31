import time
import pandas as pd
from openai import OpenAI

client = OpenAI(api_key="please generate the API key and paste here")

def build_prompt(external_name, internal_name):
    return f"""
SYSTEM (Context & Role):
You are an AI assistant specializing in product matching between an external supplier's product and an internal product catalog. You have deep knowledge of product naming conventions and sizing formats.

USER (Instructions & Format):
You will be given two product names:
1. External product (from supplier)
2. Internal product (from our catalog)

According to our business rules, these two products should be considered the same (i.e., a valid match) only if:
1. They have the same manufacturer (brand).
2. They have the same product name (semantically equivalent).
3. They have the same size (e.g., quantity in oz, lb, ml, etc.).

*Your task:*
- Compare the external product name with the internal product name.
- Decide if all three criteria are met.
- Respond with exactly one word, either \"MATCH\" or \"NO MATCH\" (all caps).  
- Do not provide any additional text or explanation.

Now here are the two product names for you to compare:
External product: \"{external_name}\"
Internal product: \"{internal_name}\"

Please respond with only \"MATCH\" or \"NO MATCH\".
"""

def validate_with_gpt(external_name, internal_name):
    if pd.isna(internal_name) or not external_name:
        return "NO MATCH"

    prompt = build_prompt(external_name, internal_name)

    try:
        time.sleep(1.2)  # To avoid rate limit
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a strict product matcher."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=5,
            temperature=0.0
        )
        answer = response.choices[0].message.content.strip().upper()
        return "MATCH" if answer == "MATCH" else "NO MATCH"

    except Exception as e:
        return f"ERROR: {str(e)}"

def apply_gpt_decision(df):
    df = df.copy()
    df['GPT_Decision'] = df.apply(
        lambda row: validate_with_gpt(row['PRODUCT_NAME'], row['Internal_Product_Name']) 
        if row['Internal_Product_Name'] != 'NULL' else 'NO MATCH',
        axis=1
    )
    return df
