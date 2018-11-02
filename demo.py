import os
import re
import json
from pathlib import Path
from pythonrouge.pythonrouge import Pythonrouge
from corpus import Corpus
from summarizers import MMR

# Reading ROUGE evaluation parameters:
with open('rouge_args.json') as f:
    rouge_args = json.load(f)

# Define test corpus directory structure:
baseDir = Path(os.getcwd())
with open('directories.json') as f:
    directories = json.load(f)
documentsDir = baseDir / directories['test']['documents']
queriesDir = baseDir / directories['test']['queries']
referencesDir = baseDir / directories['test']['references']
candidatesDir = baseDir / directories['test']['candidates']
if not candidatesDir.is_dir():
    os.mkdir(candidatesDir)

# Load the test corpus:
corpus = Corpus(documentsDir, queriesDir, referencesDir)


# MMR summarizer evaluation on text corpus:
candidates = []
mmr = MMR()
mmrDir = candidatesDir/'MMR'
if not mmrDir.is_dir():
    os.mkdir(mmrDir)


# For each query from the corpus:
for i in range(len(corpus.queries)):

    topic = corpus.topics[i]

    # Create a summary candidate:
    candidateFile = topic + '.txt'
    candidate = mmr.summarize(corpus.documents[i], corpus.queries[i], mmrDir/candidateFile)
    candidates.append(candidate)
    

    print("\nQUERY {}: ".format(topic),  corpus.queries[i])
    for document in corpus.documents[i]:
        print("\tTITLE\t:", document.title)
        print("\tTEXT\t:", document.text[:90],"...")
    print("\tSUM:\t", candidate)
    print("\tREF:\t", corpus.references[i])



rouge = Pythonrouge(summary=candidates, reference=corpus.references,
                    summary_file_exist=rouge_args['summary_file_exist'],
                    n_gram=rouge_args['n_gram'],
                    ROUGE_SU4=rouge_args['ROUGE_SU4'],
                    ROUGE_L=rouge_args['ROUGE_L'],
                    recall_only=rouge_args['recall_only'],
                    stemming=rouge_args['stemming'],
                    stopwords=rouge_args['stopwords'],
                    word_level=rouge_args['word_level'],
                    length_limit=rouge_args['length_limit'],
                    length=rouge_args['length'],
                    use_cf=rouge_args['use_cf'],
                    cf=rouge_args['cf'],
                    scoring_formula=rouge_args['scoring_formula'],
                    resampling=rouge_args['resampling'],
                    samples=rouge_args['samples'],
                    favor=rouge_args['favor'],
                    p=rouge_args['p'])


print("\nEVALUATION:")
score = rouge.calc_score()
for key in score.keys():
    print("\t" + key + ":\t{}".format(score[key]))
