from validateInput import *
from modifyData import *
from analyzeTrans import *

def run():
    nonCreditFileNames = input('Enter non-credit accounts transactions file names seperated by "|": ').split('|')
    creditFileNames = input('Enter credit accounts transactions file names seperated by "|": ').split('|')
    fileNames = nonCreditFileNames + creditFileNames

    if len(fileNames) == 0:
        print('ERROR! No files selected')
        return

    for file in fileNames:
        try:
            open(file).close()
        except:
            print('ERROR! Invalid files selected')
            return

    creditFiles = input('\nDid you select a credit account transactions file? (y/n): ').lower()
    while creditFiles not in ['y','n']:
        print('Please enter valid input')
        creditFiles = input('\nDid you select a credit account transactions file? (y/n): ').lower()
    
    if creditFiles == 'y':
        creditFiles = input('Enter credit account transactions files names seperated by "|": ').split('|')

        if len(creditFiles) == 0:
            print('ERROR! No files selected')
            return
        
        for creditFile in creditFiles:
            if creditFile not in fileNames:
                print('ERROR! Invalid files selected')
                return
            try:
                f = open(creditFile)
                f.close()
            except:
                print('ERROR! Invalid files selected')
                return
    
        fileNames = modifyCreditFileData(creditFiles, fileNames)

    data = getData(fileNames)

    analyze = input('\nWhat do you want to see?\nNet expenditure (expenses - earnings) -> "ne"\nTotal expenditure -> "te"\nNet expenditure of a time period -> "net"\nTotal expenditure of a time period -> "tet"\nExit -> "exit"\nEnter input: ').lower()
    while analyze not in ['ne','te','net','tet','exit']:
        print('Please enter valid input')
        analyze = input('\nWhat do you want to see?\nNet expenditure (expenses - earnings) -> "ne"\nTotal expenditure -> "te"\nNet expenditure of a time period -> "net"\nTotal expenditure of a time period -> "tet"\nExit -> "exit"\nEnter input: ').lower()

    if analyze == 'exit':
        print('Thanks for using Transactions Analyzer')
        return

    llimit = input('\nEnter lower amount limit or enter "0" to select all: ')
    while not(isValidLlimit(llimit)):
        print('Please enter valid input')
        llimit = input('\nEnter lower amount limit or enter "0" to select all: ')

    ulimit = input('\nEnter upper amount limit or enter "all" to select all: ').lower()
    while not(isValidUlimit(ulimit)):
        print('Please enter valid input')
        ulimit = input('\nEnter upper amount limit or enter "infinite" to select all: ').lower()

    exclude = input('\nEnter any transaction keywords you want to exclude seperated by "|" or leave blank to select all: ')
    while not(isValidExclude(exclude)):
        print('Please enter valid input')
        exclude = input('\nEnter any transaction keywords you want to exclude seperated by "|" or leave blank to select all: ')
    if exclude == '':
        exclude = []
    else:
        exclude = exclude.split('|')

    if analyze in ['ne','te']:
        freq = input('\nWhat frequency do you want to use?\nWeekly -> "w"\nMonthly -> "m"\nQuarterly -> "q"\nYearly -> "y"\nEnter input: ').lower()
        while freq not in ['w', 'm', 'q', 'y']:
            print('Please enter valid input')
            freq = input('\nWhat frequency do you want to use?\nWeekly -> "w"\nMonthly -> "m"\nQuarterly -> "q"\nYearly -> "y"\nEnter input: ').lower()

        start = input('\nEnter start date (YYYY-MM-DD) or enter "0" to select all: ')
        while not (isValidStartDate(start)):
            print('Please enter valid input')
            start = input('\nEnter start date (YYYY-MM-DD) or enter "0" to select all: ')

        end = input('\nEnter end date (YYYY-MM-DD) or enter "9" to select all: ')
        while not (isValidEndDate(end)):
            print('Please enter valid input')
            end = input('\nEnter end date (YYYY-MM-DD) or enter "0" to select all: ')

        order = input('\nEnter order of accuracy between 1 and 4: ')
        while order not in ['1','2','3','4']:
            print('Please enter valid input')
            order = input('\nEnter order of accuracy (1-4): ')

        pred = input('\nHow many predictions do you want to see? (1-4): ')
        while pred not in ['1','2','3','4']:
            print('Please enter valid input')
            pred = input('\nHow many predictions do you want to see? (1-4): ')

    else:
        freq = input('\nWhat time period do you want to use?\n1 Week -> "w"\n1 Monthly -> "m"\n1 Quarter -> "q"\n1 Year -> "y"\nEnter input: ').lower()
        while freq not in ['w', 'm', 'q', 'y']:
            print('Please enter valid input')
            freq = input('\nWhat time period do you want to use?\n1 Week -> "w"\n1 Monthly -> "m"\n1 Quarter -> "q"\n1 Year -> "y"\nEnter input: ').lower()

        freqYear = input('\nEnter year: ')
        while not(isValidYear(freqYear)):
            print('Please enter valid input')
            freqYear = input('\nEnter year: ')

        if freq != 'year':
            freqNum = input('Enter ' + freqMap[freq].replace('Value', '') + ' number: ')
        else:
            freqNum = freqYear

    if analyze == 'ne':
        netExp(data, freq, start, end, int(llimit), ulimit, exclude, int(order), int(pred))
    elif analyze == 'te':
        exp(data, freq, start, end, int(llimit), ulimit, exclude, int(order), int(pred))
    elif analyze == 'net':
        netExpData(data, freqYear, freq, freqNum, int(llimit), ulimit, exclude)
    else:
        expData(data, freqYear, freq, freqNum, int(llimit), ulimit, exclude)

run()
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