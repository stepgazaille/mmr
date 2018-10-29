import pandas as pd
import os

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
            