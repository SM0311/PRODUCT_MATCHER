# Product Matching System

## Objective

The goal of this project is to develop an intelligent, automated system to match external supplier products with internal store inventory. This aims to replace the current slow and manual process. The match criteria require exact alignment on product manufacturer, name, and size.

---

## Project Structure
```bash
├── data/
│   ├── Data_External.csv        # Supplier products
│   └── Data_Internal.csv        # Store inventory products
│
├── notebooks/
│   └── notebook4.ipynb          # Exploratory development and final logic tests
│
├── utils/
│   ├── cleaning.py              # String-based cleaning functions
│   ├── exact_match.py           # Exact matching logic
│   ├── fuzzy_match.py           # Fuzzy match using RapidFuzz
│   ├── gpt_match.py             # GPT validation logic
│   └── fuzzy_gpt_match.py       # Fuzzy + GPT matching integration
│
├── app.py                       # Streamlit application entry point
├── requirements.txt             # List of dependencies

---
```

##  How It Works

1. **Upload CSVs**  
   - External products (e.g. from suppliers)  
   - Internal store product catalog

2. **Preview Cleaned Data**  
   - Product names are standardized using lowercase, punctuation removal, and size normalization.

3. **Choose Matching Logic**  
   - **Exact Match**: Full cleaned string equality  
   - **Fuzzy Match**: Uses RapidFuzz token sort ratio  
   - **Fuzzy + GPT Match**: Fuzzy match + GPT-4 validation  
     - GPT prompt checks brand, name, and size strictly  
     - Returns only `MATCH` or `NO MATCH`

4. **Download Results**  
   - Final table includes:
     - External Product Name  
     - Internal Product Name (or `NULL`)  
     - Match Status (MATCHED / NO MATCH)

---

## Technologies Used

- Python
- Pandas
- Numpy
- RapidFuzz
- OpenAI GPT-4 API
- Streamlit (UI)

---

## How to Run the Project

1. **Clone the repository**
```bash
git clone https://github.com/SM0311/PRODUCT_MATCHER_APP.git

```

## Install dependencies
```bash
pip install -r requirements.txt

```

## Add OpenAI API Key

Add API _KEY to get the access of LLM


## Run the Streamlit app

``` bash
streamlit run app.py
```




