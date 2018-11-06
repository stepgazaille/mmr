import os
import subprocess
import re
import json
from pathlib import Path
from pythonrouge.pythonrouge import Pythonrouge
from qbsum.corpus import Corpus
from qbsum.summarizers import MMR


#Define directory structure:
# Read directories description from file:
with open('directories.json') as f:
    directories = json.load(f)

baseDir = Path(os.getcwd())
documentsDir = baseDir / directories['test']['documents']
queriesDir = baseDir / directories['test']['queries']
referencesDir = baseDir / directories['test']['references']
summariesDir = baseDir / directories['test']['summaries']

if not summariesDir.is_dir():
    os.mkdir(summariesDir)

mmrDir = summariesDir/'MMR'
if not mmrDir.is_dir():
    os.mkdir(mmrDir)

# Load the test corpus:
corpus = Corpus(documentsDir, queriesDir, referencesDir)


for doc_set in corpus.document_sets:
    print("DOC SET")
    for doc in doc_set:
        print("\tDOC")
        for sentence in doc:
            print("\t\t" + sentence)