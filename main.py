from validateInput import *
from modifyData import *
from analyzeTrans import *
import tkinter as tk
from tkinter import filedialog as fd

def selectNonCreditFiles():
    filetypes = (('csv files', '*.csv'),('All files', '*.*'))
    global nonCreditFileNames
    nonCreditFileNames = list(fd.askopenfilenames(title='Select files', initialdir='Z:\Coding\Projects\Manage Money', filetypes=filetypes))

def selectCreditFiles():
    filetypes = (('csv files', '*.csv'),('All files', '*.*'))
    global creditFileNames
    creditFileNames = list(fd.askopenfilenames(title='Select files', initialdir='Z:\Coding\Projects\Manage Money', filetypes=filetypes))

def addExclude():
    global excludesE
    next_row = 10 + len(excludesE)
    exclude = tk.Entry(root)
    exclude.grid(row=next_row, column=1)
    excludesE.append(exclude)

def run():
    # modifyCreditFileData(creditFileNames)
    fileNames = creditFileNames + nonCreditFileNames
    if len(fileNames) == 0:
        tk.Label(root, text='ERROR! No files selected').grid(row=12,column=0)
    for file in fileNames:
        try:
            open(file).close()
        except:
            tk.Label(root, text='ERROR! Invalid files selected').grid(row=12,column=0)
    global analyzeE
    global analyze
    analyze = {'Net expenditure trend': 'net', 'Total expenditure trend': 'tet'}[analyzeE.get()]
    global freqE
    global freq
    freq = freqE.get()
    global startE
    global start
    start = startE.get()
    global endE
    global end
    end = endE.get().lower()
    global llimitE
    global llimit
    llimit = llimitE.get()
    global ulimitE
    global ulimit
    ulimit = ulimitE.get()
    global predE
    global pred
    pred = predE.get()
    global excludesE
    global excludes
    excludes = [e.get() for e in excludesE]

    if not(isValidStartDate(start)):
        tk.Label(root, text='ERROR! Invalid start date').grid(row=12, column=0)
    elif not(isValidEndDate(end)):
        tk.Label(root, text='ERROR! Invalid end date').grid(row=12, column=0)
    elif not(isValidLlimit(llimit)):
        tk.Label(root, text='ERROR! Invalid lower limit').grid(row=12, column=0)
    elif not(isValidUlimit(ulimit)):
        tk.Label(root, text='ERROR! Invalid upper limit').grid(row=12, column=0)
    elif pred not in ['1','2','3','4','5']:
         tk.Label(root, text='ERROR! Invalid number of predictions').grid(row=12, column=0)
    elif not(isValidExclude(excludes)):
        tk.Label(root, text='ERROR! Invalid excludes added').grid(row=12, column=0)
    else:
        # print(fileNames, analyze, freq, start, end, llimit, ulimit, pred, excludes)
        data = getData(fileNames)
        if analyze == 'net':
            netExp(data, freq, start, end, int(llimit), ulimit, excludes, int(pred))

root = tk.Tk()
root.title('Select Files')

tk.Label(root, text='Open non-credit accounts transaction files: ').grid(row=0, column=0, sticky='W')
nonCreditFileNames=[]
tk.Button(root, text='Choose Files', command=selectNonCreditFiles).grid(row=0, column=1)

tk.Label(root, text='Open credit accounts transaction files: ').grid(row=1, column=0, sticky='W')
creditFileNames=[]
tk.Button(root, text='Choose Files', command=selectCreditFiles).grid(row=1, column=1)

# fileNames = nonCreditFileNames + creditFiles

tk.Label(root, text='How do you want to analyze your transactions?: ').grid(row=2, column=0, sticky='W')
analyzeE = tk.StringVar(root)
analyzeE.set('Net expenditure trend')
tk.OptionMenu(root, analyzeE, 'Net expenditure trend', 'Total expenditure trend').grid(row=2, column=1)
# analyze = {'Net expenditure trend' : 'net', 'Total expenditure trend' : 'tet'}[analyze.get()]

tk.Label(root, text='What frequency do you want to use?').grid(row=3, column=0, sticky='W')
freqE = tk.StringVar(root)
freqE.set('Weekly')
tk.OptionMenu(root, freqE, 'Weekly', 'Monthly', 'Quarterly', 'Yearly').grid(row=3, column=1)
# freq = freq.get()

tk.Label(root, text='Enter start date (YYYY-MM-DD or "0" to select all): ').grid(row=4, column=0, sticky='W')
startE = tk.Entry(root)
startE.insert(0, '0')
startE.grid(row=4, column=1)
# start=start.get()

tk.Label(root, text='Enter start date (YYYY-MM-DD or "9" to select all): ').grid(row=5, column=0, sticky='W')
endE = tk.Entry(root)
endE.insert(0, '9')
endE.grid(row=5, column=1)
# end=end.get().lower()

tk.Label(root, text='Enter lower limit (or "0" to select all): ').grid(row=6, column=0, sticky='W')
llimitE = tk.Entry(root)
llimitE.insert(0, '0')
llimitE.grid(row=6, column=1)
# llimit=llimit.get()

tk.Label(root, text='Enter upper limit (or "all" to select all): ').grid(row=7, column=0, sticky='W')
ulimitE = tk.Entry(root)
ulimitE.insert(0, 'all')
ulimitE.grid(row=7, column=1)
# ulimit=ulimit.get()

tk.Label(root, text='Enter number of predictions (1-5): ').grid(row=8, column=0, sticky='W')
predE = tk.Entry(root)
predE.insert(0, '3')
predE.grid(row=8, column=1)
# pred=pred.get()

tk.Label(root, text='Enter any terms you want to exclude: ').grid(row=9, column=0, sticky='W')
excludesE = []
tk.Button(root, text='Add exclude', command=addExclude).grid(row=9, column=1)

tk.Button(root, text='Analyze Data', command=run).grid(row=10, column=0)
tk.Button(root, text='Exit', command=root.destroy).grid(row=11, column=0)

root.mainloop()


# netExp(getData(['savings.csv','chequing.csv','credit(1).csv']), 'w', '2021-09', '9', 0, 'all',
#        ['Internet Banking INTERNET TRANSFER',
#         'Electronic Funds Transfer GIC Short-Term GIC',
#         'Branch Transaction CREDIT MEMO IBB CIBC CONESTOGA BANKING CENTRE',
#         'Branch Transaction DEBIT MEMO IBB CIBC ELECTRONIC BANKING OPERAT',
#         'Electronic Funds Transfer PREAUTHORIZED DEBIT CIBC CARD PRODUCTS DIVISION',
#         'Branch Transaction CREDIT MEMO',
#         'PAYMENT THANK YOU/PAIEMEN T MERCI',
#         'PRE-AUTHORIZED PAYMENT - THANK YOU',
#         'Automated Banking Machine US $ DEPOSIT IN CANADIAN $'], 3, 4)