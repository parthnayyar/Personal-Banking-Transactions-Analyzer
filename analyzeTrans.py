import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import math

def getPredictions(coeff, freq, count):
    curDate = dt.datetime.today()
    curYear = curDate.year

    if freq == 'w':
        curWeek = curDate.isocalendar()[1]
        frequency = 52
        curVal = curYear + curWeek / frequency

    elif freq == 'm':
        curMonth = curDate.month
        frequency = 12
        curVal = curYear + curMonth / frequency

    elif freq == 'q':
        curQuarter = math.ceil(curDate.month / 3)
        frequency = 4
        curVal = curYear + curQuarter / frequency

    else:
        frequency = 1
        curVal = curYear
        pass

    predictions = []
    order = len(coeff)

    for i in range(count):
        curVal_i = curVal + i / frequency
        val = 0
        for j in range(order):
            val += coeff[j] * curVal_i ** (order - 1 - j)
        predictions.append(val)

    return predictions

freqMap = {
    'w': 'weekValue',
    'm': 'monthValue',
    'q': 'quarterValue',
    'y': 'yearValue'
}

def netExp(df, freq, start, end, llimit, ulimit, exclude, order, predict):
    if freq not in freqMap.keys():
        raise ValueError('ERROR! Specify valid frequency')

    df = df[(df['dateStr'] >= start) & (df['dateStr'] <= end) & (df['amountSpent'] >= llimit) & (df['amountEarned'] >= llimit)]
    if ulimit != 'all':
        df = df[(df['amountSpent'] <= ulimit) & (df['amountEarned'] <= ulimit)]
    for e in exclude:
        df = df[~df['transactionDescription'].str.match('.*' + e + '.*')]

    df['netExpenditure'] = df['amountSpent'] - df['amountEarned']

    netExpdf = df.groupby([freqMap[freq]]).sum(['netExpenditure'])['netExpenditure']

    t = np.array(df[freqMap[freq]].unique().tolist())
    exp = np.array(netExpdf.tolist())

    coeff = tuple(np.polyfit(t, exp, order - 1))
    fit = 0
    for i in range(order):
        fit += coeff[i] * t ** (order - 1 - i)

    predictions = getPredictions(coeff, freq, predict)
    for i in range(predict):
        if i == 0:
            print('This ' + freqMap[freq][:-5] + ' : $' + str(round(predictions[i])))
        else:
            print(freqMap[freq][:-5].capitalize() + ' ' + str(i) + ' : $' + str(round(predictions[i])))

    plt.plot(netExpdf)
    plt.plot(t, fit, c='red', ls=':')
    plt.axhline(y=0, c='black', ls='--')
    plt.xlabel('Time')
    plt.ylabel('Net Expenditure')
    plt.legend(['Expenditure', 'Best Fit'])
    plt.title(freqMap[freq][:-5].capitalize() + 'ly Net Expenditure')
    plt.show()

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