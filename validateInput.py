import datetime as dt

def isValidStartDate(s):
    if s == '0':
        return True
    try:
        s = dt.datetime.strptime(s, '%Y-%m-%d').strftime("%Y-%m-%d")
        now = dt.datetime.now().strftime("%Y-%m-%d")
        if s > now:
            return False
        return True
    except:
        return False

def isValidEndDate(s):
    if s == '9':
        return True
    try:
        s = dt.datetime.strptime(s, '%Y-%m-%d').strftime("%Y-%m-%d")
        now = dt.datetime.now().strftime("%Y-%m-%d")
        if s > now:
            return False
        return True
    except:
        return False

def isValidLlimit(s):
    try:
        amount = float(s)
        if amount >= 0:
            return True
        return False
    except:
        return False

def isValidUlimit(s):
    if s == 'all':
        return True
    try:
        amount = float(s)
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