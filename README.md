#WFDGen 2024
>Been slacking for a few years, Here's the big 2024 update

This program builds Cabrillo formatted log files for use with Winter Field Day.  
Winter Field Day Rules and Scoring: www.winterfieldday.com

CSV Input format:

Frequency,Callsign,Category,Section,Time,Mode,Date

14336,kd9vgv,1o,wi,1904,PH,27

The frequency for HF must be in kilohertz rounded to the nearest kilohertz. 3753 is fine, 3753.20 is not. Frequencies above 50 MHz are specified as the band. Examples: 50, 70, 144, 222, 432, 902, 1.2G, 2.3G, 3.4G, 5.7G, 10G, 24G, etc.

Time must be in UTC.
Mode must be PH, CW or DG.

Set debug = 0
Set theFile to the filename of your CSV input.
self.owncall = Your callsign
self.owncat = Your category
self.ownsec = Your section
self.year = The year
self.isQRP = 0 for no, 1 for yes

Once the output log is generated, attach the Cabrillo header information and the "END-OF-LOG: " at the end.

