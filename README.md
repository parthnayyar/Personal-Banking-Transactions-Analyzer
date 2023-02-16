# Personal-Banking-Transactions-Analyzer
This program allows a user to analyze their bank account transactions.

How to run:
1. Download your bank transaction files in csv format
2. For example, follow these steps to download CIBC transaction files:
    1. From Online Banking, select "My Accounts," then “Download Transactions”
    2. Choose the account and time period
    3. Choose "Spreadsheet (CSV)" under "Financial management software"
3. After you have downloaded all the transaction files you want to analyze, run the "main.py" file (right click -> open with Python)

## About Excludes
Excludes are any keywords that you do not want to include in your analysis. For example if you add an exclude "Internet Banking INTERNET TRANSFER", all the transactions with transaction descriptions that include the words "Internet Banking INTERNET TRANSFER" will not be considered during analysis.
### Recommended Excludes
1. "Internet Banking INTERNET TRANSFER" for internet transfers (eg. transferring money from chequing to savings account)
2. "Electronic Funds Transfer GIC Short-Term GIC" for transfer of GIC funds from GIC account to chequing account
3. "Branch Transaction CREDIT MEMO" for transferring money internationally
4. "PAYMENT THANK YOU/PAIEMEN T MERCI" and "PRE-AUTHORIZED PAYMENT - THANK YOU" for payment of credit cards
5. "Branch Transaction DEBIT MEMO"
6. "Branch Transaction CREDIT MEMO"
7. "Electronic Funds Transfer PREAUTHORIZED DEBIT CIBC CARD PRODUCTS DIVISION"

<img src="https://user-images.githubusercontent.com/97373046/219493795-940d620d-7e40-4f8b-98b6-e21a34d1b0ae.png" width="300" height="300">
<img src="https://user-images.githubusercontent.com/97373046/219493859-b47095a5-9abf-4c9d-9339-638697a67b1d.png" width="100" height="150">
<img src="https://user-images.githubusercontent.com/97373046/219493734-3e78350f-fe7e-4aa6-8f9a-7356cf53abb0.png" width="600" height="300">
