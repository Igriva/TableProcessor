import os
import sys
import tableprocessor as tp

if __name__ == "__main__":
    path = sys.argv[1]
    os.chdir(path)
    print(os.getcwd())

    file_list = [i for i in os.listdir('.') if i.split(".")[-1].find("xls") >= 0]
    print(file_list)
    
    for file in file_list:
        print(file,"-"*30)
        table_df = tp.TableProcessor(file) #,logger)
        table_df.save_txt("_".join(file.split(".")[:-1]) + ".txt")
