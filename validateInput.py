import datetime as dt

def isValidStartDate(s):
    if s == '0':
        return True
    try:
        dt.datetime.strptime(s, '%Y-%m-%d')
        return True
    except:
        return False

def isValidEndDate(s):
    if s == '9':
        return True
    try:
        dt.datetime.strptime(s, '%Y-%m-%d')
        return True
    except:
        return False

def isValidLlimit(s):
    try:
        amount = int(s)
        if amount >= 0:
            return True
        return False
    except:
        return False

def isValidUlimit(s):
    if s == 'all':
        return True
    try:
        amount = int(s)
        if amount >= 0:
            return True
        return False
    except:
        return False

def isValidExclude(L):
    for e in L:
        if e == '':
            return False
    return True

def isValidYear(s):
    try:
        return int(s) >= 0
    except:
        return False