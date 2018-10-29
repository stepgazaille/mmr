import os
from pathlib import Path
import pandas as pd

class ToyCorpusLoader(object):
    """A data loader for the toy corpus."""

    def __init__(self, documentsDir=None, queriesDir=None, referencesDir=None):
        """
        Loader default constructor.
        """
        self.documentsDir = documentsDir
        self.queriesDir = queriesDir
        self.referencesDir = referencesDir
    


    def getDocuments(self):
        documents = {}
        event_files = os.listdir(self.documentsDir)
        for event in event_files:
            df = pd.read_csv(self.documentsDir/event)
            event = event.replace(".csv", "")
            documents[event] = []
            for i, row in df.iterrows():
                documents[event].append({
                    'title': row['TITLE'],
                    'text': row['TEXT'],
                })
        return documents
    

    def getQuery(self, event):
        file_name = event + ".txt"
        if Path(self.queriesDir/file_name).is_file:
            with open(self.queriesDir/file_name) as f:
                return f.readline()
    
    def getReference(self, event):
        file_name = event + ".txt"
        if Path(self.referencesDir/file_name).is_file:
            with open(self.referencesDir/file_name) as f:
                return f.readline()
            