import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import datetime as dt
import math

def getPredictions(coeff, freq, predCount):
    curDate = dt.datetime.today()
    curYear = curDate.year

    if freq == 'Weekly':
        curWeek = curDate.isocalendar()[1]
        frequency = 52
        curVal = curYear + curWeek / frequency

    elif freq == 'Monthly':
        curMonth = curDate.month
        frequency = 12
        curVal = curYear + curMonth / frequency

    elif freq == 'Quarterly':
        curQuarter = math.ceil(curDate.month / 3)
        frequency = 4
        curVal = curYear + curQuarter / frequency

    else:
        frequency = 1
        curVal = curYear
        pass

    predictions = []

    for i in range(predCount):
        curVal_i = curVal + i / frequency
        val = 0
        for j in range(3):
            val += coeff[j] * curVal_i ** (2 - j)
        predictions.append(val)

    return predictions

freqMap = {
    'Weekly': 'weekValue',
    'Monthly': 'monthValue',
    'Quarterly': 'quarterValue',
    'Yearly': 'yearValue'
}

def netExp(df, freq, start, end, llimit, ulimit, exclude, predict):

    df = df[(df['dateStr'] >= start) & (df['dateStr'] <= end) & (df['amountSpent'] >= llimit) & (df['amountEarned'] >= llimit)]
    if ulimit != 'all':
        df = df[(df['amountSpent'] <= int(ulimit)) & (df['amountEarned'] <= int(ulimit))]
    for e in exclude:
        df = df[~df['transactionDescription'].str.match('.*' + e + '.*')]

    df['netExpenditure'] = df['amountSpent'] - df['amountEarned']

    netExpdf = df.groupby([freqMap[freq]]).sum(['netExpenditure'])['netExpenditure']

    t = np.array(df[freqMap[freq]].unique().tolist())
    exp = np.array(netExpdf.tolist())

    coeff = tuple(np.polyfit(t, exp, 2))
    fit = 0
    for i in range(3):
        fit += coeff[i] * t ** (2 - i)

    predictions = getPredictions(coeff, freq, predict)
    predOut = []
    for i in range(predict):
        if i == 0:
            predOut.append('This ' + freqMap[freq][:-5] + ' : $' + str(round(predictions[i])))
        else:
            predOut.append(freqMap[freq][:-5].capitalize() + ' ' + str(i) + ' : $' + str(round(predictions[i])))

    def showPlot():
        plt.plot(netExpdf)
        plt.plot(t, fit, c='red', ls=':')
        plt.axhline(y=0, c='black', ls='--')
        plt.xlabel('Time')
        plt.ylabel('Net Expenditure')
        plt.legend(['Expenditure', 'Best Fit'])
        plt.title(freq + ' Net Expenditure')
        plt.show()

    root = tk.Tk()
    root.title('Your Predictions')
    if predict != 0:
        tk.Label(root, text='Predictions', font='Helvetica 18 bold underline').grid(row=0, column=0)
        for i in range(predict):
            tk.Label(root, text=predOut[i]).grid(row=i+1, column=0, sticky='W')
    tk.Button(root, text='Show graph', command=showPlot).grid(row=predict+1, column=0)
    tk.Button(root, text='Close', command=root.destroy).grid(row=predict+2, column=0)
    root.mainloop()


def totalExp(df, freq, start, end, llimit, ulimit, exclude, predict):

    df = df[(df['dateStr'] >= start) & (df['dateStr'] <= end) & (df['amountSpent'] >= llimit)]
    if ulimit != 'all':
        df = df[df['amountSpent'] <= int(ulimit)]
    for e in exclude:
        df = df[~df['transactionDescription'].str.match('.*' + e + '.*')]

    totalExpdf = df.groupby([freqMap[freq]]).sum(['amountSpent'])['amountSpent']

    t = np.array(df[freqMap[freq]].unique().tolist())
    exp = np.array(totalExpdf.tolist())

    coeff = tuple(np.polyfit(t, exp, 2))
    fit = 0
    for i in range(3):
        fit += coeff[i] * t ** (2 - i)

    predictions = getPredictions(coeff, freq, predict)
    predOut = []
    for i in range(predict):
        if i == 0:
            predOut.append('This ' + freqMap[freq][:-5] + ' : $' + str(round(predictions[i])))
        else:
            predOut.append(freqMap[freq][:-5].capitalize() + ' ' + str(i) + ' : $' + str(round(predictions[i])))

    def showPlot():
        plt.plot(totalExpdf)
        plt.plot(t, fit, c='red', ls=':')
        plt.axhline(y=0, c='black', ls='--')
        plt.xlabel('Time')
        plt.ylabel('Total Expenditure')
        plt.legend(['Expenditure', 'Best Fit'])
        plt.title(freq + ' Total Expenditure')
        plt.show()

    root = tk.Tk()
    root.title('Your Predictions')
    if predict != 0:
        tk.Label(root, text='Predictions', font='Helvetica 18 bold underline').grid(row=0, column=0)
        for i in range(predict):
            tk.Label(root, text=predOut[i]).grid(row=i+1, column=0, sticky='W')
    tk.Button(root, text='Show graph', command=showPlot).grid(row=predict+1, column=0)
    tk.Button(root, text='Close', command=root.destroy).grid(row=predict+2, column=0)
    root.mainloop()



def netExpData(df, year, freq, freqNum, llimit, ulimit, exclude):
    df = df[(df['year'] == int(year)) &
            (df[freqMap[freq].replace('Value', '')] == int(freqNum)) &
            (df['amountSpent'] >= llimit) &
            (df['amountEarned'] >= llimit)]
    if ulimit != 'all':
        df = df[(df['amountSpent'] <= int(ulimit)) &
                (df['amountEarned'] <= int(ulimit))]
    print(df)
    for e in exclude:
        e = '.*' + e + '.*'
        df = df[not(df['transactionDescription'].str.match(e))]
    print('This ' + freqMap[freq].replace('Value', '') + "'s net expenditure:",round(df['amountSpent'].sum() - df['amountEarned'].sum()))

def expData(df, year, freq, freqNum, llimit, ulimit, exclude):
    df = df[(df['year'] == int(year)) &
            (df[freqMap[freq].replace('Value', '')] == int(freqNum)) &
            (df['amountSpent'] >= llimit)]
    if ulimit != 'all':
        df = df[(df['amountSpent'] <= int(ulimit))]
    for e in exclude:
        e = '.*' + e + '.*'
        df = df[not(df['transactionDescription'].str.match(e))]
    print('This ' + freqMap[freq].replace('Value', '') + "'s total expenditure:", round(df['amountSpent'].sum()))