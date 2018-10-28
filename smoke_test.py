import os
import re
from mmr import MMR
from pathlib import Path

corporaDir = Path(os.getcwd() + '/documents')
referencesDir = Path(os.getcwd() + '/references')
summariesDir = Path(os.getcwd() + '/summaries')


mmr = MMR()
for corpus in os.listdir(corporaDir):
    print("Running MMR Summarizer for files in corpus", corpus)
    mmr.summarize(corporaDir, corpus, summariesDir)
