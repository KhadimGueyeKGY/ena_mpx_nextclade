# -*- coding: utf-8 -*-

"""
@author: kgy
"""


import os
import pandas as pd
from datetime import  datetime , date
 



os.system("cd packages/ena-mpx-prep/ ; python metadata_processing.py")
os.system("mkdir -p packages/ena-mpx-prep/data/seq")
matadata = pd.read_csv("packages/ena-mpx-prep/data/ENA_Search.tsv",sep="\t")
id = matadata.accession


# #**************************************** Downloading  ....
print('\n\n> Downloading Fastas ... [ '+str(datetime.now())+" ]")
#os.system("mkdir -p data")
for i in range(len(id)):
    os.system('curl "https://www.ebi.ac.uk/ena/browser/api/fasta/'+id[i]+'?download=true" --output packages/ena-mpx-prep/data/seq/'+id[i]+'.fasta')
os.system("cat packages/ena-mpx-prep/data/seq/* > packages/ena-mpx-prep/data/sequences.fasta")

 
# #**************************************** Running Nextclade analysis pipeline  ....
print('\n\n> Running Nextclade analysis pipeline ... [ '+str(datetime.now())+" ]")
os.system("nextclade run   --input-dataset 'packages/dataset/MPXV/'   --output-csv 'output/nextclade.csv' --output-tsv 'output/nextclade.tsv' --output-tree 'output/tree.json' packages/ena-mpx-prep/data/sequences.fasta")

print('\033[1;32m \n\n> Done ... [ '+str(datetime.now())+" ] \n\n")


###################################### Generat of the public_sequence_pango_lineages[date] file. 

input_file = open("output/nextclade.tsv","r").read().split("\n")
date= date.today()
new_file = "../public_sequence_pango_lineages_"+str(date.day)+str(date.month)+str(date.year)+".csv"
output_file = open(new_file, "w")
output_file.write("accession,clade,lineage\n")
for i in range(1,len(input_file)):
    if input_file[i] !="":
        acc =input_file[i].split("\t")[0].split("|")[1]
        clade=input_file[i].split("\t")[1]
        lineage = input_file[i].split("\t")[3]
        output_file.write(str(acc)+","+str(clade)+","+str(lineage)+"\n")
output_file.close()
 



os.system("ln -sf  "+new_file+"  ../public_sequence_pango_lineages.csv")
