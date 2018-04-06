
import datetime
import my_functions_classes as myFC
import sys
#==================================================================================================================

def main():
    
    try:
        script = sys.argv[0]
        log_filename_str = sys.argv[1]
        inactivity_filename_str  = sys.argv[2]
        output_filename_str = sys.argv[3]
    
    except:
        print('Input arguments are missing.')
        print('Correct format:')
        print('python ./src/sessionization.py ./input/log.csv ./input/inactivity_period.txt ./output/sessionization.txt')
        print('Check the run.sh file')
        
    else:

        #file operations: checking if the input files are there etc.
        inactivity_duration, output_file = myFC.Input_Output_file_operations(inactivity_filename_str,output_filename_str,log_filename_str)
        
        try:
            #log file is read line by line and necessary operations are done
            process(inactivity_duration, output_file,log_filename_str)
        
        finally:
            #closing the output file       
            output_file.close() 
            print('----------- Output file is closed ----------------')
#==================================================================================================================

def process(inactivity_duration, output_file,log_filename_str):

    
    #reading the log file with readline to be able to work with large files
    with open(log_filename_str) as input_file:
 
        # reading the field row
        fields_row = input_file.readline().rstrip()
        assert len(fields_row.split(',')) == 15, 'Check the first row of the log.csv file'
    
        #initializations
        ActiveSessions = {}
        line_number = 0
        current_moment = None
    
        #reading the other rows one by one
        for line in input_file:
            row_str = line.rstrip()

            if len(row_str.split(',')) is not 15:#, 'Check the {} th row of the log.csv file'.format(line_number+2)
                skip_row = True
                print('Skipped Row - Missing field:',row_str)
            else:    
                row = myFC.reading_row(row_str)
                date_str = row['date']
                time_str = row['time']
                ip_str = row['ip']
    
          
            moment,skip_row = myFC.strip_date_time(date_str,time_str)[0:2]
           
            if skip_row:  
                print('Skipped Row - date/time format error:',row_str)          
            else:    
                assert type(moment) is datetime.datetime, 'moment problem'
    
                if current_moment == None: # initial value
                # this case should happen only when it is first request, then make sure the following:
                    assert  ActiveSessions == {}, 'ActiveSessions should be empty initally'
                    assert line_number == 0, 'line_number should be 0 initally'
                
                    current_moment = moment
                    session= myFC.Session(line_number,moment,ip_str)
                    ActiveSessions[ip_str] = session
        
                elif moment<current_moment:
                    print('\nLog file is NOT in chronological order. previuos entry = {}  new entry: {}'.format(current_moment,moment))
                    print('This row in the input file is ignored.\n')
                    print('Skipped Row - Chronological Error:',row_str)
        
                elif moment == current_moment: # in this case the time has not changed so, we do not need to pop any items    
                    ActiveSessions = myFC.embed_last_entry_to_ActiveSessions(ActiveSessions,ip_str,moment,line_number)
        
                elif moment>current_moment:
        
                    #update the current moment
                    current_moment = moment
                    #pop the expired sessions into FinishedSession List
                    myFC.clean_expired_sessions(ActiveSessions,current_moment,inactivity_duration,output_file)
                    #insert or update the sessions using the most recent entry
                    ActiveSessions = myFC.embed_last_entry_to_ActiveSessions(ActiveSessions,ip_str,moment,line_number)
 
            line_number +=1
        
        if(line_number==0):
            print('Zero request in the log file, check the log file')
        #end of file reached   
        
    # any sessions left should be all considered as expired and written to the output file.     
    pop_all = True

    #pop the expired sessions into FinishedSession List
    myFC.clean_expired_sessions(ActiveSessions,current_moment,inactivity_duration,output_file,pop_all)
   
    #ActiveSessions should be empty
    assert not(bool(ActiveSessions)), 'ActiveSessions problem.' 

       


#==================================================================================================================
if __name__== "__main__":
  main()

