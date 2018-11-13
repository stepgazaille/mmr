import unittest
import os
import json
from pathlib import Path
from qbsum.corpus import Corpus
from qbsum.summarizers import MMR

class TestSummarizer(unittest.TestCase):

    def setUp(self):
        # Read directories description from file:
        with open('directories.json') as f:
            directories = json.load(f)
        baseDir = Path(os.getcwd())
        documentsDir = baseDir / directories['test']['documents']
        queriesDir = baseDir / directories['test']['queries']
        referencesDir = baseDir / directories['test']['references']

        # Load the test corpus:
        self.corpus = Corpus(documentsDir, queriesDir, referencesDir)
        self.mmr = MMR()
    

    def test_summary_type(self):
        summary = self.mmr.summarize(self.corpus.document_sets[0], self.corpus.queries[0])
        print("hello")
        self.assertIsInstance(summary, list)

    def test_sum_sentence_type(self):
        summary = self.mmr.summarize(self.corpus.document_sets[0], self.corpus.queries[0])
        self.assertIsInstance(summary[0], str)

    def test_similar_sentences(self):
        score = self.mmr._MMR__similarity("Here's a sentence", "Here's a sentence")
        self.assertTrue(score > 0.6)

    def test_dissimilar_sentences(self):
        score = self.mmr._MMR__similarity("Here's a sentence", "Quelque chose de différent")
        self.assertTrue(score < 0.4)

    def test_count_words(self):
        word_count = self.mmr._MMR__count_words("One two three, four five six?!")
        self.assertTrue(word_count == 6)
