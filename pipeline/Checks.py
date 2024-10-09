import os
import csv



def checks(file_path):
    '''This script checks the CSV file for the follwing errors:
            # check for pipe symbol instead of hindi purnaviram symbol and undo if found 
            # pairing of annotation tags
            - even number of instances in each utterance 
            - if not, print the error with filename, begin_time, utterance
            # the overlap tag should be equal in number for Sp1 and Sp2 - print the no. of # for Sp1 and Sp2
            '''
    
    dirs = os.listdir(file_path)
    #print(dirs)
    # for every file in the directory
    for file in dirs:
        filename = file_path+str(file)
        #print(file)

        if filename.endswith("_0.csv"):
            filename_in = filename
           
            #print ("in = "+ filename_in)
            #print ("out = "+ filename_out)

            fields = []
            rows = []
            column_value = "" #variable for the string in the transcription column
            data_value= "" #variable for the string in the transcription column as it will appear in the output file
            speaker_value = "" #variable for the string value of Speaker1 or Speaker2
            result_list = []

            count_overlap_sp1 = 0
            count_overlap_sp2 = 0

            with open(filename_in, 'r', encoding="utf-8") as csvfile:
                csvreader = csv.reader(csvfile)
                reader = csv.DictReader(csvfile, delimiter=",")
                #print (filename_in)

                for row in reader:

                    begin_time = row["Begin Time - hh:mm:ss.ms"]
                    end_time = row["End Time - hh:mm:ss.ms"]
                    duration = row["Duration - hh:mm:ss.ms"]
                    speaker_1 = row["Channel1"]
                    speaker_2 = row["Channel2"]


                    # the last above line assigns str in "data" column to variable data_value. 
                    # Also replaces a double white space with a single white space 
                    # Replaces pipe symbol with hindi purnaviram symbol
                    if speaker_1 !="":
                        data_value=speaker_1   #+str(" ।");     #Adding Purnaviram to see how pipeline works when 
                    else:                                  #transcription already have it   
                        data_value=speaker_2   #+str(" ।");

                    data_value = str(data_value).replace("  "," ").replace("|","।")
                    #count the number of \d in the utterance and print (filename+begin_time_utterance) if odd number of occurances
                    count_d = int(data_value.count(r"\d"))
                    if (count_d % 2) != 0:   
                        print ("ERROR FOR d: " + filename_in[-13:-6] + " " + begin_time + " " + data_value)

                    #count the number of \r in the utterance and print (filename+begin_time_utterance) if odd number of occurances
                    count_r = int(data_value.count(r"\r"))
                    if (count_r % 2) != 0:   
                        print ("ERROR FOR r: " + filename_in[-13:-6] + " " + begin_time + " " + data_value)

                    #count the number of \h in the utterance and print (filename+begin_time_utterance) if odd number of occurances
                    count_h = int(data_value.count(r"\h"))
                    if (count_h % 2) != 0:   
                        print ("ERROR FOR h: " + filename_in[-13:-6] + " " + begin_time + " " + data_value)

                    #count the number of \exp in the utterance and print (filename+begin_time_utterance) if odd number of occurances
                    count_exp = int(data_value.count(r"\exp"))
                    if (count_exp % 2) != 0:   
                        print ("ERROR FOR exp: " + filename_in[-13:-6] + " " + begin_time + " " + data_value)

                    #count the number of \q in the utterance and print (filename+begin_time_utterance) if odd number of occurances
                    count_q = int(data_value.count(r"\q"))
                    if (count_q % 2) != 0:   
                        print ("ERROR FOR q: " + filename_in[-13:-6] + " " + begin_time + " " + data_value)

                    #count the number of \c in the utterance and print (filename+begin_time_utterance) if odd number of occurances
                    count_c = int(data_value.count(r"\c"))
                    if (count_c % 2) != 0:   
                        print ("ERROR FOR c: " + filename_in[-13:-6] + " " + begin_time + " " + data_value)

                    #count the number of # in the utterance and print (filename+begin_time_utterance) if odd number of occurances
                    count_overlap = int(data_value.count(r"#"))
                    if (count_overlap % 2) != 0:   
                        print ("ERROR FOR overlap: " + filename_in[-13:-6] + " " + begin_time + " " + data_value)

                    #to check overlaps - additional check - for the 2 speakers, the total number of overlap tags should be the same
                    if speaker_1 != "":
                        count_overlap_sp1 = count_overlap_sp1 + count_overlap
                    if speaker_2 != "":
                        count_overlap_sp2 = count_overlap_sp2 + count_overlap

                    if speaker_1 !="":
                        speaker_1=data_value;
                    else:
                        speaker_2=data_value;
                        
                        
                    speaker_1 = str(speaker_1).replace("  "," ").replace("|","।")
                    speaker_2 = str(speaker_2).replace("  "," ").replace("|","।")

                    result_list.append([begin_time, end_time, duration, speaker_1, speaker_2])
                    #print(result_list)

            #the following prints for each file, the total number of overlap tags for Sp1 and Sp2 
            
            print (str(filename_in[-13:-6]) + " Sp1 overlap count is " + str(int(count_overlap_sp1)))
            print (str(filename_in[-13:-6]) + " Sp2 overlap count is " + str(int(count_overlap_sp2)))

               
            
            
            #Create a New folder to store output of intermediatory steps
            directory= "temp_files" 
            new_path=os.path.join(file_path,directory)
            print(new_path)
            try:
                os.makedirs(new_path,exist_ok=True)
            except OSError as error:
                pass


            new_filename = file.replace("_0.csv", "_0_checks.txt")
            filename_out2 = os.path.join(new_path,new_filename)
            #print(filename_out2)


            
                
            with open(filename_out2, 'w',encoding="utf-8", newline='') as csvfile:
                # creating a csv writer object
                csvwriter = csv.writer(csvfile)
                # writing the fields
                fields = ["Begin Time - hh:mm:ss.ms","End Time - hh:mm:ss.ms","Duration - hh:mm:ss.ms", 'Channel1','Channel2']
                csvwriter.writerow(fields)
                csvwriter.writerows(result_list)

                
                
#Giving directory path of csv input files to checks function                
path = "E:/Cognitive_Science/Project/DialogueCorpus/syntactic_analysis/March_10/"
checks(path)


# In[ ]:




