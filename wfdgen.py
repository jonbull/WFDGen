debug = 1
theFile = 'af7xj2024.csv'

if debug == 1:
    theFile = 'debug.csv'

class qso:
    def __init__(self):

        self.owncall = 'af7xj'
        self.owncat = '1o'
        self.ownsec = 'id'
        self.year = '2024'
        self.month = '01'
        self.isQRP = 1

        self.bands = {'160m': [1800, 2000],
                 '80m': [3500, 4000],
                 '40m': [7000, 7300],
                 '20m': [14000, 14350],
                 '15m': [21000, 21450],
                 '10m': [28000, 29700],
                 '2m': [144, 148],
                 '70cm': [420, 450]
                 }

        self.sections = ["CO","IA","KS","MN","MO","ND","NE","SD","CT","EMA","ME","NH","RI","VT","WMA","ENY","NLI","NNJ","NNY","SNJ","WNY","DE","EPA","MDC","WPA","AL","GA","KY","NC","NFL","PR","SC","SFL","TN","VA","VI","WCF","AR","LA","MS","NM","NTX","OK","STX","WTX","EB","LAX","ORG","PAC","SB","SCV","SDG","SF","SJV","SV","AK","AZ","EWA","ID","MT","NV","OR","UT","WWA","WY","MI","OH","WV","IL","IN","WI","AB","BC","GH","MB","NB","NL","NS","ONE","ONN","ONS","PE","QC","SK","TER"]

        self.classification = ["I","O","M","H"]

        self.contactTypes = ["PH","CW","DG"]

        self.qsoCount = {'CW': 0,
                    'PH': 0,
                    'DG': 0}

        self.multiplier = set()

        self.errorBlob = {}
        self.qsoList = []

    def addErrorLog(self,key,message):
        #IF the key is not in the dictionary add the key and message
        if key in self.errorBlob.keys():
            self.errorBlob[key].append(message)
        else:
            self.errorBlob[key] = [message]

    """
    valdiate column counts per row, discard rows that are over under and add them to the log blob
    """
    def validateQsoList(self, rawList):
        for line in range(len(rawList)):
            if len(rawList[line]) > 7:
                self.addErrorLog((line + 1),"More than 7 Elements.")
            elif len(rawList[line]) < 7:
                self.addErrorLog((line + 1), "Less than 7 Elements.")
            self.qsoList.append(rawList[line])

    """
    Find Band is used for determining band multiplier and testing for OOB elements
    """
    def findBand(self, freq):
        qsoband = 'OOB'
        for currentband in self.bands.keys():
            if freq >= self.bands[currentband][0] and freq <= self.bands[currentband][1]:
                qsoband = currentband
        return qsoband

    """
    validate freq
    """
    def validateFreq(self):
        for line in range(len(self.qsoList)):
            if len(self.qsoList[line]) >= 1:
                if (wfdEntry.findBand(int(self.qsoList[line][0])) == "OOB"):
                    self.addErrorLog((line + 1), "May be OOB.")

    """
    Validate class
    """
    def validateClass(self):
        for line in range(len(self.qsoList)):
            if len(self.qsoList[line]) >= 3:
                if (self.classification.count(self.qsoList[line][2][-1].upper()) == 0):
                    self.addErrorLog((line + 1), "Bad class")

    """
    validate section
    """
    def validateSection(self):
        for line in range(len(self.qsoList)):
            if len(self.qsoList[line]) >= 4:
                if (self.sections.count(self.qsoList[line][3].upper()) == 0):
                    self.addErrorLog((line + 1), "Bad section.")

    """
    validate contact type
    """
    def validateContact(self):
        for line in range(len(self.qsoList)):
            if len(self.qsoList[line]) >= 6:
                if (self.contactTypes.count(self.qsoList[line][5].upper()) == 0):
                    self.addErrorLog((line + 1), "Bad contact type.")

    """
    validate time
    """
    def validateTime(self):
        for line in range(len(self.qsoList)):
            if len(self.qsoList[line]) >= 5:
                if ((int(self.qsoList[line][4]) > 2400) or (int(self.qsoList[line][4]) < 0)):
                    self.addErrorLog((line + 1), "Bad time.")

    """
    validate date
    """
    def validateDate(self):
        for line in range(len(self.qsoList)):
            if len(self.qsoList[line]) >= 7:
                if ((int(self.qsoList[line][6]) > 31) or (int(self.qsoList[line][6]) < 1)):
                    self.addErrorLog((line + 1), "Bad date.")

    """
    score log
    """
    def genScore(self):
        for line in range(len(self.qsoList)):
            if line+1 not in self.errorBlob.keys():
                self.qsoCount[self.qsoList[line][5].upper()]+=1
                self.multiplier.add(f'{self.findBand(int(self.qsoList[line][0]))}+{self.qsoList[line][5]}')

        totalPoints = 0
        print("\nMode: Contacts -> Points")
        for mode in self.qsoCount.keys():
            print(mode+": "+str(self.qsoCount[mode]),end='')
            if mode in ["CW","DG"]:
                print(" -> "+str(2*self.qsoCount[mode]))
                totalPoints += 2*self.qsoCount[mode]
            else:
                print(" -> " + str(self.qsoCount[mode]))
                totalPoints += self.qsoCount[mode]
        temp = 0
        for mode in self.qsoCount.keys():
            temp += self.qsoCount[mode]
        print ("Numbers of QSO: "+str(temp))
        print ("QSO Points: "+str(totalPoints)+"\n")

        print("Multipliers = "+str(self.multiplier))
        print("Multiplier Count = "+str(len(self.multiplier)))
        print("QSO Points * Multiplier Count = Total")
        print(str(totalPoints)+" * "+str(len(self.multiplier))+" = "+str(totalPoints*len(self.multiplier))+"\n")
        totalPoints = totalPoints * len(self.multiplier)
        if self.isQRP == 1:
            print("QRP Bonus * 2")
            print(str(totalPoints)+" * 2 = "+str(totalPoints*2)+"\n")
            totalPoints = totalPoints * 2

        print("##############################")
        print("Total Points = "+str(totalPoints))
        print("##############################")

    def padspace(self, tstring, tlength):
        padding = ''
        if tlength - len(str(tstring)) > 0:
            for rep in range(tlength - len(str(tstring))):
                padding += ' '
        else:
            padding = ' '
        return padding
    def writerecord(self, freq, mode, totaldate, time, owncall, owncat, ownsec, tcall, tcat, tsec):
        file = open(f'{self.owncall}-{self.year}.log', "a")
        file.write(
            f'QSO: {freq}{self.padspace(freq, 7)}{mode.upper()}{self.padspace(mode, 3)}{totaldate}{self.padspace(totaldate, 11)}{time}{self.padspace(time, 5)}{owncall.upper()}{self.padspace(owncall, 8)}{owncat.upper()}{self.padspace(owncat, 4)}{ownsec.upper()}{self.padspace(ownsec, 4)}{tcall.upper()}{self.padspace(tcall, 8)}{tcat.upper()}{self.padspace(tcat, 4)}{tsec.upper()}\n')
        file.close

    def generateLog(self):
        for line in range(len(self.qsoList)):
            if line+1 not in self.errorBlob.keys():
                self.writerecord(self.qsoList[line][0], self.qsoList[line][5], self.year+"-"+self.month+"-"+self.qsoList[line][6], self.qsoList[line][4], self.owncall, self.owncat, self.ownsec, self.qsoList[line][1], self.qsoList[line][2], self.qsoList[line][3])

    def errorLog(self):
        for thiskey in self.errorBlob.keys():
            print("Line "+str(thiskey)+":")
            for report in self.errorBlob[thiskey]:
                print (report)

"""
read in a csv of QSO data
"""
masterList = []

theCSV = open(theFile)
for line in theCSV:
    masterList.append(line.rstrip().split(","))

wfdEntry = qso()
wfdEntry.validateQsoList(masterList)
wfdEntry.validateFreq()
wfdEntry.validateClass()
wfdEntry.validateSection()
wfdEntry.validateContact()
wfdEntry.validateTime()
wfdEntry.validateDate()
wfdEntry.genScore()
wfdEntry.generateLog()
wfdEntry.errorLog()