import os
import math
import string
import re
import nltk
from nltk.corpus import stopwords

# Original implementation: https://github.com/syedhope/Text_Summarization-MMR_and_LexRank


class MMR(object):
    """A summarizer implementing the Maximal Marginal Relevence (MMR) summarization algorithm (Carbonell & Goldstein, 1998)."""

    def __init__(self):
        """
        MMR default constructor. MMR is a simple query-based, multi-document summarization algorithm.
        """


    def __processFile(self, file_name):
        """
        Preprocess the files in the document cluster before passing them into the MMR summarizer system. Here the sentences of the document cluster are modelled as sentences after extracting from the files in the folder path.
        :param file_name: file_name, name of the file in the document cluster.
        :type file_name: str()
        :return: pre-processed sentences.
        :rtype: list(Sentence)
        """

        # read file from provided folder path
        f = open(file_name,'r')
        text_0 = f.read()

        # extract content in TEXT tag and remove tags
        text_1 = re.search(r"<TEXT>.*</TEXT>",text_0, re.DOTALL)
        text_1 = re.sub("<TEXT>\n","",text_1.group(0))
        text_1 = re.sub("\n</TEXT>","",text_1)

        # replace all types of quotations by normal quotes
        text_1 = re.sub("\n"," ",text_1)
        
        text_1 = re.sub("\"","\"",text_1)
        text_1 = re.sub("''","\"",text_1)
        text_1 = re.sub("``","\"",text_1)	
        
        text_1 = re.sub(" +"," ",text_1)

        # segment data into a list of sentences
        sentence_token = nltk.data.load('tokenizers/punkt/english.pickle')
        lines = sentence_token.tokenize(text_1.strip())	

        # setting the stemmer
        sentences = []
        porter = nltk.PorterStemmer()

        # modelling each sentence in file as sentence object
        for line in lines:

            # original words of the sentence before stemming
            originalWords = line[:]
            line = line.strip().lower()

            # word tokenization
            sent = nltk.word_tokenize(line)
            
            # stemming words
            stemmedSent = [porter.stem(word) for word in sent]		
            stemmedSent = list(filter(lambda x: x!='.'and x!='`'and x!=','and x!='?'and x!="'" 
                and x!='!' and x!='''"''' and x!="''" and x!="'s", stemmedSent))
            
            # list of sentence objects
            if stemmedSent != []:
                sentences.append(self.Sentence(file_name, stemmedSent, originalWords))				
        
        return sentences


    def __TFs(self, sentences):
        """
        Calculate term frequencies of the words in the sentences present in the provided document cluster.
        :param sentences: sentences of the document cluster.
        :type sentences: list(Sentence)
        :return: dictonary of term frequency for words in sentences.
        :rtype: dict
        """
        # initialize tfs dictonary
        tfs = {}

        # for every sentence in document cluster
        for sent in sentences:
            # retrieve word frequencies from sentence object	
            wordFreqs = sent.getWordFreq()

            # for every word
            for word in wordFreqs.keys():
                # if word already present in the dictonary
                if tfs.get(word, 0) != 0:
                    tfs[word] = tfs[word] + wordFreqs[word]
                # # else if word is being added for the first time
                else:
                    tfs[word] = wordFreqs[word]	
        return tfs


    def __IDFs(self, sentences):
        """
        Calculate the inverse document frequencies of the words in the sentences present in the provided document cluster.
        :param sentences: sentences of the document cluster.
        :type sentences: list(Sentence)
        :return: dictonary of inverse document frequency score for words in sentences.
        :rtype: dict
        """

        N = len(sentences)
        idf = 0
        idfs = {}
        words = {}
        w2 = []
        
        # every sentence in our cluster
        for sent in sentences:
            
            # every word in a sentence
            preProcWords = sent.getPreProWords()
            for word in preProcWords:
            # for word in sent.getPreProWords():

                # not to calculate a word's IDF value more than once
                if sent.getWordFreq().get(word, 0) != 0:
                    words[word] = words.get(word, 0)+ 1

        # for each word in words
        for word in words:
            n = words[word]
            
            # avoid zero division errors
            try:
                w2.append(n)
                idf = math.log10(float(N)/n)
            except ZeroDivisionError:
                idf = 0
                    
            # reset variables
            idfs[word] = idf
                
        return idfs


    def __TF_IDF(self, sentences):
        """
        Calculate TF-IDF score of the words in the document cluster.
        :param sentences: sentences of the document cluster.
        :type sentences: list(Sentence)
        :return: dictonary of TF-IDF score for words in sentences.
        :rtype: dict
        """

        # Method variables
        tfs = self.__TFs(sentences)
        idfs = self.__IDFs(sentences)
        retval = {}


        # for every word
        for word in tfs:
            #calculate every word's tf-idf score
            x = tfs[word]
            y = idfs[word]
            tf_idfs = x*y
            # tf_idfs=  tfs[word] * idfs[word]
            
            # add word and its tf-idf score to dictionary
            if retval.get(tf_idfs, None) == None:
                retval[tf_idfs] = [word]
            else:
                retval[tf_idfs].append(word)

        return retval


    def __sentenceSim(self, sentence1, sentence2, IDF_w):
        """
        Determining the sentence similarity for a pair of sentences by calculating cosine similarity.
        :param sentence1: first sentence.
        :type sentence1: Sentence
        :param sentence2: second sentence.
        :type sentence2: Sentence
        :return: cosine similarity score.
        :rtype: float
        """

        numerator = 0
        denominator = 0	
        
        for word in sentence2.getPreProWords():		
            numerator+= sentence1.getWordFreq().get(word,0) * sentence2.getWordFreq().get(word,0) *  IDF_w.get(word,0) ** 2

        for word in sentence1.getPreProWords():
            denominator+= ( sentence1.getWordFreq().get(word,0) * IDF_w.get(word,0) ) ** 2

        # check for divide by zero cases and return back minimal similarity
        try:
            return numerator / math.sqrt(denominator)
        except ZeroDivisionError:
            return float("-inf")	


    def __buildQuery(self, sentences, TF_IDF_w, n):
        """
        Build a query of n words on the basis of TF-IDF value.
        :param sentences: sentences of the document cluster.
        :type sentences: list(Sentence)
        :param TF_IDF_w: TF-IDF values of the words.
        :type TF_IDF_w: dict
        :param n: desired length of query (number of words in query).
        :type n: int
        :return: query sentence consisting of best n words.
        :rtype: Sentence
        """

        #sort in descending order of TF-IDF values
        scores = TF_IDF_w.keys()
        # scores.sort(reverse=True)
        scores = sorted(scores, reverse=True)	
        
        i = 0
        j = 0
        queryWords = []

        # select top n words
        while(i<n):
            words = TF_IDF_w[scores[j]]
            for word in words:
                queryWords.append(word)
                i=i+1
                if (i>n): 
                    break
            j=j+1

        # return the top selected words as a sentence
        return self.Sentence("query", queryWords, queryWords)


    def bestSentence(self, sentences, query, IDF):
        """
        Find the best sentence in reference to the query.
        :param sentences: sentences of the document cluster.
        :type sentences: list(Sentence)
        :param query: reference query.
        :type query: Sentence
        :param IDF: IDF value of words of the document cluster.
        :type IDF: dict
        :return: best sentence among the sentences in the document cluster.
        :rtype: Sentence
        """

        best_sentence = None
        maxVal = float("-inf")

        for sent in sentences:
            similarity = self.__sentenceSim(sent, query, IDF)		

            if similarity > maxVal:
                best_sentence = sent
                maxVal = similarity
        sentences.remove(best_sentence)

        return best_sentence

    
    def makeSummary(self, sentences, best_sentence, query, summary_length, lambta, IDF):
        """
        Create the summary set of a desired number of words.
        :param sentences: sentences of the document cluster.
        :type sentences: list(Sentence)
        :param best_sentence: best sentence in the document cluster.
        :type best_sentence: Sentence
        :param query: reference query.
        :type query: Sentence
        :param summary_length: desired number of words for the summary.
        :type summary_length: int
        :param lambta: lambda value of the MMR formula.
        :type lambta: float
        :param IDF: IDF value of words of the document cluster.
        :type IDF: dict
        :return: best sentence among the sentences in the document cluster.
        :rtype: Sentence
        """

        summary = [best_sentence]
        sum_len = len(best_sentence.getPreProWords())

        MMRval={}

        # keeping adding sentences until number of words exceeds summary length
        while (sum_len < summary_length):	
            MMRval={}		

            for sent in sentences:
                MMRval[sent] = self.__MMRScore(sent, query, summary, lambta, IDF)

            maxxer = max(MMRval, key=MMRval.get)
            summary.append(maxxer)
            sentences.remove(maxxer)
            sum_len += len(maxxer.getPreProWords())	

        return summary


    def __MMRScore(self, Si, query, Sj, lambta, IDF):
        """
        Function to calculate the MMR score given a sentence, the query and the current best set of sentences.
        :param Si: particular sentence for which the MMR score has to be calculated.
        :type Si: Sentence
        :param query: reference query.
        :type query: Sentence
        :param Sj: already selected best sentences.
        :type Sj: list(Sentence)
        :param lambta: lambda value of the MMR formula.
        :type lambta: float
        :param IDF: IDF value of words of the document cluster.
        :type IDF: dict
        :return: MMR score.
        :rtype: float
        """

        Sim1 = self.__sentenceSim(Si, query, IDF)
        l_expr = lambta * Sim1
        value = [float("-inf")]

        for sent in Sj:
            Sim2 = self.__sentenceSim(Si, sent, IDF)
            value.append(Sim2)

        r_expr = (1-lambta) * max(value)
        MMR_SCORE = l_expr - r_expr	

        return MMR_SCORE


    def generate_summaries(self, documents_dir=None, summaries_dir=None):
        """
        Generate_summaries.
        """

        # set the main Document folder path where the subfolders are present
        main_folder_path = documents_dir
        results_folder = summaries_dir + "/MMR"


        # read in all the subfolder names present in the main folder
        for folder in os.listdir(main_folder_path):
            
            print("Running MMR Summarizer for files in folder: ", folder)
            # for each folder run the MMR summarizer and generate the final summary
            curr_folder = main_folder_path + "/" + folder		

            # find all files in the sub folder selected
            files = os.listdir(curr_folder)

            sentences = []	

            for file in files:			
                sentences = sentences + self.__processFile(curr_folder + "/" + file)

            # calculate TF, IDF and TF-IDF scores
            # TF_w 		= TFs(sentences)
            IDF_w 		= self.__IDFs(sentences)
            TF_IDF_w 	= self.__TF_IDF(sentences)	

            # build query; set the number of words to include in our query
            query = self.__buildQuery(sentences, TF_IDF_w, 10)

            # pick a sentence that best matches the query	
            best1sentence = self.bestSentence(sentences, query, IDF_w)		

            # build summary by adding more relevant sentences
            summary = self.makeSummary(sentences, best1sentence, query, 100, 0.5, IDF_w)
            
            final_summary = ""
            for sent in summary:
                final_summary = final_summary + sent.getOriginalWords() + "\n"
            final_summary = final_summary[:-1]

            if not os.path.exists(results_folder):
                os.makedirs(results_folder)	
            
            with open(os.path.join(results_folder,(str(folder))),"w") as fileOut: fileOut.write(final_summary)

    

    class Sentence(object):

        def __init__(self, docName, preproWords, originalWords):
            """
            Sentence constructor.
            Encapsulates sentences original text along preprocessed statistics.
            :param docName: name of the original document/file.
            :type docName: str
            :param preproWords: words of the file after the stemming process.
            :type preproWords: list(str)
            :param originalWords: actual words before stemming.
            :type originalWords: list(str)
            """
            self.docName = docName
            self.preproWords = preproWords
            self.wordFrequencies = self.sentenceWordFreq()
            self.originalWords = originalWords

        def getDocName(self):
            return self.docName
        
        def getPreProWords(self):
            return self.preproWords
        
        def getOriginalWords(self):
            return self.originalWords


        def getWordFreq(self):
            return self.wordFrequencies	
        
        def sentenceWordFreq(self):
            """
            Create a dictonary of word frequencies for the sentence object.
            :return: dictonary of word frequencies.
            :rtype: dict
            """
            wordFreq = {}
            for word in self.preproWords:
                if word not in wordFreq.keys():
                    wordFreq[word] = 1
                else:
                    # if word in stopwords.words('english'):
                    # 	wordFreq[word] = 1
                    # else:			
                    wordFreq[word] = wordFreq[word] + 1
            return wordFreq
