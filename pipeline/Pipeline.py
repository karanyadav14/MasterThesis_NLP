#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import sys
import csv
import requests
import pyconll
import stanza
from stanza.models.common.doc import Document
from stanza.utils.conll import CoNLL

class Parser:
    
    def __init__(self, filepath):
        self.filepath = filepath
        
        
    def format1(self):
        
        ''' # formats the output of Checks steo to add Speaker_id (Sp1,Sp2 and if present Sp3)
            # merges two Channel columns (for two speakers) to one data column
            # adds purna viram to the end of every utterance
            #   Input file = hi_1234_0_checks.txt  
            #   Output file =  hi_1234_1_format.txt
        '''
        
        dirs = os.listdir(self.filepath)
        #print(dirs)
        for file in dirs:
            filename = self.filepath+str(file)
            
            if filename.endswith("_0_checks.txt"):
                filename_in = filename
                filename_out = filename_in.replace("_0_checks.txt","_1_format.txt")
                #print ("in = "+ filename_in)
                #print ("out = "+ filename_out)

                fields = []
                rows = []
                column_value = "" #variable for the string in the transcription column
                data_value= "" #variable for the string in the transcription column as it will appear in the output file
                speaker_value = "" #variable for th string value of Speaker1 or Speaker2
                result_list = []  

                with open(filename_in, 'r', encoding="utf-8") as csvfile:
                    csvreader = csv.reader(csvfile)
                    reader = csv.DictReader(csvfile, delimiter=",")
                    #print (filename_in)
                    
                    flag=False
                    flag1=False
                    
                    for row in reader:

                        begin_time = row["Begin Time - hh:mm:ss.ms"]
                        end_time = row["End Time - hh:mm:ss.ms"]
                        duration = row["Duration - hh:mm:ss.ms"]
                        speaker_1 = row["Channel1"]
                        speaker_2 = row["Channel2"]
                        
                        #print(speaker_1, len(speaker_1), "-", speaker_2, len(speaker_2))
                        if len(str(speaker_1).strip()) == 0:    # use strip in case there are empty spaces at the end of the string
                            column_value = str(speaker_2).strip()    #if empty then this col will be filled with speaker2 value 
                            if "[b_speaker3]" in (column_value):
                                flag=True
                                speaker_value="Sp3"

                            elif "[e_speaker3]" in (column_value) :
                                flag=False
                                speaker_value="Sp3"

                            elif flag==True:
                                speaker_value="Sp3"
                            else:
                                speaker_value = "Sp2"       # correct speaker id is inserted
                        elif len(str(speaker_2).strip()) == 0:
                            column_value = str(speaker_1).strip()
                            if "[b_speaker3]" in (column_value):
                                flag1=True
                                speaker_value="Sp3"
                            elif flag1==True:
                                speaker_value="Sp3"
                            elif "[e_speaker3]" in (column_value) :
                                flag1=False
                                speaker_value="Sp3"   
                            else:
                                speaker_value = "Sp1"
#                         data_value = column_value+str(" ।")     #add a period marker at the end of every utterance (REMOVE)
                        #This last above step can be omitted if the sentence segmentation is taken care of in the transcription
                        
                        if "[b_speaker3]" in column_value:
                            column_value=column_value.replace("[b_speaker3]"," ").replace("  ","")

                        elif "[e_speaker3]" in column_value:
                            column_value=column_value.replace("[e_speaker3]","").replace("  "," ")


                        data_value = column_value
                        #print(data_value)
        
                        result_list.append([begin_time, end_time, duration, speaker_value, data_value])
                        #print(result_list)

                # writing to csv file
                with open(filename_out, 'w',encoding="utf-8", newline='') as csvfile:
                # creating a csv writer object
                    csvwriter = csv.writer(csvfile)
                # writing the fields
                    fields = ['Begin_Time-hh:mm:ss.ms', 'End_Time-hh:mm:ss.ms', 'Duration-hh:mm:ss.ms', 'speaker_id', 'data']
                    csvwriter.writerow(fields)
                    csvwriter.writerows(result_list)



                
    def segment(self):
        
        ''' # one word in a row with space as a delimiter (including annotation tags)
            # each token/word given an index
            # sentence segmentation with purnaviram as delimiter
            # sent_id added to each sentence
            # Metadata added as comments before every sentence: 
               - begin_time, end_time, duration, speaker_id, contains_overlap
            # contains_overlap = True/False (removes # from tokens)
            # insert blank row after every sentence (after every PUNCT)
            #   Input file = hi_1234_1_format.txt  
            #   Output file =  hi_1234_2_segment.txt
        '''
        
        
        dirs = os.listdir(self.filepath)
        #print(dirs)
        for file in dirs:
            filename = self.filepath+str(file)
            
            if filename.endswith("_1_format.txt"):
                filename_in = filename
                filename_out = filename_in.replace("_1_format.txt", "_2_segment.txt")
                #print ("in = "+ filename_in)
                #print ("out = "+ filename_out)

                fields = []
                rows = []
                result_list = []
                sent_id = 1

                with open(filename_in, 'r',encoding="utf-8") as csvfile:
                    csvreader = csv.reader(csvfile)
                    reader = csv.DictReader(csvfile, delimiter=',')

                    result_list.append([("# sent_id = " + str(sent_id)),""])

                    for row in reader:
                        word_index = 1
                        file_name= filename_in[-16:-9]
                        begin_time = row["Begin_Time-hh:mm:ss.ms"]
                        end_time = row["End_Time-hh:mm:ss.ms"]
                        duration = row["Duration-hh:mm:ss.ms"]
                        speaker_name = row["speaker_id"]
                        rowdata = str(row['data']).strip()
                        word_list = rowdata.split(' ')
                        
                        flag = False
                        var= False

                        count = 0
                        count_list = ["#", ]
                        N = len(word_list)
                        temp_list = []
        #                 print(temp_list)
                        for word in word_list:
        #                     if not word.startswith(("#", "\\",)):
        #                         print("###")                   
        #                         count+=1
        #                     print(word)
                            #if word != "": #this line creates a check for double spaces - not required now, as double speces eliminated by checks.py
                            if word == "#":
                                if flag == False:
                                    flag = True     
                                else:
                                    flag = False
                                    var = True


                            elif word == "।":
                                temp_list.append([word_index, word])

                                result_list.append([("# sent_id = " + str(sent_id)),""])
                                result_list.append([("# begin_time = " + str(begin_time)), ""])
                                result_list.append([("# end_time = " + str(end_time)), ""])
                                result_list.append([("# duration = " + str(duration)), ""])
                                result_list.append([("# speaker_id = " + str(speaker_name)), ""])
                                if flag ==True:
                                    x= True
                                elif var ==True:
                                    x= True
                                    var = False
                                else:
                                    x=False
                                result_list.append([("# contains_overlap = "+str(x)), ""])
                                result_list.extend(temp_list)
                                result_list.append(["", ""])

                                temp_list = []
                                word_index = 1
                                sent_id = sent_id+1    

                            else:
                                temp_list.append([word_index, word])
        #                         print(temp_list)
                                word_index = word_index+1


                with open(filename_out, 'w',encoding="utf-8", newline='') as csvfile:
                    # creating a csv writer object
                    csvwriter = csv.writer(csvfile, delimiter = '\t')
                    csvwriter.writerows(result_list)
        

    def chunks(self):
        
        
        ''' # creates chunks based on (outermost) annotation tags 
            # re-orders the word indices within sentences after chunking
            # adds prefix and suffix of outermost tag to the chunk 
            # creates a misc string for outermost tag
            # nested tags are included in the chunk as is
            # maintain the structure of metadta in comments
            #   Input file =  hi_1234_2_segment.txt 
            #   Output file =  hi_1234_3_chunks.txt
        '''
        
        dirs = os.listdir(self.filepath)
        #print(dirs)
        for file in dirs:
            filename = self.filepath+str(file)
        
            if filename.endswith("_2_segment.txt"):
                filename_in = filename
                filename_out = filename_in.replace("_2_segment.txt", "_3_chunks.txt")
                #print ("in = "+ filename_in)
                #print ("out = "+ filename_out)

                result_list= []
                sent_id = 1
                chunk_list = []
                chunk = ""
                chunk_id = ""
                word_index = 1
                misc = {}
                with open(filename_in,'r', encoding = 'utf-8') as csvfile:
                    csvreader = csv.reader(csvfile, delimiter='\t')

                    for row in csvreader:  
                        word_n = row[0]
                        #print(word_n)
                        word_form = row[1]
                        #print(word_form)
                        #print(type(word_form))
                        if len(chunk_list) != 0 and word_form[0]!="\\":
                            chunk_list.append(word_form)

                        if word_n.startswith("#"):
                            result_list.append([word_n,"","","","","","","","",""])
                            continue
                        elif word_n == "":
                            continue 
                        elif word_form =="।":
                            if len(chunk_list) != 0:
                                chunk_list.append(chunk_id)
                                chunk = "_".join(chunk_list)
                                #chunk = chunk.replace("\\","")
                                result_list.append([str(word_index),chunk,misc])
                                word_index = word_index + 1
                                result_list.append([str(word_index),word_form,"_"])
                                result_list.append(["","",""])
                                word_index = 1
                                chunk_list =[]  
                                #this block should check instances of errors where tag is not closed. This code should serve as a barrier for the error to carry over beyond sentence boundary.
                                #check in the end if this block works, by manually removing one of the closing tags (outermost, not nested) in a sentence
                            else:
                                result_list.append([str(word_index),word_form,"_"])
                                result_list.append(["","",""])
                                word_index = 1  

                        elif word_form.startswith("\\"):
                            if len(chunk_list) == 0:
                                chunk_id = word_form
                                chunk_list.append(word_form)
                                
                                 
                                if word_form[1]=='q':
                                    misc = "Quote=Matrix_Tag"
                                if word_form[1]=='c': 
                                    misc = "CodeSwitch=Matrix_Tag"
                                if word_form[1]=='r':
                                    misc = "Repair=Matrix_Tag"
                                if word_form[1]=='d':
                                    misc = "Disfluency=Matrix_Tag"
                                if word_form[1]=='h':
                                    misc = "Hesitation=Matrix_Tag"
                                if word_form[1]=='e':  
                                    misc = "Expletive=Matrix_Tag"

                                #print(misc)
                            elif word_form == chunk_id:
                                chunk_list.append(word_form)
                                chunk = "_".join(chunk_list)
                                #chunk = chunk.replace("\\","")
                                result_list.append([str(word_index),chunk,misc])
                                word_index = word_index +1
                                chunk_list =[]
                            else:
                                chunk_list.append(word_form)
                            continue                            

                        else:
                            if len(chunk_list) == 0:
                                result_list.append([str(word_index) ,word_form,"_"])
                                word_index = word_index + 1

                with open(filename_out, 'w',encoding = 'utf-8', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile, delimiter = '\t')
                    csvwriter.writerows(result_list)


                
                
    def misc(self):
        
        ''' # maintains the sent_id and word_index of the tokens
            # for each nested tag, adds information to misc column
            # removes tags from the chunks
            # format of chunk: prefix & suffix "_" retained (is this needed?)
            # formats the output to conllu format 
            # maintains the structure of metadata in comments
            #   Input file =  hi_1234_3_chunks.txt
            #   Output file =  hi_1234_4_misc.txt
        '''
        
        dirs = os.listdir(self.filepath)
        #print(dirs)
        for file in dirs:
            filename = self.filepath+str(file)
        
            if filename.endswith("_3_chunks.txt"):
                filename_in = filename
                filename_out = filename_in.replace("_3_chunks.txt", "_4_misc.txt")
                #print ("in = "+ filename_in)
                #print ("out = "+ filename_out)

               
                with open(filename_in,'r', encoding = 'utf-8') as csvfile:
                    csvreader = csv.reader(csvfile, delimiter='\t' )

                    result_list = []

                    for row in csvreader: 
                        

                        word_n = row[0]
                        word_form = row[1]
                        misc = row[2]
                        misc_list= []

                        if word_n.startswith("#"):
                            result_list.append(word_n+'\n')
                            continue

                        elif word_n =="":
                            result_list.append('\n')  
                            continue

                        elif word_form.startswith("\\"):
                            misc_list.append(misc)
                            if "_\\q_" in word_form or "_\\r_" in word_form or "_\\d_" in word_form or "_\\h_" in word_form or "_\\c_" in word_form or "_\\exp_" in word_form:
                                misc_list.append("NestedTag=True")
                                #misc_list.append({"NestedTag":"True"})
                                if "_\\q_" in word_form:
                                    subtag = word_form.split("\\q")[1].strip("_")
                                    misc_list.append("Quote='"+subtag+"'")
                                    #print (subtag)
                                if "_\\r_" in word_form:
                                    subtag = word_form.split("\\r")[1].strip("_")
                                    misc_list.append("Repair='"+subtag+"'")
                                    #print (subtag)
                                if "_\\d_" in word_form:
                                    subtag = word_form.split("\\d")[1].strip("_")
                                    misc_list.append("Disfluency='"+subtag+"'")
                                    #print (subtag)
                                if "_\\h_" in word_form:
                                    subtag = word_form.split("\\h")[1].strip("_")
                                    misc_list.append("Hesitation='"+subtag+"'")
                                    #print (subtag)
                                if "_\\c_" in word_form:
                                    subtag = word_form.split("\\c")[1].strip("_")
                                    misc_list.append("CodeSwitch='"+subtag+"'")
                                    #print (subtag)
                                if "_\\exp_" in word_form:
                                    subtag = word_form.split("\\exp")[1].strip("_")   #
                                    misc_list.append("Expletive='"+subtag+"'")
                                    #print (subtag)   
                                misc = r"|".join(misc_list) 
                                #print (type(misc))
                                #print(misc_list)
                                word_form = word_form.replace("\\q_", "")
                                word_form = word_form.replace("_\\q", "")
                                word_form = word_form.replace("\\r_", "")
                                word_form = word_form.replace("_\\r", "")
                                word_form = word_form.replace("\\d_", "")
                                word_form = word_form.replace("_\\d", "")
                                word_form = word_form.replace("\\h_", "")
                                word_form = word_form.replace("_\\h", "")
                                word_form = word_form.replace("\\c_", "")
                                word_form = word_form.replace("_\\c", "")
                                word_form = word_form.replace("\\exp_", "")
                                word_form = word_form.replace("_\\exp", "")
                                word_form = word_form.replace("__", "_")

                                result_list.append(word_n+'\t'+word_form+'\t'+"_"+'\t'+"_"+'\t'+"_"+'\t'+"_"+'\t'+"_"+'\t'+"_"+'\t'+"_"+'\t'+misc+'\n')
                            else:
                                word_form = word_form.replace("\\q_", "")
                                word_form = word_form.replace("_\\q", "")
                                word_form = word_form.replace("\\r_", "")
                                word_form = word_form.replace("_\\r", "")
                                word_form = word_form.replace("\\d_", "")
                                word_form = word_form.replace("_\\d", "")
                                word_form = word_form.replace("\\h_", "")
                                word_form = word_form.replace("_\\h", "")
                                word_form = word_form.replace("\\c_", "")
                                word_form = word_form.replace("_\\c", "")
                                word_form = word_form.replace("\\exp_", "")
                                word_form = word_form.replace("_\\exp", "")
                                word_form = word_form.replace("__", "_")

                                result_list.append(word_n+'\t'+word_form+'\t'+"_"+'\t'+"_"+'\t'+"_"+'\t'+"_"+'\t'+"_"+'\t'+"_"+'\t'+"_"+'\t'+misc+'\n')    
                        else:
                            result_list.append(word_n+'\t'+word_form+'\t'+"_"+'\t'+"_"+'\t'+"_"+'\t'+"_"+'\t'+"_"+'\t'+"_"+'\t'+"_"+'\t'+"_"+'\n')


                with open(filename_out, 'w', encoding = 'utf-8') as f:
                        for item in result_list:
                            f.write(item)
                        
    def stanza_pos(self):
            
        ''' This function uses Stanza POS tagger for POS tagging 
            #   Input file =  hi_1234_4_misc.txt
            #   Output file =  hi_1234_5_pos.txt
         '''

        #giving the path of the directory
        dirs = os.listdir(self.filepath)

        # for every file in the directory
        for file in dirs:
            filename = path+str(file)

            if filename.endswith("_4_misc.txt"):
                filename_in = filename
                filename_out = filename_in.replace("_4_misc.txt", "_5_pos.txt")
                #print ("in = "+ filename_in)
                #print ("out = "+ filename_out)


                doc = CoNLL.conll2doc(filename_in)   #Coverting txt file to stanza Document
                #print(type(doc))

                #Create Stanza POS tagging pipeline
                pos_pipeline = stanza.Pipeline(lang='hi', processors='tokenize,lemma, pos', tokenize_pretokenized=True)

                pos_tagged_doc = pos_pipeline(doc)
                # print(pos_tagged_doc)

                CoNLL.write_doc2conll(pos_tagged_doc, filename_out)



                    
        
    def stanza_pos_rules(self):
        
        ''' # The deterministic rules:
            #   1. The following are tagged X in one step
            #   * disfluency - prefix "d_"
            #   * repair - prefix "r_"
            #   * hesitation - prefix "h_"
            #   * quote - prefix "q_"
            #   * code_switching - prefix "c_"
            #   * [pause]
            #   * [aside]
            #   * [b_aside]
            #   * [e_aside]
            #   * [laughter]
            #   * [noise]
            #   * [incomprehensible]
            #   2. The following tags are modified, unless already tagged X in the previous step:
            #   * हाँ > INTJ
            #   * ह्म > PART
            #   * [anonymized] >PROPN
        
            #   Input file =  hi_1234_5_pos.txt
            #   Output file =  hi_1234_6_pos_rules.txt
        '''
        
        dirs = os.listdir(self.filepath)
        #print(dirs)
        for file in dirs:
            filename = self.filepath+str(file)
            
            if filename.endswith("_5_pos.txt"):
                filename_in = filename
                filename_out = filename_in.replace("_5_pos.txt", "_6_pos_rules.txt")
                #print ("in = "+ filename_in)
                #print ("out = "+ filename_out)

                file = pyconll.load_from_file(filename_in)

                for sentence in file:
                    for token in sentence:
                        misc_item1 = list((token.misc).items())
                        #print (misc_item1)
                        tag = [('Quote', {'Matrix_Tag'}), ('Repair', {'Matrix_Tag'}), ('Disfluency', {'Matrix_Tag'}), 
                       ('Hesitation', {'Matrix_Tag'}),('CodeSwitch', {'Matrix_Tag'}), ('Expletive', {'Matrix_Tag'})]
                        for i in tag:
                            if i in misc_item1:
                                token.upos ="X"
                            #print(misc_item1)
                            #print(token.upos)
                        #help(token.misc)    
                        
                        if str(token.form) == "[pause]":
                            token.upos = "X"
                            
                        if str(token.form) == "[aside]":
                            token.upos = "X"

                        if str(token.form) == "[b_aside]":
                            token.upos = "X"

                        if str(token.form) == "[e_aside]":
                            token.upos = "X"
                        
                        if str(token.form) == "[laughter]":
                            token.upos = "X"
                            

                        if str(token.form) == "[incomprehensible]":
                            token.upos = "X"

                        if str(token.form) == "[noise]":
                            token.upos = "X"

                        if str(token.form) == "हाँ":
                            token.upos = "INTJ"          #Changed from PART to INTJ

                        if str(token.form) == "ह्म":
                            token.upos = "PART" 

                        if str(token.form) == "[anonymized]":
                            token.upos = "PROPN"

#                         if str(token.lemma) == "है" and str(token.xpos) == "VM":
#                             token.upos = "VERB"

#                         if str(token.lemma) == "था" and str(token.xpos) == "VM":
#                             token.upos = "VERB"            

                with open(filename_out, 'w', encoding = 'utf-8') as f:
                    file.write(f)            

    
    def sent_comment(self):
        
        ''' This function adds sentence as a meta data   
        '''
        
        dirs = os.listdir(self.filepath)

        # for every file in the directory
        for file in dirs:
            filename = self.filepath+str(file)

            if filename.endswith("_6_pos_rules.txt"):
    
                file = pyconll.load_from_file(filename)  # Loading file using pyconll
 
                sent = []                          # Creating list to form a single sentence 

                for sentence in file:
                    #print(sentence.to_tree())

                    for word in sentence:
                        sent.append(word.form)                    # Appending each word in sent list
                        if word.form == '।':
                            sent2= " ".join(sent)                   
                            sentence.set_meta('Sentence',sent2)   # Adding sentence in as a meta data
                            sent = []
                            continue


                with open(filename, 'w', encoding = 'utf-8') as f:
                    file.write(f)
    
    
    
    
    def stanza_parse(self):
        
        '''
            Function uses Stanza dependency parser  
            #   Input file =  hi_1234_6_pos_rules.txt
            #   Output file =  hi_1234_output.txt
        '''
        
        dirs = os.listdir(self.filepath)
        #print(dirs)
        for file in dirs:
            filename = self.filepath+str(file)
            
            if filename.endswith("_6_pos_rules.txt"):
                filename_in = filename
                #filename_out = filename_in.replace("_Stanza_SingleScript_6_udpos_rules.txt", "_Stanza_SingleScript_7_Stanza_parse.txt")
                #print(filename_out)

                doc = CoNLL.conll2doc(filename)

                nlp = stanza.Pipeline(lang='hi', processors='depparse', depparse_pretagged=True)

                doc1 = nlp(doc)
                #print(doc1)

                
                #creating new folder in current directory to store the output files
                directory=self.filepath.replace("temp_files","Output_files") 
                #print(directory)
                
                try:
                    os.makedirs(directory,exist_ok=True)
                except OSError as error:
                    pass


                filename_out = file.replace("_6_pos_rules.txt", "_output.txt")
                filename_out2 = os.path.join(directory, filename_out)
                #print(filename_out2)
                
                CoNLL.write_doc2conll(doc1, filename_out2)     #Coverting stanza document to conll format

               
    
    def parser_output(self):
        
        self.format1()
        self.segment()
        self.chunks()
        self.misc()
        self.stanza_pos()
        self.stanza_pos_rules()
        self.sent_comment()
        self.stanza_parse()
        


# In[ ]:


#Giving the path of directory where output of checks is stored

#path = "E:/Cognitive_Science/Project/DialogueCorpus/syntactic_analysis/SingleScript/temp_files/"


single_script = Parser(path)

single_script.parser_output()

