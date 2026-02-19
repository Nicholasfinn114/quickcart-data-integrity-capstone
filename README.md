# AltSchool Data Engineering Capstone: QuickCart Data Integrity Crisis


## Problem Statement
Marketing dashboards showed a revenue discrepancy against bank statements. This project provides an auditable pipeline to prove real revenue.


## Solution Architecture
1. **Python Normalization**: Messy JSON logs (with 4 different currency formats) are standardized into a single USD float column. 
2. **Test Filtering**: All transactions flagged as `test` or associated with test emails are excluded from the financial truth.
3. **SQL Deduplication**: Used `ROW_NUMBER()` window functions to handle payment retries, ensuring only one successful payment is counted per order.
4. **Reconciliation**: Compared internal "Successful Sales" against "Bank Settlements" to identify the **Discrepancy Gap**.


## How to Run
- Run `generate_quickcart_data.py` to create the dataset.
- Execute `scripts/clean_transactions.py` to produce the cleaned dataset.
- Run `sql/reconciliation.sql` in a Postgres environment to generate the final Finance Report.
