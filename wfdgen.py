# Used to find the band given a freq.  Returns "OOB" if freq is our of band.
def findBand(freq):
    # List of bands and their freq range
    bands = {'160m': [1800, 2000],
             '80m': [3500, 4000],
             '40m': [7000, 7300],
             '20m': [14000, 14350],
             '15m': [21000, 21450],
             '10m': [28000, 29700],
             '2m': [144, 148],
             '70cm': [420, 450]
             }

    results = "OOB"
    for currentband in bands.keys():
        if int(freq) >= bands[currentband][0] and int(freq) <= bands[currentband][1]:
            results = currentband
    return results

class ValidateQSO:
    def __init__(self):

        myConfig = {}
        theCSV = open("config.ini")
        for line in theCSV:
            if line[0] != '#':
                row = line.rstrip().split("=")
                myConfig[row[0]] = row[1]

        file = myConfig["file"]

        self.rawlist = []

        for line in open(file):
            self.rawlist.append(line.rstrip().split(","))

        # List of ARRL Sections
        self.sections = ["CO", "IA", "KS", "MN", "MO", "ND", "NE", "SD", "CT", "EMA", "ME", "NH", "RI", "VT", "WMA",
                         "ENY", "NLI", "NNJ", "NNY", "SNJ", "WNY", "DE", "EPA", "MDC", "WPA", "AL", "GA", "KY", "NC",
                         "NFL", "PR", "SC", "SFL", "TN", "VA", "VI", "WCF", "AR", "LA", "MS", "NM", "NTX", "OK", "STX",
                         "WTX", "EB", "LAX", "ORG", "PAC", "SB", "SCV", "SDG", "SF", "SJV", "SV", "AK", "AZ", "EWA",
                         "ID", "MT", "NV", "OR", "UT", "WWA", "WY", "MI", "OH", "WV", "IL", "IN", "WI", "AB", "BC",
                         "GH", "MB", "NB", "NL", "NS", "ONE", "ONN", "ONS", "PE", "QC", "SK", "TER"]

        # List of Winter Field Day categories
        self.category = ["I", "O", "M", "H"]

        # List of Cabrillo valid contact types/
        self.contactTypes = ["PH", "CW", "DG"]

        self.errorDict = {}
        self.validQsoList = []

    # Method to build our error log.
    # Key is the line number from the CSV
    # Message will be the reason the line may not be valid
    def adderrorlog(self, key, message):
        if key in self.errorDict.keys():  # IF the key is not in the dictionary add the key and message
            self.errorDict[key].append(message)
        else:  # ELSE just add the message
            self.errorDict[key] = [message]

    def validatelength(self, totalline):  # If we don't have 7 elements in a line, that's an error.
        if len(totalline) != 7:
            return True
        else:
            return False

    def validateclass(self, arrlClass):  # Class provided should be in the class list.
        if self.category.count(arrlClass.upper()) == 0:
            return True
        else:
            return False

    def validatesection(self, section):  # Section provided should be in the section list.
        if self.sections.count(section.upper()) == 0:
            return True
        else:
            return False

    def validatecontact(self, contacttype):  # Contact Type should be the list of accepted contact types.
        if self.contactTypes.count(contacttype.upper()) == 0:
            return True
        else:
            return False

    def validatetime(self, time):  # Time needs to be between 2400 and 0
        if (int(time) > 2400) or (int(time) < 0):
            return True
        else:
            return False

    def validate_date(self, date):  # Date should be between 1 and 31
        if (int(date) > 31) or (int(date) < 1):
            return True
        else:
            return False

    def check_line(self):  # For each line, validate the available elements
        for line in range(len(self.rawlist)):
            if self.validatelength(self.rawlist[line]):
                self.adderrorlog(line + 1, "QSO line is not 7 elements long.")
            else:
                if findBand(self.rawlist[line][0]) == "OOB":
                    self.adderrorlog(line + 1, "Check frequency, may be out of band.")
                if self.validateclass(self.rawlist[line][2][-1]):
                    self.adderrorlog(line + 1, "Check class")
                if self.validatesection(self.rawlist[line][3]):
                    self.adderrorlog(line + 1, "Check section")
                if self.validatetime(self.rawlist[line][4]):
                    self.adderrorlog(line + 1, "Check time - should be > 0000 and < 2400")
                if self.validatecontact(self.rawlist[line][5]):
                    self.adderrorlog(line + 1, "Check mode - should be PH, CW of DG")
                if self.validate_date(self.rawlist[line][6]):
                    self.adderrorlog(line + 1, "Check date - should be > 0 and < 31")

        # Go through our QSO list, if there isn't an entry in the errorDict
        # than write the row to our validQsoList
        for line in range(len(self.rawlist)):
            if line + 1 not in self.errorDict.keys():
                self.validQsoList.append(self.rawlist[line])

        return self.validQsoList

    # Print the errorDict
    def print_error_log(self):
        print("\n##########")
        print("Error Log:")
        for thiskey in self.errorDict.keys():
            print("Line " + str(thiskey) + ":")
            for report in self.errorDict[thiskey]:
                print(report)
        print("##########")

class ScoreAndLog:
    def __init__(self, goodList):

        self.goodList = goodList  # Our good QSO list

        # Dictionary to count our QSOs by type
        self.qsoCount = {'CW': 0,
                         'PH': 0,
                         'DG': 0}

        # Empty set to track our Bands+Modes for multiplier
        self.multiplier = set()

        self.myConfig = {}
        theCSV = open("config.ini")
        for line in theCSV:
            if line[0] != '#':
                row = line.rstrip().split("=")
                self.myConfig[row[0]] = row[1]

    def padspace(self, tstring, tlength):
        padding = ''
        if tlength - len(str(tstring)) > 0:
            for rep in range(tlength - len(str(tstring))):
                padding += ' '
        else:
            padding = ' '
        return padding

    def writerecord(self, freq, mode, totaldate, time, owncall, owncat, ownsec, tcall, tcat, tsec):
        file = open(f'{self.myConfig["owncall"]}-{self.myConfig["year"]}.log', "a")
        file.write(
            f'QSO: {freq}{self.padspace(freq, 7)}{mode.upper()}{self.padspace(mode, 3)}{totaldate}{self.padspace(totaldate, 11)}{time}{self.padspace(time, 5)}{owncall.upper()}{self.padspace(owncall, 8)}{owncat.upper()}{self.padspace(owncat, 4)}{ownsec.upper()}{self.padspace(ownsec, 4)}{tcall.upper()}{self.padspace(tcall, 8)}{tcat.upper()}{self.padspace(tcat, 4)}{tsec.upper()}\n')
        file.close

    def score_and_gen_log(self):
        total_points = 0

        for line in self.goodList:
            # Build QSO Count and Multiplier List
            self.qsoCount[line[5].upper()] += 1
            self.multiplier.add(f'{findBand(int(line[0]))}+{line[5]}')
            # Print out the log
            # Pad out date time string
            if len(line[4]) == 1:
                line[4] = "000" + line[4]
            if len(line[4]) < 3:
                line[4] = "00" + line[4]
            if len(line[4]) < 4:
                line[4] = "0" + line[4]
            self.writerecord(line[0], line[5], self.myConfig["year"] + "-" + self.myConfig["month"] + "-" + line[6], line[4], self.myConfig["owncall"],
                             self.myConfig["owncat"],self.myConfig["ownsec"], line[1], line[2], line[3])

        #The Scoring block
        print("\n#########################\nScore:")
        print("Mode: Contacts -> Points")

        for mode in self.qsoCount.keys():
            print(mode + ": " + str(self.qsoCount[mode]), end='')
            if mode in ["CW", "DG"]:
                print(" -> " + str(2 * self.qsoCount[mode]))
                total_points += 2 * self.qsoCount[mode]
            else:
                print(" -> " + str(self.qsoCount[mode]))
                total_points += self.qsoCount[mode]

        temp = 0
        for mode in self.qsoCount.keys():
            temp += self.qsoCount[mode]

        print("Numbers of QSO: " + str(temp))
        print("QSO Points: " + str(total_points) + "\n")
        print("Multipliers = " + str(self.multiplier))
        print("Multiplier Count = " + str(len(self.multiplier)))
        print("QSO Points * Multiplier Count = Total")
        print(str(total_points) + " * " + str(len(self.multiplier)) + " = " + str(
            total_points * len(self.multiplier)) + "\n")
        total_points = total_points * len(self.multiplier)
        if self.myConfig["isQRP"] == "1":
            print("QRP Bonus * 2")
            print(str(total_points) + " * 2 = " + str(total_points * 2) + "\n")
            total_points = total_points * 2

        print("##############################")
        print("Total Points = " + str(total_points))
        print("##############################")

        print("\nValid QSO rows have been added to "+self.myConfig["owncall"]+"-"+self.myConfig["year"]+".log")

validateMyLog = ValidateQSO()  # Create Object
validQsoList = validateMyLog.check_line()  # Validate the QSO List
validateMyLog.print_error_log() # Print error log
theScore = ScoreAndLog(validQsoList)  # Create object
theScore.score_and_gen_log()  # Generate score and output log
