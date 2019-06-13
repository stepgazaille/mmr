import unittest
from mmr import preproc
from nltk.corpus import stopwords

class TestPreProc(unittest.TestCase):
    
    def test_lowercase(self):
        text = "The Quick Brown Fox Jumps Over a Lazy Dog"
        preproc_text = preproc.lowercase(text)
        self.assertTrue(preproc_text.islower())


    def test_tokenize(self):
        text = "The Quick Brown Fox Jumps Over a Lazy Dog"
        word_list = preproc.tokenize(text)
        self.assertEqual(len(word_list), 9)


    def test_special_chars(self):
        text = "çéâêîôûàèùëïü|#\\!±\"@$¢%¤?¬&¦*()_-+=^[]:;~`<>{},'.»«°"

        # Should return a single white space character:
        filtered_chars = preproc.remove_special_chars_from(text)
        self.assertEqual(filtered_chars, " ")


    def test_remove_digits(self):
        text  = "123456789 10"

        # Should keep the single white space character:
        filtered_digits = preproc.remove_digits_from(text)
        self.assertEqual(filtered_digits, " ")


    def test_remove_stopwords(self):
        stpwords = stopwords.words('english')

        # All words should be removed:
        filtered_words = preproc.remove_stopwords_from(stpwords)
        self.assertEqual(filtered_words, [])


    def test_stem(self):
        # The sample vocabulary and output were sourced from:
        #     http://tartarus.org/martin/PorterStemmer/voc.txt
        #     http://tartarus.org/martin/PorterStemmer/output.txt
        # and are linked to from the Porter Stemmer algorithm's homepage
        # at http://tartarus.org/martin/PorterStemmer/
        
        words =  ["a", "aaron", "abaissiez", "abandon", "abandoned", "abase", "abash", "abate", "abated", "abatement", "abatements", "abates", "abbess"]
        expected_output = ["a", "aaron", "abaissiez", "abandon", "abandon", "abas", "abash", "abat", "abat", "abat", "abat", "abat", "abbess"]
        output = preproc.stem(words)
        self.assertEqual(output, expected_output)
