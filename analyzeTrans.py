import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import datetime as dt
import math
from scipy.signal import find_peaks
from matplotlib.widgets import Cursor

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
frequencyMap = {
    'Weekly': 52,
    'Monthly': 12,
    'Quarterly': 4,
    'Yearly': 1
}

def netExp(df, freq, start, end, llimit, ulimit, exclude, predict):
    df = df[(df['dateStr'] >= start) & (df['dateStr'] <= end) & ((df['amountSpent'] + df['amountEarned']) >= llimit)]
    if ulimit != 'all':
        df = df[(df['amountSpent'] <= float(ulimit)) & (df['amountEarned'] <= float(ulimit))]
    for e in exclude:
        df = df[~df['transactionDescription'].str.match('.*' + e + '.*')]

    df['netExpenditure'] = round(df['amountSpent'] - df['amountEarned'], 2)

    netExpS = round(df.groupby([freqMap[freq]]).sum(['netExpenditure'])['netExpenditure'], 2)

    t = np.array(df[freqMap[freq]].unique().tolist())
    exp = np.array(netExpS.tolist())

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

        fig = plt.figure()
        fig.canvas.set_window_title(freq+" Transactions")
        ax = fig.subplots()
        ax.plot(netExpS)
        ax.plot(t, fit, c='red', ls=':')

        peaks, _ = find_peaks(netExpS, prominence=1)
        ax.plot(netExpS.iloc[peaks], 'ob')

        valleys, _ = find_peaks(-netExpS, prominence=1)
        ax.plot(netExpS.iloc[valleys], 'or')

        ax.grid()

        cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, c='green')
        annot = ax.annotate(text="", xy=(0,0), xytext=(0,0), textcoords='offset points',
                            bbox={'boxstyle':'round4', 'fc':'linen', 'ec':'k', 'lw':1})

        def onClick(event):
            x = event.xdata
            year = math.floor(float(x))
            if freq != 'Yearly':
                freqNum = round((float(x) - year) * frequencyMap[freq])
                if freqNum == 0:
                    year -= 1
                    freqNum = frequencyMap[freq]
                x = round(year + freqNum / frequencyMap[freq], 3)
                netExpVal = str(netExpS[x])
                y = float(netExpVal)
                if netExpVal[0] == '-':
                    netExpVal = netExpVal[1:]
                    annot.set_text('Year: ' + str(year) + '\n' + freq[:-2] + ': ' + str(freqNum) + '\nNet Expenditure: -$' + netExpVal)
                else:
                    annot.set_text('Year: ' + str(year) + '\n' + freq[:-2] + ': ' + str(freqNum) + '\nNet Expenditure: $' + netExpVal)
            else:
                x = year
                netExpVal = str(netExpS[x])
                y = float(netExpVal)
                if netExpVal[0] == '-':
                    netExpVal = netExpVal[1:]
                    annot.set_text('Year: ' + str(year) + '\nNet Expenditure: -$' + netExpVal)
                else:
                    annot.set_text('Year: ' + str(year) + '\nNet Expenditure: $' + netExpVal)
            annot.xy = (x, y)
            fig.canvas.draw()
        fig.canvas.mpl_connect('button_press_event', onClick)

        ax.legend(['Expenditure', 'Trend'])
        ax.axhline(y=0, color='black', ls='--')
        plt.xlabel('Time')
        plt.ylabel('Net Expenditure')
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
        df = df[df['amountSpent'] <= float(ulimit)]
    for e in exclude:
        df = df[~df['transactionDescription'].str.match('.*' + e + '.*')]

    totalExpS = round(df.groupby([freqMap[freq]]).sum(['amountSpent'])['amountSpent'], 2)

    t = np.array(df[freqMap[freq]].unique().tolist())
    exp = np.array(totalExpS.tolist())

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

        fig = plt.figure()
        ax = fig.subplots()
        ax.plot(totalExpS)
        ax.plot(t, fit, c='red', ls=':')

        peaks, _ = find_peaks(totalExpS, prominence=1)
        ax.plot(totalExpS.iloc[peaks], 'ob')

        valleys, _ = find_peaks(-totalExpS, prominence=1)
        ax.plot(totalExpS.iloc[valleys], 'or')

        ax.grid()

        cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, c='green')
        annot = ax.annotate(text="", xy=(0, 0), xytext=(0, 0), textcoords='offset points',
                            bbox={
                                'boxstyle': 'round4',
                                'fc': 'linen',
                                'ec': 'k',
                                'lw': 1
                            },
                            arrowprops={
                                'arrowstyle': '-|>'
                            })

        def onClick(event):
            x = event.xdata
            year = math.floor(float(x))
            if freq != 'Yearly':
                freqNum = round((float(x) - year) * frequencyMap[freq])
                if freqNum == 0:
                    year -= 1
                    freqNum = frequencyMap[freq]
                x = round(year + freqNum / frequencyMap[freq], 3)
                totalExpVal = str(totalExpS[x])
                y = float(totalExpVal)
                if totalExpVal[0] == '-':
                    totalExpVal = totalExpVal[1:]
                    annot.set_text('Year: ' + str(year) + '\n' + freq[:-2] + ': ' + str(
                        freqNum) + '\nTotal Expenditure: -$' + totalExpVal)
                else:
                    annot.set_text('Year: ' + str(year) + '\n' + freq[:-2] + ': ' + str(
                        freqNum) + '\nTotal Expenditure: $' + totalExpVal)
            else:
                x = year
                totalExpVal = str(totalExpS[x])
                y = float(totalExpVal)
                if totalExpVal[0] == '-':
                    totalExpVal = totalExpVal[1:]
                    annot.set_text('Year: ' + str(year) + '\nTotal Expenditure: -$' + totalExpVal)
                else:
                    annot.set_text('Year: ' + str(year) + '\nTotal Expenditure: $' + totalExpVal)
            annot.xy = (x, y)
            fig.canvas.draw()

        fig.canvas.mpl_connect('button_press_event', onClick)

        ax.legend(['Expenditure', 'Trend'])
        ax.axhline(y=0, color='black', ls='--')
        plt.xlabel('Time')
        plt.ylabel('Total Expenditure')
        plt.title(freq + ' Total Expenditure')
        plt.show()

    root = tk.Tk()
    root.title('Your Predictions')
    if predict != 0:
        tk.Label(root, text='Predictions', font='Helvetica 18 bold underline').grid(row=0, column=0)
        for i in range(predict):
            tk.Label(root, text=predOut[i]).grid(row=i + 1, column=0, sticky='W')
    tk.Button(root, text='Show graph', command=showPlot).grid(row=predict + 1, column=0)
    tk.Button(root, text='Close', command=root.destroy).grid(row=predict + 2, column=0)
    root.mainloop()