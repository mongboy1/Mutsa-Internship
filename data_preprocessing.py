
"""
Day 3 - Data Preprocessing Script
Project: Personal Expense Analysis Dashboard

This script validates the dataset based on the data specification,
performs preprocessing, and computes basic KPIs for verification.
"""

import pandas as pd

# ==============================
# 1. Load Data
# ==============================
# Update the path if needed
DATA_PATH = "C:\Users\최현석\OneDrive\바탕 화면\workspace\sample_expense_data_300.csv"

df = pd.read_csv(DATA_PATH)

# ==============================
# 2. Schema Validation
# ==============================
REQUIRED_COLUMNS = [
    "date",
    "amount",
    "category",
    "description",
    "payment_method",
    "is_fixed"
]

missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns: {missing_cols}")

# ==============================
# 3. Preprocessing
# ==============================

# Date parsing
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])

# Amount validation
df = df[df["amount"] > 0]

# Category normalization
VALID_CATEGORIES = [
    "식비", "교통비", "카페", "쇼핑",
    "주거/통신", "구독", "의료/건강",
    "문화/여가", "교육", "기타"
]
df["category"] = df["category"].where(df["category"].isin(VALID_CATEGORIES), "기타")

# Description handling
df["description"] = df["description"].fillna("내역 없음")

# is_fixed handling
df["is_fixed"] = df["is_fixed"].fillna(False).astype(bool)

# Derived columns
df["year_month"] = df["date"].dt.strftime("%Y-%m")

# ==============================
# 4. KPI Calculation (Validation Purpose)
# ==============================
total_expense = df["amount"].sum()
avg_expense = df["amount"].mean()
max_expense = df["amount"].max()
transaction_count = len(df)

fixed_expense = df.loc[df["is_fixed"], "amount"].sum()
fixed_ratio = fixed_expense / total_expense * 100 if total_expense > 0 else 0

# ==============================
# 5. Print Summary
# ==============================
print("===== KPI Validation Result =====")
print(f"Total Expense: {total_expense:,.0f}")
print(f"Average Expense: {avg_expense:,.0f}")
print(f"Max Expense: {max_expense:,.0f}")
print(f"Transaction Count: {transaction_count}")
print(f"Fixed Expense Total: {fixed_expense:,.0f}")
print(f"Fixed Expense Ratio: {fixed_ratio:.2f}%")

print("\n===== Category Summary (Top 5) =====")
print(
    df.groupby("category")["amount"]
      .sum()
      .sort_values(ascending=False)
      .head(5)
)

print("\n===== Monthly Expense Summary =====")
print(
    df.groupby("year_month")["amount"]
      .sum()
      .sort_index()
)

# ==============================
# 6. Save Preprocessed Data
# ==============================
OUTPUT_PATH = "expense_data_preprocessed.csv"
df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

print(f"\nPreprocessed file saved to: {OUTPUT_PATH}")
