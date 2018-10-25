import os
import math
import string
import re
import nltk
from nltk.corpus import stopwords

# Original implementation: https://github.com/syedhope/Text_Summarization-MMR_and_LexRank



class MMR(object):

    def __init__(self):
            self.attribute = None



    #---------------------------------------------------------------------------------
    # Description	: Function to preprocess the files in the document cluster before
    #				  passing them into the MMR summarizer system. Here the sentences
    #				  of the document cluster are modelled as sentences after extracting
    #				  from the files in the folder path. 
    # Parameters	: file_name, name of the file in the document cluster
    # Return 		: list of sentence object
    #---------------------------------------------------------------------------------
    def processFile(self, file_name):

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

    #---------------------------------------------------------------------------------
    # Description	: Function to find the term frequencies of the words in the
    #				  sentences present in the provided document cluster
    # Parameters	: sentences, sentences of the document cluster
    # Return 		: dictonary of word, term frequency score
    #---------------------------------------------------------------------------------
    def TFs(self, sentences):
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

    #---------------------------------------------------------------------------------
    # Description	: Function to find the inverse document frequencies of the words in
    #				  the sentences present in the provided document cluster 
    # Parameters	: sentences, sentences of the document cluster
    # Return 		: dictonary of word, inverse document frequency score
    #---------------------------------------------------------------------------------
    def IDFs(self, sentences):
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

    #---------------------------------------------------------------------------------
    # Description	: Function to find TF-IDF score of the words in the document cluster
    # Parameters	: sentences, sentences of the document cluster
    # Return 		: dictonary of word, TF-IDF score
    #---------------------------------------------------------------------------------
    def TF_IDF(self, sentences):

        # Method variables
        tfs = self.TFs(sentences)
        idfs = self.IDFs(sentences)
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

    #---------------------------------------------------------------------------------
    # Description	: Function to find the sentence similarity for a pair of sentences
    #				  by calculating cosine similarity
    # Parameters	: sentence1, first sentence
    #				  sentence2, second sentence to which first sentence has to be compared
    #				  IDF_w, dictinoary of IDF scores of words in the document cluster
    # Return 		: cosine similarity score
    #---------------------------------------------------------------------------------
    def sentenceSim(self, sentence1, sentence2, IDF_w):
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

    #---------------------------------------------------------------------------------
    # Description	: Function to build a query of n words on the basis of TF-IDF value
    # Parameters	: sentences, sentences of the document cluster
    #				  IDF_w, IDF values of the words
    #				  n, desired length of query (number of words in query)
    # Return 		: query sentence consisting of best n words
    #---------------------------------------------------------------------------------
    def buildQuery(self, sentences, TF_IDF_w, n):
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

    #---------------------------------------------------------------------------------
    # Description	: Function to find the best sentence in reference to the query
    # Parameters	: sentences, sentences of the document cluster
    #				  query, reference query
    #				  IDF, IDF value of words of the document cluster
    # Return 		: best sentence among the sentences in the document cluster
    #---------------------------------------------------------------------------------
    def bestSentence(self, sentences, query, IDF):
        best_sentence = None
        maxVal = float("-inf")

        for sent in sentences:
            similarity = self.sentenceSim(sent, query, IDF)		

            if similarity > maxVal:
                best_sentence = sent
                maxVal = similarity
        sentences.remove(best_sentence)

        return best_sentence

    #---------------------------------------------------------------------------------
    # Description	: Function to create the summary set of a desired number of words 
    # Parameters	: sentences, sentences of the document cluster
    #				  best_sentnece, best sentence in the document cluster
    #				  query, reference query for the document cluster
    #				  summary_length, desired number of words for the summary
    #				  labmta, lambda value of the MMR score calculation formula
    #				  IDF, IDF value of words in the document cluster 
    # Return 		: name 
    #---------------------------------------------------------------------------------
    def makeSummary(self, sentences, best_sentence, query, summary_length, lambta, IDF):	
        summary = [best_sentence]
        sum_len = len(best_sentence.getPreProWords())

        MMRval={}

        # keeping adding sentences until number of words exceeds summary length
        while (sum_len < summary_length):	
            MMRval={}		

            for sent in sentences:
                MMRval[sent] = self.MMRScore(sent, query, summary, lambta, IDF)

            maxxer = max(MMRval, key=MMRval.get)
            summary.append(maxxer)
            sentences.remove(maxxer)
            sum_len += len(maxxer.getPreProWords())	

        return summary

    #---------------------------------------------------------------------------------
    # Description	: Function to calculate the MMR score given a sentence, the query
    #				  and the current best set of sentences
    # Parameters	: Si, particular sentence for which the MMR score has to be calculated
    #				  query, query sentence for the particualr document cluster
    #				  Sj, the best sentences that are already selected
    #				  lambta, lambda value in the MMR formula
    #				  IDF, IDF value for words in the cluster
    # Return 		: name 
    #---------------------------------------------------------------------------------
    def MMRScore(self, Si, query, Sj, lambta, IDF):	
        Sim1 = self.sentenceSim(Si, query, IDF)
        l_expr = lambta * Sim1
        value = [float("-inf")]

        for sent in Sj:
            Sim2 = self.sentenceSim(Si, sent, IDF)
            value.append(Sim2)

        r_expr = (1-lambta) * max(value)
        MMR_SCORE = l_expr - r_expr	

        return MMR_SCORE





    class Sentence(object):

        #------------------------------------------------------------------------------
        # Description	: Constructor to initialize the setence object
        # Parameters  	: docName, name of the document/file
        #				  preproWords, words of the file after the stemming process
        #				  originalWords, actual words before stemming
        # Return 		: None
        #------------------------------------------------------------------------------
        def __init__(self, docName, preproWords, originalWords):
            self.docName = docName
            self.preproWords = preproWords
            self.wordFrequencies = self.sentenceWordFreq()
            self.originalWords = originalWords

        #------------------------------------------------------------------------------
        # Description	: Function to return the name of the document
        # Parameters	: None
        # Return 		: name of the document
        #------------------------------------------------------------------------------
        def getDocName(self):
            return self.docName
        
        #------------------------------------------------------------------------------
        # Description	: Function to return the stemmed words
        # Parameters	: None
        # Return 		: stemmed words of the sentence
        #------------------------------------------------------------------------------
        def getPreProWords(self):
            return self.preproWords
        
        #------------------------------------------------------------------------------
        # Description	: Function to return the original words of the sentence before
        #				  stemming
        # Parameters	: None
        # Return 		: pre-stemmed words
        #------------------------------------------------------------------------------
        def getOriginalWords(self):
            return self.originalWords

        #------------------------------------------------------------------------------
        # Description	: Function to return a dictonary of the word frequencies for
        #				  the particular sentence object
        # Parameters	: None
        # Return 		: dictionar of word frequencies
        #------------------------------------------------------------------------------
        def getWordFreq(self):
            return self.wordFrequencies	
        
        #------------------------------------------------------------------------------
        # Description	: Function to create a dictonary of word frequencies for the
        #				  sentence object
        # Parameters	: None
        # Return 		: dictionar of word frequencies
        #------------------------------------------------------------------------------
        def sentenceWordFreq(self):
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






    # -------------------------------------------------------------
    #	MAIN FUNCTION
    # -------------------------------------------------------------
    def generate_summaries(self):	

        # set the main Document folder path where the subfolders are present
        main_folder_path = os.getcwd() + "/documents"

        # read in all the subfolder names present in the main folder
        for folder in os.listdir(main_folder_path):
            
            print("Running MMR Summarizer for files in folder: ", folder)
            # for each folder run the MMR summarizer and generate the final summary
            curr_folder = main_folder_path + "/" + folder		

            # find all files in the sub folder selected
            files = os.listdir(curr_folder)

            sentences = []	

            for file in files:			
                sentences = sentences + self.processFile(curr_folder + "/" + file)

            # calculate TF, IDF and TF-IDF scores
            # TF_w 		= TFs(sentences)
            IDF_w 		= self.IDFs(sentences)
            TF_IDF_w 	= self.TF_IDF(sentences)	

            # build query; set the number of words to include in our query
            query = self.buildQuery(sentences, TF_IDF_w, 10)		

            # pick a sentence that best matches the query	
            best1sentence = self.bestSentence(sentences, query, IDF_w)		

            # build summary by adding more relevant sentences
            summary = self.makeSummary(sentences, best1sentence, query, 100, 0.5, IDF_w)
            
            final_summary = ""
            for sent in summary:
                final_summary = final_summary + sent.getOriginalWords() + "\n"
            final_summary = final_summary[:-1]
            results_folder = os.getcwd() + "/results/MMR"
            if not os.path.exists(results_folder):
                os.makedirs(results_folder)	
            with open(os.path.join(results_folder,(str(folder) + ".mmr")),"w") as fileOut: fileOut.write(final_summary)