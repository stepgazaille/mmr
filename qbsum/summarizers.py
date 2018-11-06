import os
import collections
import spacy
import re


# Original implementation: https://www.quora.com/Where-can-I-find-a-maximum-marginal-relevance-algorithm-in-Python-for-redundancy-removal-in-two-documents
class MMR(object):
    """A summarizer implementing the Maximal Marginal Relevence (MMR) summarization algorithm (Carbonell & Goldstein, 1998)."""
    def __init__(self):
        """
        MMR default constructor. MMR is a simple query-based, multi-document summarization algorithm.
        """
        self.__nlp = spacy.load('en')


    def summarize(self, document_set, query, summary_file=None, max_length=100, lda=0.3):
        """
        Generates a summary of the documents in a set with respect to a particular query.
        :param document_set: set of documents to be summarized.
        :type document_set: list(list(str))
        :param query: query about the set of documents.
        :type query: str
        :param summary_file: path of a file where to output the candidate summary. If None is provided then no file is created or updated.
        :type summary_file: Path
        :param max_length: Maximum number of words that the summary cans include.
        :type max_length: int
        :param lda: lambda parameter used in computation of MMR score.
        :type lda: float
        :return: the candidate summary
        :rtype: list(str)
        """
        complete_set = set()
        for document in document_set:
            complete_set = complete_set.union(set(document))

        selected = collections.OrderedDict()
        summary_len = 0
        while set(selected) != complete_set and summary_len < max_length:
            remaining = complete_set - set(selected)
            mmr_score = lambda x: lda*self.__similarity(x, query) - (1-lda)*max([self.__similarity(x, y) for y in set(selected)-{x}], default=0)
            next_selected = max(remaining, key=mmr_score) #self.__argmax(remaining, mmr_score)
            summary_len += self.__count_words(next_selected)
            selected[next_selected] = len(selected)

        if summary_file:
            with open(summary_file, 'w', encoding='utf-8-sig') as f:
                f.write(" ".join(selected))

        return list(selected)


    def __similarity(self, sent_1, sent_2):
        """
        Compute similarity score between two sentences.
        :param sent_1: the first sentence.
        :type sent_1: str
        :param sent_2: the second sentence.
        :type sent_2: str
        :return: similarity score
        :rtype: float
        """
        sent_1 = self.__nlp(sent_1)
        sent_2 = self.__nlp(sent_2)
        return sent_1.similarity(sent_2)


    def __count_words(self, sentence):
        """
        Compute the number of words in a sentence.
        :param sentence: a sentence.
        :type sentence: str
        :return: number of words in the sentence
        :rtype: int
        """
        return len(re.sub(r"[^\w]", " ",  sentence).split())
