import os
from pathlib import Path
import pandas as pd
from models import Document


class Corpus(object):
    """A data loader for the test corpus."""

    def __init__(self, documentsDir=None, queriesDir=None, referencesDir=None, candidatesDir=None):
        """
        Constructor.
        :param documentsDir:
        :type documentsDir: Path
        :param queriesDir:
        :type queriesDir: Path
        :param referencesDir:
        :type referencesDir: Path
        :param candidatesDir:
        :type candidatesDir: Path
        """
        # Reference list must respect the pythonrouge evaluation tool input format.
        # This in turns "imposes" a certain format on the documents and queries list
        # because else it becomes difficult to match topics between lists.
        # See demo_rouge.py file for more details on
        # the pythonrouge evaluation tool input format.

        self.documentsDir = documentsDir
        self.queriesDir = queriesDir
        self.referencesDir = referencesDir
        self.candidatesDir = candidatesDir
        self.documents = []
        self.queries = []
        self.references = []

        
        for flatFile in sorted(os.listdir(self.documentsDir)):

            # Load topic's documents:
            df = pd.read_csv(self.documentsDir/flatFile)
            topic = flatFile.replace(".csv", "")
            topicDocuments = []
            for i, row in df.iterrows():
                topicDocuments.append(Document(row['TITLE'], row['TEXT']))
            self.documents.append(topicDocuments)


            # Load topic's query:
            fileName = topic + ".txt"
            if Path(self.queriesDir/fileName).is_file:
                # Query is the first line of text from the query file:
                with open(self.queriesDir/fileName) as f:
                    self.queries.append(f.readline())
            
            # Load topic's reference summary:
            topicReferences = []
            if Path(self.referencesDir/fileName).is_file:
                with open(self.referencesDir/fileName) as f:
                    # Currently, references consists of the first line of text from the reference file:
                    # TODO: add support for multi-sentence references:
                    topicReferences.append([f.readline()])
                
                self.references.append(topicReferences)
