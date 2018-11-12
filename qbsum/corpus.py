import os
from pathlib import Path
import pandas as pd
import spacy


class Corpus(object):
    """A data loader for the test corpus."""

    def __init__(self, documents_dir, queries_dir, references_dir):
        """
        Constructor.
        :param documents_dir:
        :type documents_dir: Path
        :param queries_dir:
        :type queries_dir: Path
        :param references_dir:
        :type references_dir: Path
        """
        # Reference list must respect the pythonrouge evaluation tool input format.
        # This in turns imposes a certain format on the documents and queries lists
        # because else it becomes difficult to match document sets between lists.
        # See demo_rouge.py file for more details on
        # the pythonrouge evaluation tool input format.

        nlp = spacy.load('en_core_web_sm')
        self.documents_dir = documents_dir
        self.queries_dir = queries_dir
        self.references_dir = references_dir
        
        self.document_sets = []
        self.queries = []
        self.references = []
        self.document_set_names = []

        for flat_file in sorted(os.listdir(str(self.documents_dir))):

            # Define the documents set:
            document_set_name = flat_file.replace(".csv", "")
            self.document_set_names.append(document_set_name)

            # Load documents:
            df = pd.read_csv(self.documents_dir/flat_file, encoding='utf-8-sig')
            document_set = []
            for i, row in df.iterrows():
                document = [row['TITLE']]
                body = nlp(row['TEXT'])
                for sentence in body.sents:
                    document.append(sentence.text)
                document_set.append(document)
            self.document_sets.append(document_set)


            # Load queries:
            file_name = document_set_name + ".txt"
            if Path(self.queries_dir/file_name).is_file:
                # Query is the first line of text from the query file:
                with open(str(self.queries_dir/file_name), encoding='utf-8-sig') as f:
                    self.queries.append(f.readline())
            
            # Load topic's reference summary:
            doc_set_references = []
            if Path(self.references_dir/file_name).is_file:
                with open(str(self.references_dir/file_name), encoding='utf-8-sig') as f:
                    # Currently, references consists of the first line of text from the reference file:
                    # TODO: add support for multi-sentence references:
                    doc_set_references.append([f.readline()])
                
                self.references.append(doc_set_references)
