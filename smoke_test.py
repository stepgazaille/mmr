import os
import re
import json
from pathlib import Path
from loaders import TestCorpusLoader
from mmr import MMR


# Defining directory structure:
with open('directories.json') as f:
    directories = json.load(f)


documentsDir = Path(os.getcwd()) / directories['test']['documents']
queriesDir = Path(os.getcwd()) / directories['test']['queries']
referencesDir = Path(os.getcwd()) / directories['test']['references']
candidatesDir = Path(os.getcwd()) / directories['test']['candidates']


loader = TestCorpusLoader(documentsDir, queriesDir, referencesDir, candidatesDir)

documentsDir = loader.getDocuments()

for topic in documentsDir.keys():
    print("TOPIC", topic)
    print('\tQUERY:\t', loader.getQuery(topic))
    loader.getQuery(topic)
    for document in documentsDir[topic]:
        print('\tTITLE:\t', document['title'])
        print('\tTEXT:\t', document['text'][:90],"...")
    print('\tREF:\t', loader.getReference(topic))
