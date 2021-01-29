
owncall = 'af7xj'
owncat = '1h'
ownsec = 'id'
powermult = 4 #>100w = 1x, <100w = 2x, QRP = 4x
year = '2021'
month = '01'


qsocount = {'CW':0,
            'PH':0,
            'DI':0}

multiplier = set()

bands = {'160m':[1.8, 2],
    '80m':[3.5, 4],
    '40m':[7, 7.3],
    '20m':[14, 14.35],
    '15m':[21, 21.45],
    '12m':[24.89, 24.99],
    '10m':[28, 29.7],
    '2m':[144, 148],
    '70cm':[420, 450]
         }

def findband(freq):
    khz = freq / 1000
    qsoband = 'OOB'
    for currentband in bands.keys():
        if khz >= bands[currentband][0] and khz <= bands[currentband][1]:
            qsoband = currentband
    return qsoband

def padspace(tstring,tlength):
    padding = ''
    if tlength-len(str(tstring)) > 0:
        for rep in range(tlength-len(str(tstring))):
            padding += ' '
    else:
        padding = ' '
    return padding


def getdate(date):
    status = False
    while not status:
        status = True
        ndate = input(f'Enter date for {year}-{month}-DD [{year}-{month}-{date}]: ')
        if ndate == '':
            ndate = date
        elif not ndate.isnumeric():
            status = False
            print('Date must be a number')
        elif len(ndate) != 2:
            status = False
            print('Date must be two digits in length')
        if status:
            return ndate

def gettime():
    status = False
    while not status:
        status = True
        time = input(f'Enter time in UTC as HHMM: ')
        if not time.isnumeric():
            status = False
            print('Time must be numeric')
        if len(time) != 4:
            status = False
            print('Time must be four digits')
        if status:
            return time

def getfreq():
    status = False
    while not status:
        status = True
        freq = input('Enter freq: ')
        if freq.isdigit():
            return int(freq)
        else:
            print('Frequency should be reported as a whole number rounded to the nearest in kilohertz')
            status = False

def getmode():
    status = False
    while not status:
        status = True
        mode = input('Enter mode; [1] - Phone, 2 - Digital, 3 - CW: ')
        if mode == '':
            mode = '1'
        if mode.isdigit() and mode in ['1','2','3']:
            if mode == '1':
                return 'PH'
            if mode == '2':
                return 'DI'
            if mode == '3':
                return 'CW'
        else:
            print('Mode must be either "1", "2", or "3"')
            status = False

def gettargetcall():
    status = False
    while not status:
        status = True
        targetcall = input('Enter contact callsign: ')
        if targetcall != '':
            return targetcall
        else:
            status = False

def gettargetcategory():
    status = False
    while not status:
        status = True
        targetcategory = input('Enter contact category: ')
        if targetcategory != '':
            return targetcategory
        else:
            status = False

def gettargetsection():
    status = False
    while not status:
        status = True
        targetsection = input('Enter contact section: ')
        if targetsection != '':
            return targetsection
        else:
            status = False

def printrecord(freq,mode,totaldate,time,owncall,owncat,ownsec,tcall,tcat,tsec):
    print(f'QSO: {freq}{padspace(freq,7)}{mode.upper()}{padspace(mode,3)}{totaldate}{padspace(totaldate,11)}{time}{padspace(time,5)}{owncall.upper()}{padspace(owncall,8)}{owncat.upper()}{padspace(owncat,4)}{ownsec.upper()}{padspace(ownsec,4)}{tcall.upper()}{padspace(tcall,8)}{tcat.upper()}{padspace(tcat,4)}{tsec.upper()}\n')

def inputoption():
    status = False
    while not status:
        status = True
        i = input("Options [W]rite (default), [D]iscard, [Q]uit, [WQ] Writes and Quits: ")
        if i == '':
            i = 'w'
        i = i.lower()
        if i not in ['w','d','q', 'wq']:
            status = False
            print("Options allowed are W, D, Q, WQ")
        else:
            return i

def writerecord(freq,mode,totaldate,time,owncall,owncat,ownsec,tcall,tcat,tsec):
    file = open(f'{owncall}-{year}.log', "a")
    file.write(f'QSO: {freq}{padspace(freq,7)}{mode.upper()}{padspace(mode,3)}{totaldate}{padspace(totaldate,11)}{time}{padspace(time,5)}{owncall.upper()}{padspace(owncall,8)}{owncat.upper()}{padspace(owncat,4)}{ownsec.upper()}{padspace(ownsec,4)}{tcall.upper()}{padspace(tcall,8)}{tcat.upper()}{padspace(tcat,4)}{tsec.upper()}\n')
    file.close

if __name__ == '__main__':
    stat = 'd'
    date = ''
    while stat != 'q':
        freq = getfreq()
        mode = getmode()
        date = getdate(date)
        totaldate = year+"-"+month+"-"+date
        time = gettime()
        tcall = gettargetcall()
        tcat = gettargetcategory()
        tsec = gettargetsection()
        print('')
        printrecord(freq, mode, totaldate, time, owncall, owncat, ownsec, tcall, tcat, tsec)
        if findband(freq) == 'OOB':
            print(f'Warning - freq {freq} appears out of band')
        stat = inputoption()
        if stat == 'w':
            writerecord(freq, mode, totaldate, time, owncall, owncat, ownsec, tcall, tcat, tsec)
            print("Record written\n")
            multiplier.add(f'{findband(freq)}+{mode}')
            qsocount[mode] += 1
        elif stat == 'd':
            print("Record discarded\n")
        elif stat == 'wq':
            writerecord(freq, mode, totaldate, time, owncall, owncat, ownsec, tcall, tcat, tsec)
            print("Record written, will quit\n")
            multiplier.add(f'{findband(freq)}+{mode}')
            qsocount[mode] += 1
            stat = 'q'
        elif stat == 'q':
            print("Quiting!\n")
            stat = 'q'

    totalpoints = 0
    print(f'Points before BONUS:')
    print(f'PH contacts:  {qsocount["PH"]} @ 1pt each: {qsocount["PH"]}')
    totalpoints += qsocount["PH"]
    print(f'CW contacts:  {qsocount["CW"]} @ 2pts each: {qsocount["CW"]*2}')
    totalpoints += qsocount["CW"] * 2
    print(f'DI contacts:  {qsocount["DI"]} @ 2pts each: {qsocount["DI"]*2}')
    totalpoints += qsocount["DI"] * 2
    print(f'QSO Points Subtotal: {totalpoints}')
    print(f'Power Multiplier = {powermult}')
    totalpoints *= powermult
    print(f'Power Multiplier Subtotal: {totalpoints}')
    print(f'Bands/Modes Worked: {multiplier} for {len(multiplier)} x QSO Points {totalpoints}')
    totalpoints *= len(multiplier)
    print(f'Total Points before BONUS: {totalpoints}')
    print(f'QSOs count = {qsocount}')













