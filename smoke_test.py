import os
import re
import json
from pathlib import Path
from mmr import MMR


# Defining directory structure:
with open('directories.json') as f:
    directories = json.load(f)
corporaDir = Path(os.getcwd() + directories['corpora'])
referencesDir = Path(os.getcwd() + directories['references'])
summariesDir = Path(os.getcwd() + directories['summaries'])


# Create summaries for all corpora:
mmr = MMR()
for corpus in os.listdir(corporaDir):
    print("Running MMR Summarizer for files in corpus", corpus)
    mmr.summarize(corporaDir, corpus, summariesDir)
