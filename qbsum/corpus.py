import os
from pathlib import Path
import pandas as pd
from qbsum.models import Document


class Corpus(object):
    """A data loader for the test corpus."""

    def __init__(self, documentsDir, queriesDir, referencesDir):
        """
        Constructor.
        :param documentsDir:
        :type documentsDir: Path
        :param queriesDir:
        :type queriesDir: Path
        :param referencesDir:
        :type referencesDir: Path
        """
        # Reference list must respect the pythonrouge evaluation tool input format.
        # This in turns "imposes" a certain format on the documents and queries list
        # because else it becomes difficult to match topics between lists.
        # See demo_rouge.py file for more details on
        # the pythonrouge evaluation tool input format.

        self.documentsDir = documentsDir
        self.queriesDir = queriesDir
        self.referencesDir = referencesDir
        
        self.documents = []
        self.queries = []
        self.references = []
        self.documentSetNames = []

        
        for flatFile in sorted(os.listdir(self.documentsDir)):

            # Define the documents set:
            documentSetName = flatFile.replace(".csv", "")
            self.documentSetNames.append(documentSetName)

            # Load topic's documents:
            df = pd.read_csv(self.documentsDir/flatFile)
            topicDocuments = []
            for i, row in df.iterrows():
                topicDocuments.append(Document(row['TITLE'], row['TEXT']))
            self.documents.append(topicDocuments)


            # Load topic's query:
            fileName = documentSetName + ".txt"
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
