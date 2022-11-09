# -*- coding: utf-8 -*-

"""
@author: kgy
"""


import os
import pandas as pd
from datetime import  datetime
 



os.system("cd packages/ena-mpx-prep/ ; python metadata_processing.py")
os.system("mkdir -p packages/ena-mpx-prep/data/seq")
matadata = pd.read_csv("packages/ena-mpx-prep/data/ENA_Search.tsv",sep="\t")
id = matadata.accession
contry = matadata.country
date = matadata.collection_date
date_public = matadata.first_public

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
