#!/usr/bin/env python
from datetime import datetime
import re
import time
import subprocess

#Junk, these will not show.
JUNK = [
    'MESSAGE : STMM Sort Memory Tuning cannot be activated because the Database',
    'MESSAGE : Completed archive for log file',
    'MESSAGE : Started archive for log file',
    'Warning: Unable to read reorg policy. Error: -1',
    'Information in this record is only valid at the time when this file was',
    'DB2ADMIN.RELATIONSHIPS" to lock intent "S" was successful.',
    '.SYSCOLUMNS" to lock intent "X" was successful.',
    '.SYSCOLDIST" to lock intent "X" was successful.',
    'FUNCTION: DB2 UDB, data protection services, sqlpgadf, probe:630',
    'Maximum allowable unarchived log files reached.',
    'MESSAGE : ADM5500W  DB2 is performing lock escalation.  The total number of',
    'DATA #1 : unsigned integer, 8 bytes',
    'MESSAGE : Backup complete.',
    'MESSAGE : Starting an online incremental delta db backup.',
    'MESSAGE : Started retrieve for log file',
    'MESSAGE : Completed retrieve for log file',
    'MESSAGE : ADM10502W  Health indicator "Table Space Operational State"',
    'FUNCTION: DB2 UDB, data protection services, sqlpgadf, probe:510',
    'MESSAGE : Starting an online db backup.',
    'FUNCTION: DB2 UDB, Self tuning memory manager, stmmLog, probe:1115',
    'FUNCTION: DB2 UDB, bsu security, sqlexSlsSystemAuthenticate, probe:150',
    'FUNCTION: DB2 UDB, data management, sqldIndexCreate, probe:1',
    'FUNCTION: DB2 UDB, relation data serv, sqlrreorg_indexes, probe:600',
    'FUNCTION: DB2 UDB, data protection services, sqlpgadf, probe:630',
]

#open and name Files.
infile = open('db2diag.log')
outfile = open('db2diag_important.txt', 'w')

#Todays date, kinda messy but it works.
TODAY = datetime.today()
TODAY = TODAY.strftime("%Y %m %d")

#User Input
print "View logs from set date (YYYY MM DD), or just hit enter to view all."
userinput = raw_input("Enter Date: ")
#Bad at error checking so this is what you get.
if userinput == "":
    #If no entered data, will show it all. No records over a couple months old anyway.
    userinput = "2010 01 01"
if userinput == "today":
    userinput = TODAY

#Convert users input to a real date.
DATE = datetime.strptime(userinput, "%Y %m %d")


write = True
collector = []
for line in infile:
    #Start looking at chunks of data that start with '####-##-##'.
    if re.match(r'\d{4}-\d{2}-\d{2}', line):
        #write all the good data to output file.
        if write:
            for l in collector:
                outfile.write(l)
        write = True
        #Covert first 10 characters into a real date.
        logdate = datetime.strptime(line[:10], "%Y-%m-%d")
        #Compare if User enter date is greater than date in log.
        if DATE > logdate:
            #If entered date is more recently, do not write.
            write = False
        collector = []

    collector.append(line)
    for j in JUNK:
        #If it finds something that matches the in the JUNK list, do not write to output file.
        if re.search(j, line):
            write = False
            break

#Write the last peice of good info if ends in good.
if write:
    for l in collector:
        outfile.write(l)

#closes files.
infile.close()
outfile.close()

#Completes and waits 1 second to show completion.
print "Completed"
print "Opening parsed log..."
time.sleep(1)
text = "C:\Python27\db2diag_important.txt"
editor = r"C:\Program Files\Sublime Text 2\sublime_text.exe"
#Opens up the output file in Sublime2
subprocess.Popen("%s %s" % (editor, text))
