# Table of Contents
1. [Project Title](README.md#project-title)
2. [Introduction](README.md#introduction)
3. [Challenge Link ](README.md#challenge-link)
4. [Prerequisites ](README.md#prerequisites)
5. [Input Output Files ](README.md#input-output-files)
6. [Source Files](README.md#source-files)
7. [Assumptions and Preffered Actions](README.md#source-files)
8. [Algorithm and Data Structures](README.md#algorithm-data-structures)
9. [Test Cases](README.md#test-cases)
10. [How to test](README.md#how-to-test)
11. [Example](README.md#example)
12. [Repo directory structure](README.md#Repo-directory-structure)
13. [Contact](README.md#contact)









# Project Title

Insight Data Engineering Challenge: EDGAR

# Introduction

Many investors, researchers, journalists and others use the Securities and Exchange Commission's Electronic Data Gathering, Analysis and Retrieval (EDGAR) system to retrieve financial documents, whether they are doing a deep dive into a particular company's financials or learning new information that a company has revealed through their filings. 

Data engineer's job is to build a pipeline to ingest that stream of data and calculate how long a particular user spends on EDGAR during a visit and how many documents that user requests during the session. 

# Challenge Link

For more details see the challenge page

https://github.com/InsightDataScience/edgar-analytics

# Prerequisites

I developed and tested in Python 3.6.3
I am importing two Python modules:
- import datetime
- import sys

#  Input Output Files

My program expects two input files (See the section, "Repo directory structure", for details on where these files should be located):

* `log.csv`: EDGAR weblog data
* `inactivity_period.txt`: Holds a single value denoting the period of inactivity that should be used to identify when a user session is over

It creates one output file:
* `sessionization.txt`


#Source Files

sessionization.py
my_functions_classes.py


# Assumptions and Preffered Actions

Some assumptions and preferred actions in case of errors in the input files:

- Due to some potential errors in the data file, some rows might not have the right format. In these cases, I will print out a warning to the screen and opt to skip that row.
- Some foreseen errors:
- rows might not be in chronological order
- rows might have missing values
- Missing input files: Warning to the user
- Empty input files


- I also assume a simple time zone as we are told not to care about the time zone field.

- If in?? is less than 1, I will set it to 1.
- If in?? is greater than max , I will set it to max.

- output file to be written every so many lines maybe 

cik 
accession 
extention


('Skipped Row - Chronological Error:',row_str)
print('Skipped Row - date/time format error:',row_str) 
('Skipped Row - Missing field:',row_str)


# Algorithm and Data Structures

Needed data structures
I need the following data structures:
ActiveSessions: A dictionary for keeping active sessions where the keys are IDs
Each element in ActiveSessions is a Session object
A Session object has the following attributes:
- moment of the first request FR
- moment of the last request
- request counter
- line number
- session duration
- sort method __lt__
- ID
- print method __str__
FinishedSession: This is a list of Sessions that are just popped from the ActiveSessions. We need to sort the items in this list according to their moments and line numbers
SortedSessions: Sorted version of the FinishedSession to be written to the output file

# Test Cases



Information regarding test cases I think about. The input / output files for the test cases are within folder insight_testsuite. test_1 is the one given by the challenge

- TEST CASES
Comment about the so-called fails
'OK' means the output matches what I would expect.

1)  folder name: test_1:  Given by the challenge itself - OK
2)  folder name: test_2:  Row entries are NOT in chronological order - OK
3)  folder name: test_3:  Empty log file - OK
4)  folder name: test_4:  Header row is there but no requests
5)  folder name: test_5:  Try rows that all come at the same time - OK
6)  folder name: test_6:  Try inactivity_duration to be 1 sec. - OK PS: the result makes sense to me but insight test fails ??
7)  folder name: test_7:  Try inactivity_duration to be <= 0 sec. - OK
8)  folder name: test_8:  Try inactivity_duration to be > 86400 sec. -OK

9)  folder name: test_9:  Try with consecutive identical rows - OK
10) folder name: test_10: Try with a single request - OK
11) folder name: test_11: Try inactivity_duration to be 100 sec. - OK
12) folder name: test_12: Somewhat convoluted case of rows - OK

13) folder name: test_13: inactivity_period.txt is missing - OK
14) folder name: test_14: log.csv is missing - OK


# How to test


## Testing the directory structure and output format

Challange provided a test script called `run_tests.sh` in the `insight_testsuite` folder.

The tests are stored simply as text files under the `insight_testsuite/tests` folder. Each test have a separate folder with an `input` folder for `inactivity_period.txt` and `log.csv` and an `output` folder for `sessionization.txt`.

You can run the test with the following command from within the `insight_testsuite` folder:

insight_testsuite~$ ./run_tests.sh 

On a failed test, the output of `run_tests.sh` should look like:

[FAIL]: test_1
[Thu Mar 30 16:28:01 PDT 2017] 0 of 1 tests passed

On success:

[PASS]: test_1
[Thu Mar 30 16:25:57 PDT 2017] 1 of 1 tests passed

# Example

Suppose your input files contained only the following few lines. Note that the fields we are interested in are in **bold** below but will not be like that in the input file. There's also an extra newline between records below, but the input file won't have that.

**`inactivity_period.txt`**
> **2**

**`log.csv`**

>**ip,date,time**,zone,**cik,accession,extention**,code,size,idx,norefer,noagent,find,crawler,browser

>**101.81.133.jja,2017-06-30,00:00:00**,0.0,**1608552.0,0001047469-17-004337,-index.htm**,200.0,80251.0,1.0,0.0,0.0,9.0,0.0,

>**107.23.85.jfd,2017-06-30,00:00:00**,0.0,**1027281.0,0000898430-02-001167,-index.htm**,200.0,2825.0,1.0,0.0,0.0,10.0,0.0,

>**107.23.85.jfd,2017-06-30,00:00:00**,0.0,**1136894.0,0000905148-07-003827,-index.htm**,200.0,3021.0,1.0,0.0,0.0,10.0,0.0,

>**107.23.85.jfd,2017-06-30,00:00:01**,0.0,**841535.0,0000841535-98-000002,-index.html**,200.0,2699.0,1.0,0.0,0.0,10.0,0.0,

>**108.91.91.hbc,2017-06-30,00:00:01**,0.0,**1295391.0,0001209784-17-000052,.txt**,200.0,19884.0,0.0,0.0,0.0,10.0,0.0,

>**106.120.173.jie,2017-06-30,00:00:02**,0.0,**1470683.0,0001144204-14-046448,v385454_20fa.htm**,301.0,663.0,0.0,0.0,0.0,10.0,0.0,

>**107.178.195.aag,2017-06-30,00:00:02**,0.0,**1068124.0,0000350001-15-000854,-xbrl.zip**,404.0,784.0,0.0,0.0,0.0,10.0,1.0,

>**107.23.85.jfd,2017-06-30,00:00:03**,0.0,**842814.0,0000842814-98-000001,-index.html**,200.0,2690.0,1.0,0.0,0.0,10.0,0.0,

>**107.178.195.aag,2017-06-30,00:00:04**,0.0,**1068124.0,0000350001-15-000731,-xbrl.zip**,404.0,784.0,0.0,0.0,0.0,10.0,1.0,

>**108.91.91.hbc,2017-06-30,00:00:04**,0.0,**1618174.0,0001140361-17-026711,.txt**,301.0,674.0,0.0,0.0,0.0,10.0,0.0,

The output to this should be

101.81.133.jja,2017-06-30 00:00:00,2017-06-30 00:00:00,1,1
108.91.91.hbc,2017-06-30 00:00:01,2017-06-30 00:00:01,1,1
107.23.85.jfd,2017-06-30 00:00:00,2017-06-30 00:00:03,4,4
106.120.173.jie,2017-06-30 00:00:02,2017-06-30 00:00:02,1,1
107.178.195.aag,2017-06-30 00:00:02,2017-06-30 00:00:04,3,2
108.91.91.hbc,2017-06-30 00:00:04,2017-06-30 00:00:04,1,1


# Repo directory structure

The directory structure for this repo is like this:

    ├── README.md 
    ├── run.sh
    ├── src
    │   └── sessionization.py
    |   └── my_functions_classes.py
    ├── input
    │   └── inactivity_period.txt
    │   └── log.csv
    ├── output
    |   └── sessionization.txt
    ├── insight_testsuite
        └── run_tests.sh
        └── tests
            └── test_1
            |   ├── input
            |   │   └── inactivity_period.txt
            |   │   └── log.csv
            |   |__ output
            |   │   └── sessionization.txt
            ├── test_2
                ├── input
                │   └── my-inputs
                |── output
                    └── sessionization.txt
                .
                .
                .
                ├── test_14
                ├── input
                │   └── my-inputs
                |── output
                    └── sessionization.txt        





# Contact
<ozgun.bu@gmail.com>
