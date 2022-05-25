# -*- coding: utf-8 -*-
"""
Created on Sun May 22 22:32:29 2022

@author: i.grigoreva
"""
import pandas as pd
from collections import Counter
import logging
import sys


class TableProcessor():
    
    
    def __init__(self,file): #,logger):
        '''
        input:
             json_file - input json File     
        '''
        
    
        self.file = file
        self.path = ""
        self.before_text = ""
        self.after_text = ""
        self.caption = ""
        self.table = ""
        
        try:
            data = pd.read_excel(file,dtype=str)
        except:
            print("Table file opening EXCEPTION: " + str(sys.exc_info()[0]))
        
        print("File opened, shape: " + str(data.shape))
        print("Columns dtypes:/n " + str(data.dtypes))
        print("Columns names:/n " + str(data.columns))
        
        # detect where is a table
        #------------------------
        # collect statistics on filled cells in lines
        full_column_list = list()
        for i in range(data.shape[0]):
            #print(i,data.iloc[i].isna().sum())
            full_column_list.append(data.shape[1] - data.iloc[i].isna().sum()) 
        print("Shape[1] and null columns difference:" + str(full_column_list))
        
        # Count real columns
        if Counter(full_column_list).most_common()[0][0] > 0:
            n_columns = Counter(full_column_list).most_common()[0][0] # real count of columns
        else:
            n_columns = data.shape[1]
        print("Real quantity of coluns: " + str(n_columns))    
            
        # count fill, partly fill and other lines
        null_list = list()
        table_list = list()
        text_list = list()
        for i in range(data.shape[0]):
            if data.shape[1] - data.iloc[i].isna().sum() == n_columns: table_list.append(i)
            elif data.iloc[i].isna().sum() == data.shape[1]: null_list.append(i)
            else: text_list.append(i)
                
        # form table table_list
        range_list = list(range(table_list[0],table_list[-1]+1))
        print("null_list: " + str(null_list))
        print("table_list: " + str(table_list))
        print("range_list: "+ str(range_list))
        print("text_list: "+ str(text_list))
        
        # delete empty lines inside the table
        labels_to_drop_list = list()
        if not table_list == range_list:
            for i in range_list:
                if (not i in table_list) and i in text_list:
                    text_list.remove(i)
                    table_list.append(i)
                elif (not i in table_list) and i in null_list:
                    labels_to_drop_list.append(i)
            if len(labels_to_drop_list) > 0:
                data.drop(labels = labels_to_drop_list,axis = 0, inplace = True)
    
        print("Corrected text_list: "+ str(text_list))
        print("Corrected table_list: "+ str(table_list))
            
        # making DataFrame for table
        table_dict = dict()
        for clmn in range(n_columns):
            table_dict[data.iloc[table_list[0],clmn]] = data[data.columns[clmn]].values[table_list[0]+1:table_list[-1]]
        
        # Making DataFrame from dictionary
        table_df = pd.DataFrame.from_dict(table_dict)
        table_df.index.name = "index"
        self.table  = table_df
        print("DataFrame head:/n" + str(table_df.head()))
        #file_csv = ".".join(file.split(".")[:-1]) + ".csv"
        #table_data.to_csv("tmp/" + file_csv)
        
        # colculate before text and after text
        column_cap_list = list()
        for num,i in enumerate(data.columns):
            if not i == "Unnamed: " + str(num):
                column_cap_list.append(i)
                
        before_text_list = [i for i in text_list if i < table_list[0]]
        after_text_list = [i for i in text_list if i > table_list[-1]]
        
        if len(column_cap_list) > 0:
            caption_text = " ".join(column_cap_list)
        else:
            caption_text = ""
        for i in before_text_list:
            for j in range(data.shape[1]):
                if not pd.isnull(data.iloc[i,j]):
                    caption_text += str(data.iloc[i,j])
            caption_text += "\n"
        self.before_text = caption_text
        print("Before_text: " + caption_text)
        
        after_text = ""
        print("after_text",after_text_list)
        for i in after_text_list:
            for j in data.columns:
                if not pd.isnull(data.loc[i,j]):
                    after_text += str(data.loc[i,j])
            after_text += "\n"
        self.after_text = after_text
        print("After_text: " + after_text)
        
    def save_txt(self,file_name):
        save_text = "BEFORE TEXT:\n"
        save_text += self.before_text + "\n"
        save_text += "TABLE:\n"
        save_text += self.table.to_string()
        save_text += "\n"
        save_text += "AFTER TEXT:\n"
        save_text += self.after_text + "\n"
        save_text += "THE END"
        with open(file_name, "w") as fl:
            fl.write(save_text)
    
    def detect_type(self,description,column_names,table):
        '''
        output:
            column_types - dict if column types (text,data,number,number + units(factor))
        '''
        pass
    
    def detect_object_in_columns(self,text_column,column_name):
        '''
        Detect OBJECT of text column
        output:
            object_list - list of object-candidate (type of object-candidate?) with reliability assessments
        '''
        pass
    
    def detect_main_column(self,selfselftext_columns,description,column_names,table):
        '''
        Detecting SUBJECT COLUMNS (from the left to right, less repeats, some corelation with the caption)
        
        output:
             main_index - number of the main column (may be not one)
        '''
        pass
    
    def detect_relation(self,main_column_index,column_names,table):
        '''
        Detecting relation MAIN COLUMNS to other columns
        
        output:
             relation_names - number of the relation for pairs of columns
        '''
        pass
    
    def calculate_consistency_assessment(self):
        '''
        '''
        pass
