_WFDGen 2024_

This program builds Cabrillo formatted log files for use with Winter Field Day.  
Winter Field Day Rules and Scoring: www.winterfieldday.com

__CSV Input format__

Frequency,Callsign,Category,Section,Time,Mode,Date
>14336,kd9vgv,1o,wi,1904,PH,27

- The frequency for HF must be in kilohertz rounded to the nearest kilohertz. 3753 is fine, 3753.20 is not. Frequencies above 50 MHz are specified as the band. Examples: 50, 70, 144, 222, 432, 902, 1.2G, 2.3G, 3.4G, 5.7G, 10G, 24G, etc.
- Time must be in UTC. Exmaple: 0945
- Mode must be PH, CW or DG.

__config.ini__

-No spaces between key, equals sign and value.  (Example file=myfile.csv)

file = Set theFile to the filename of your CSV input  
owncall = Your callsign  
owncat = Your category  
ownsec = Your section  
year = The year  
month = The month  
isQRP = 0 for no, 1 for yes  

Once the output log is generated, attach the Cabrillo header information and the "END-OF-LOG: " at the end.

