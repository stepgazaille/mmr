import unittest
import os
import json
from pathlib import Path
from mmr.summarizers import MMR

class TestSummarizer(unittest.TestCase):

    def setUp(self):
        # Read directories description from file:
        self.query = "How is the food?"
        self.topic = [
            [
                "Great location, very good selection of food for breakfast buffet.",
                "Stunning food, amazing service.",
                "The food is excellent and the service great."
            ],
            [
                "Great location, very good selection of food for breakfast buffet.",
                "Stunning food, amazing service.",
                "The food is excellent and the service great."
            ]
        ]
        self.mmr = MMR()

    def test_summary_type(self):
        summary = self.mmr.summarize(self.topic, self.query)
        self.assertIsInstance(summary, list)

    def test_sum_sentence_type(self):
        summary = self.mmr.summarize(self.topic, self.query)
        self.assertIsInstance(summary[0], str)

    def test_similar_sentences(self):
        score = self.mmr._MMR__similarity("Here's a sentence", "Here's a sentence")
        self.assertTrue(score == 1.0)

    def test_dissimilar_sentences(self):
        score = self.mmr._MMR__similarity("Here's a sentence", "Quelque chose de différent")
        # similarity is hardly ever ar 0 so using arbitrary value of 0.4:
        self.assertTrue(score < 0.4)

    def test_count_words(self):
        word_count = self.mmr._MMR__count_words("One two three, four five six?!")
        self.assertTrue(word_count == 6)
