import os
import re
import json
from pathlib import Path
from loaders import ToyCorpusLoader
from mmr import MMR


# Defining directory structure:
with open('directories.json') as f:
    directories = json.load(f)

documentsDir = Path(os.getcwd()) / directories['toy_corpus']['documents']
queriesDir = Path(os.getcwd()) / directories['toy_corpus']['queries']
referencesDir = Path(os.getcwd()) / directories['toy_corpus']['references']
summariesDir = Path(os.getcwd()) / directories['candidates']


loader = ToyCorpusLoader(documentsDir, queriesDir, referencesDir)
documents = loader.getDocuments()

for event in documents.keys():
    print("EVENT", event)
    for document in documents[event]:
        print('\tTITLE:' + document['title'])
        print('\tTEXT:' + document['text'][:90],"...")
