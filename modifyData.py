import pandas as pd
import csv

def modifyCreditFileData(creditFiles):
    for creditFile in creditFiles:
        f = pd.read_csv(creditFile, names = ['A', 'B', 'C', 'D', 'E'], header = None)
        keep_col = ['A', 'B', 'C', 'D']
        new_f = f[keep_col]
        new_f.to_csv(creditFile, index = False, header = False)

def getData(fileNames):

    rows = []

    for fileName in fileNames:
        with open(fileName) as file:
            csv_reader = csv.reader(file)
            fileRows = list(csv_reader)
            for row in fileRows:
                rows.append(row)

    columns = ['dateStr', 'transactionDescription', 'amountSpent', 'amountEarned']

    df = pd.DataFrame(rows, columns=columns)

    df['date'] = pd.to_datetime(df['dateStr'], format='%Y-%m-%d')

    df['amountSpent'] = pd.to_numeric(df['amountSpent'])
    df['amountSpent'] = df['amountSpent'].fillna(0)

    df['amountEarned'] = pd.to_numeric(df['amountEarned'])
    df['amountEarned'] = df['amountEarned'].fillna(0)

    df['year'] = pd.to_numeric(pd.DatetimeIndex(df['date']).year, downcast='integer')
    df['yearValue'] = df['year']

    df['quarter'] = pd.to_numeric(pd.DatetimeIndex(df['date']).quarter, downcast='integer')
    df['quarterValue'] = df['yearValue'] + df['quarter'] / 4

    df['month'] = pd.to_numeric(pd.DatetimeIndex(df['date']).month, downcast='integer')
    df['monthValue'] = df['yearValue'] + df['month'] / 12

    df['week'] = pd.to_numeric(df['date'].dt.isocalendar().week, downcast='integer')
    df['weekValue'] = df['yearValue'] + df['week'] / 52

    df = df.sort_values('date')
    return df