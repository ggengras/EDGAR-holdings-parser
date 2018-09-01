#!/usr/local/bin/python
# Main program

import sys
import csv
import xml.etree.ElementTree as ET
import edgar

# Get user input
input = raw_input("Enter a ticker or CIK: ").strip()

# If input isn't a CIK, convert it to a CIK
try:
    int(input)
    CIK = input
except ValueError:
    ticker = input
    CIK = edgar.tickerToCIK(ticker)

# Some cases for trouble with the CIK / Ticker
if not CIK:
    sys.exit("Couldn't find ticker")

if len(CIK) != 10:
    sys.exit("That probably isn't a CIK ...")

[form, date] = edgar.get13F(CIK) # Get the 13F & filing date
if not form:
    sys.exit("Couldn't find 13F")

root = ET.fromstring(form) # Parse XML
companyName = edgar.cikToName(CIK)

# Write table of holdings to a file, .txt because Excel likes that
filename = CIK + "_13F_" + date + ".txt"
saveFile = open(filename, 'w')

# Put some info at the top
saveFile.write("13F\t" + CIK + "\t" + companyName.replace(" ", "")
    + "\t" + date + "\n")

# Field names
fieldnames = []
for element in root[0]:
    fieldnames.append(element.tag.replace("{http://www.sec.gov/edgar/document/thirteenf/informationtable}", ""))
    for child in element:
        # Some elements have sub-elements
        fieldnames.append(child.tag.replace("{http://www.sec.gov/edgar/document/thirteenf/informationtable}", ""))
    # (Sorry for the long lines)

# Open tab-delimited CSV writing and write table headings
writer = csv.writer(saveFile, dialect='excel-tab')
writer.writerow(fieldnames)

# Iterate over XML fields ond populate table
for element in root:
    row = []
    for field in element:
        if "\n" not in field.text:
            row.append(field.text)
        else:
            row.append("")

        for subfield in field:
            if "\n" not in subfield.text:
                row.append(subfield.text)
    writer.writerow(row)

print "Most recent 13F form filed by '" + companyName + "' found and saved."
