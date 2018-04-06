
"""
Created on Thu Apr  5 12:56:57 2018

@author: bursaliogluozgun
"""
def main():
    print('This file has necessary functions and class definitions for sessionization.py')
    print('list of functions and class: ')
    print(""" def reading_row(row_str):\n
        def strip_date_time(date_str,time_str):\n
        def strip_date_time(date_str,time_str):\n
        def write_to_output_file(SortedSessions,fo):\n
        def pop_expired(ActiveSessions,current_moment,inactivity_duration,pop_all=False):\n
        def embed_last_entry_to_ActiveSessions(ActiveSessions,ip_str,moment,line_number):\n
        def clean_expired_sessions(ActiveSessions,current_moment,inactivity_duration,fo,pop_all=False):\n
        def Input_Output_file_operations(inactivity_filename,output_filename,log_filename):\n
        class Session(object):\n""")

import datetime

#==================================================================================================================
#==================================================================================================================
# FUNCTIONS
#______________________________________________________________________________________________________________________
def reading_row(row_str):
    """
    input: string of the corresponding row
    output: dictionary with keys ip, date, time. These are the only things we need from a row.
    
    For the purposes of this challenge, below are the data fields you'll want to pay attention to from the SEC weblogs:

    ip: identifies the IP address of the device requesting the data. While the SEC anonymizes the last three digits, it uses a consistent formula that allows you to assume that any two ip fields with the duplicate values are referring to the same IP address
    date: date of the request (yyyy-mm-dd)
    time: time of the request (hh:mm:ss)
    cik: SEC Central Index Key
    accession: SEC document accession number
    extention: Value that helps determine the document being requested
    
    """
    words = row_str.split(',')
    ip = words[0]
    date = words[1] # yyyy-mm-dd  TODO: we can check the format of this for each row
    time = words[2]  # hh:mm:ss   TODO: we can check the format of this for each row
   # zone = words[3] #not useful
    #cik = words[4] # any request (not necessarily unique) is counted as one, so I conclude that we do not need these fields
    #accession = words[5] # any request (not necessarily unique) is counted as one, so I conclude that we do not need these fields
    #extention = words[6] # any request (not necessarily unique) is counted as one, so I conclude that we do not need these fields
    #code = words[7] #not useful
    #size = words[8] #not useful
    #idx = words[9] #not useful
    #norefer = words[10] #not useful
    #noagent = words[11] #not useful
    #find = words[12] #not useful
    #crawler = words[13] #not useful
    #browser = words[14] #not useful
    #print(' ip: {}\n date: {}\n time: {}\n zone: {}\n cik: {}\n accession: {}\n extention: {}\n code: {}\n size: {}\n idx: {}\n norefer: {}\n noagent: {}\n find: {}\n crawler: {}\n browser: {}\n'.format(*words))

#For the purposes of this challenge, you can assume the combination of 
#cik, accession and extention fields uniquely identifies a single web page document request.
    #aRequest = cik+accession+extention # any request (not necessarily unique) is counted as one, so I conclude that we do not need these fields
    
    #row = (ip,date,time,aRequest)
    row = {'ip':ip,'date':date,'time':time} #,'aRequest':aRequest}
    return row

#______________________________________________________________________________________________________________________
def strip_date_time(date_str,time_str):
    
    """
    input: date and time strings from the row
    output: create a datetime object (moment) and also a list repressentation (as_a_list)
    source: https://docs.python.org/2/library/datetime.html
    https://stackoverflow.com/questions/1345827/how-do-i-find-the-time-difference-between-two-datetime-objects-in-python
    
    sample input format: date_str = '2017-06-30' time_str = '00:00:01'
    
    """
    skip_row = False
    moment = None
    as_a_list = None
    try:
        parts = date_str.split('-')
        as_a_list = []
        for part in parts:
            as_a_list.append(int(part))
   
        parts = time_str.split(':')
        for part in parts:
            as_a_list.append(int(part))
    
        moment = datetime.datetime(*as_a_list)
        
    except:
        print('Bad formatted date / time, skipping the row')
        skip_row = True
        

    return moment,skip_row,as_a_list

#______________________________________________________________________________________________________________________    
def write_to_output_file(SortedSessions,fo):
    """
    input: SortedSessions (List of sessions), fo (output file)
    task: writing to the output file
    """
    
    for item in SortedSessions:
        fo.write((item.__str__())+'\n')
        print(item)

#______________________________________________________________________________________________________________________
def pop_expired(ActiveSessions,current_moment,inactivity_duration,pop_all=False):
    """
    input:ActiveSessions(dictionary of sessions),current_moment (datetime),inactivity_duration (int),pop_all(bool)
     pop_all: when this is True, all of the elements in the ActiveSessions dictionary are popped regardless of time.
     We use this for the end of the log file. 
    
    output:  FinishedSession (a list of finished sessions)   
    
    """
    
    FinishedSession = []
    ActiveSessions2 = ActiveSessions.copy()
    for ID in ActiveSessions2:
        session = ActiveSessions2[ID]
        if ((inactivity_duration)<(current_moment-session.momentLR).total_seconds()) or pop_all:
            #pop this session to the FinishedSession list
            expired_session = ActiveSessions.pop(ID)
            FinishedSession.append(expired_session)
    return FinishedSession
#______________________________________________________________________________________________________________________
def embed_last_entry_to_ActiveSessions(ActiveSessions,ip_str,moment,line_number):
    
    """
    input: ActiveSessions (dictionary of sessions),ip_str (str),moment (datetime),line_number(int))
    output: ActiveSessions (dictionary of sessions)
    
    either a new key added or an old one is updated with this new request
        
    """
            
    if ip_str in ActiveSessions:
        ActiveSessions[ip_str].update(moment)
    else:
        session= Session(line_number,moment,ip_str)
        ActiveSessions[ip_str] = session  
                
    return ActiveSessions  
#______________________________________________________________________________________________________________________
def clean_expired_sessions(ActiveSessions,current_moment,inactivity_duration,fo,pop_all=False):
    """
    
    input:ActiveSessions(dictionary of sessions),current_moment (datetime),inactivity_duration (int),fo(output file),pop_all(bool)
     pop_all: when this is True, all of the elements in the ActiveSessions dictionary are popped regardless of time.
     We use this for the end of the log file. 
    Task: writign the newly finished sessions to the output file
    output:  None
    """
    
    
    #pop the expired sessions into FinishedSession List
    FinishedSession = pop_expired(ActiveSessions,current_moment,inactivity_duration,pop_all)
    if len(FinishedSession)>0: 
        SortedSessions = sorted(FinishedSession)
        write_to_output_file(SortedSessions,fo)
#______________________________________________________________________________________________________________________        
def Input_Output_file_operations(inactivity_filename,output_filename,log_filename):
    """ 
        - This function opens and closes inactivity_filename
        - This function creates / clears the output_filename
        - This function opens and closes log_filename to check if the file can be open
    """
    log_file_error = False
    inactivity_file_error = False
    output_file_error = False
    
    
    try:
        #open and closing the log file
        flog = open(log_filename,'r')
        flog.close() 
    except IOError:
        print('Cannot open '+log_filename)
        log_file_error = True

    
    try:
        #reading the inactivity file
        f = open(inactivity_filename,'r') 
    except IOError:
        print('Cannot open '+inactivity_filename)
        inactivity_file_error = True
    else: 

        inactivity_duration = int(f.readline().rstrip())    
        print( '\n inactivity_duration is ',inactivity_duration,'seconds.')
        f.close()
        
        if (inactivity_duration<1) or (inactivity_duration>86400):
            raise Exception ('not a valid inactivity duration. Check the inactivity_filename, valid range: [1,2, .. 86400]')
        
    try:
        #creating the output file
        #making sure I have an empty file each time.
        open(output_filename, 'w').close()
        fo = open(output_filename,'a') #we will close it at the end of main.
    except IOError: 
        print('Cannot open'+output_filename)
        output_file_error = True
        
    if log_file_error or inactivity_file_error or  output_file_error:
        raise Exception('log_file_error:{}, inactivity_file_error:{}, output_file_error: {}'.format(log_file_error,inactivity_file_error,output_file_error))
    else:
        return inactivity_duration, fo     
    
    

#==================================================================================================================
#==================================================================================================================
# CLASSES
#______________________________________________________________________________________________________________________
class Session(object):
    """
 
    
    - A Session object has the following attributes:
        - moment of the first request: momentFR (datetime object)
        - moment of the last request:  momentLR (datetime object)
        - request counter: requestCounter (int)
        - line number: lineNumber (int)
        - session duration: Duration (int)
        - sort method __lt__
        - ID: ID (str)
        - print method __str__
        
    """
   
    
    def __init__(self,line,moment,ip_str):
        """ 
        input: line(int), moment (datetime), ip_str (str)
        
        """
        assert type(moment) is datetime.datetime, 'moment problem'
        assert type(line) is int, 'line problem'
        assert type(ip_str) is str, 'ip_str problem'
        
        self.momentFR = moment
        self.momentLR = moment
        self.requestCounter = 1
        self.lineNumber = line
        self.Duration = 1
        self.ID = ip_str
        
    def update(self,moment):
        """
        input: moment
        task: modify an entry using last information. Increase its requestCounter, update its momentLR and its duration
        
        """ 
        self.requestCounter +=1
        self.momentLR = moment
        self.Duration = int((self.momentLR-self.momentFR).total_seconds())+1
      
    def __lt__(self,other):
        """returns boolean regarding the comparison between two session in terms of which one should be written to
            the output file first. Sessions are first compared according to their moments, earlier moment means 'smaller'
            session. If moments are equal, smaller line number means 'smaller' session
        
        
        """
        earlier_moment = (self.momentFR < other.momentFR) #boolean
        earlier_line_same_moment =  ((self.momentFR == other.momentFR) and self.lineNumber<other.lineNumber) #boolean


        return earlier_moment or earlier_line_same_moment
    

    def __str__(self):
        """Returns a string representation of self:
    
        We might use this for printing into the output file:
        - self.ID: IP address of the user exactly as found in log.csv
        - self.momentFR: date and time of the first webpage request in the session (yyyy-mm-dd hh:mm:ss)
        - self.momentLR: date and time of the last webpage request in the session (yyyy-mm-dd hh:mm:ss)
        - self.Duration: duration of the session in seconds
        - self.requestCounter: count of webpage requests during the session
    
        moment1.isoformat(' ')
        ex: 101.81.133.jja,2017-06-30 00:00:00,2017-06-30 00:00:00,1,1
       """
        return self.ID+','+self.momentFR.isoformat(' ')+','+self.momentLR.isoformat(' ')+','+str(self.Duration)+','+str(self.requestCounter)    
#================================================================================================================== 
    
if __name__== "__main__":
  main()
    