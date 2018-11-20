import unittest
import os
import json
from pathlib import Path
from qbsum.corpora import NewsCorpus

class TestNewsCorpus(unittest.TestCase):

    def setUp(self):
        # Read directories description from file:
        with open('directories.json') as f:
            directories = json.load(f)
        baseDir = Path(os.getcwd())
        corpus = 'news'
        documentsDir = baseDir / directories[corpus]['documents']
        queriesDir = baseDir / directories[corpus]['queries']
        referencesDir = baseDir / directories[corpus]['references']

        # Load the test corpus:
        self.corpus = NewsCorpus(documentsDir, queriesDir, referencesDir)
    

    def test_document_set_names_type(self):
        self.assertIsInstance(self.corpus.document_set_names(), list)

    def test_document_set_name_type(self):
        self.assertIsInstance(self.corpus.document_set_names()[0], str)
    
    def test_document_sets_type(self):
        self.assertIsInstance(self.corpus.document_sets(), list)
    
    def test_document_set_type(self):
        self.assertIsInstance(self.corpus.document_sets()[0], list)

    def test_document_type(self):
        self.assertIsInstance(self.corpus.document_sets()[0][0], list)

    def test_doc_sentence_type(self):
        self.assertIsInstance(self.corpus.document_sets()[0][0][0], str)

    def test_queries_type(self):
        self.assertIsInstance(self.corpus.queries(), list)

    def test_query_type(self):
        self.assertIsInstance(self.corpus.queries()[0], str)

    def test_all_references_type(self):
        self.assertIsInstance(self.corpus.references(), list)

    def test_topic_references_type(self):
        self.assertIsInstance(self.corpus.references()[0], list)

    def test_reference_type(self):
        self.assertIsInstance(self.corpus.references()[0][0], list)

    def test_ref_sentence_type(self):
        self.assertIsInstance(self.corpus.references()[0][0][0], str)
