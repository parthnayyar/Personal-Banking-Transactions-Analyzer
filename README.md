# CIBC-Analyze-Transactions
This program allows a CIBC user to analyze their CIBC bank account transactions.

How to run:
1. Install [Python](https://www.python.org/ftp/python/3.10.6/python-3.10.6-amd64.exe)
2. Check "Add Python to PATH" on installation screen
3. After installation is complete, open command prompt and run following command: "pip install pandas numpy matplotlib"
4. Clone/Download this repositary on to your local computer
5. Download your CIBC transaction files:
    1. From Online Banking, select "My Accounts," then “Download Transactions”
    2. Choose the account and time period
    3. Choose "Spreadsheet (CSV)" under "Financial management software"
6. After you have downloaded all the transaction files you want to analyze, run the main.py file (right click -> open with Python)

## About Excludes
Excludes are any keywords that you do not want to include in your analysis. For example if you add an exclude "Internet Banking INTERNET TRANSFER", all the transactions with transaction descriptions that include the words "Internet Banking INTERNET TRANSFER" will not be considered during analysis.
### Recommended Excludes
"Internet Banking INTERNET TRANSFER" for internet transfers (eg. transferring money from chequing to savings account)
"Electronic Funds Transfer GIC Short-Term GIC" for transfer of GIC funds from GIC account to chequing account
"Branch Transaction CREDIT MEMO" for transferring money internationally
"PAYMENT THANK YOU/PAIEMEN T MERCI" and "PRE-AUTHORIZED PAYMENT - THANK YOU" for payment of credit cards
"Branch Transaction DEBIT MEMO"
"Branch Transaction CREDIT MEMO"
"Electronic Funds Transfer PREAUTHORIZED DEBIT CIBC CARD PRODUCTS DIVISION"
