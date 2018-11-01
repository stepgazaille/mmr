import os
import re
import json
from pathlib import Path
from corpus import Corpus
from mmr import MMR


# Defining directory structure:
with open('directories.json') as f:
    directories = json.load(f)


documentsDir = Path(os.getcwd()) / directories['test']['documents']
queriesDir = Path(os.getcwd()) / directories['test']['queries']
referencesDir = Path(os.getcwd()) / directories['test']['references']
candidatesDir = Path(os.getcwd()) / directories['test']['candidates']


corpus = Corpus(documentsDir, queriesDir, referencesDir, candidatesDir)


for i in range(len(corpus.queries)):
    print('QUERY:', corpus.queries[i])

    for document in corpus.documents[i]:
        print('\tTITLE\t:', document.title)
        print('\tTEXT\t:', document.text[:90],"...")
    print('\tREF:\t', corpus.references[i])


print(corpus.documents)