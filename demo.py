import os
import subprocess
import re
import json
from pathlib import Path
from pythonrouge.pythonrouge import Pythonrouge
from qbsum.corpus import Corpus
from qbsum.summarizers import MMR


#Define directory structure:
# Read directories description from file:
with open('directories.json') as f:
    directories = json.load(f)

baseDir = Path(os.getcwd())
documentsDir = baseDir / directories['test']['documents']
queriesDir = baseDir / directories['test']['queries']
referencesDir = baseDir / directories['test']['references']
summariesDir = baseDir / directories['test']['summaries']

if not summariesDir.is_dir():
    os.mkdir(summariesDir)

mmrDir = summariesDir/'MMR'
if not mmrDir.is_dir():
    os.mkdir(mmrDir)

# Load the test corpus:
corpus = Corpus(documentsDir, queriesDir, referencesDir)



# Initialize summarizer:
candidates = []
mmr = MMR()

# Generate summaries:
# For each documents set in corpus:
for i in range(len(corpus.queries)):

    document_set_name = corpus.document_set_names[i]

    # Create a summary:
    summary_file = document_set_name + '.txt'
    summary = mmr.summarize(corpus.document_sets[i],
        corpus.queries[i],
        mmrDir/summary_file,
        max_length=10,
        lda=0.9)
    candidates.append(summary)
    

    print("\nDOC SET {}".format(document_set_name))
    print("\tQUERY\t", corpus.queries[i])
    print("\tSUM\t", summary)
    print("\tREF\t", corpus.references[i])


# Read ROUGE configuration from file:
with open('rouge_args.json') as f:
    rouge_args = json.load(f)

# Configure pythonrouge:
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


# Evaluate candidate summaries:
try:
    score = rouge.calc_score()
    print("\nEVALUATION")
    for key in score.keys():
        print("\t" + key + "\t {}".format(score[key]))
except Exception as e:
    print(e)



