Coding Challenge
Graeme Gengras, May 2018
Written using Python 2.7.14

### Background:

People can invest in mutual funds that hold many stocks and bonds. Funds list what they own every quarter, so investors can get a sense of what they are actually exposed to, e.g. a "21st Century Tactical Technology Fund" does not just own 50% AAPL and 50% GOOG. Fund holdings are listed on the SEC website, i.e. EDGAR.

### Challenge:

Write code in Python that parses fund holdings pulled from EDGAR, given a ticker or CIK.

### Example:

For this example, we will use this CIK: 0001166559
Start on this page: http://www.sec.gov/edgar/searchedgar/companysearch.html
Enter in the CIK (or ticker), and it will take you here.
Find the “13F” report documents from the ones listed. Here is a “13F-HR”.
Parse and generate tab-delimited text from the xml
Goals:

Your code should be able to use any mutual fund ticker. Try morningstar.com or lipperweb.com to find valid tickers.
Be sure to check multiple tickers, since the format of the 13F reports can differ.
Let us know your thoughts on how to deal with different formats.  

### My Solution
1. Get ticker or CIK from the user
2. If ticker, convert into CIK
3. Retrieve the most recently filed 13F-HR
4. Parse XML - make table
5. Write table to tab delimited text file

### External Dependencies
- requests
- BeautifulSoup v4

### How to Run
Run the program from the command line with `./main.py`.  It will prompt you
for either a CIK or a ticker symbol and will output a file in the main directory
upon successful completion.  The name of the file contains the CIK, '13F',
and the date that the SEC accepted the form.

### Testing
I tested the program with a number of different tickers. Many tickers I tried
either weren't recognized by the SEC's website or didn't have 13Fs on file;
I tried to catch these two cases specifically and return appropriate error messages.

Tickers that my program could handle have output saved in the `test-output` directory.
I took these text files and imported them into Excel to check the formatting.

There are still some errors that I didn't figure out the cause of, such as
what happens when you use the ticker 'OAK'

### Shortcomings
- Very minimal checking for weird / malicious input
- Not all errors are handled (response to 'OAK', for instance)
- Formatting of table does not accurately reflect sub-columns (ie. shrsOrPrnAmt should be a header with subheadings that each contain data, table is definitely readable but only if you already know this)
- The 'value' heading should probably have 'x1000' in it
- It would be nice if the program took a CIK / ticker as an argument so that you could more easily automate data retrieval and testing with a shell script
- My code could be more elegant (but isn't that always the case)
