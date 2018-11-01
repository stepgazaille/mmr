import json
from pythonrouge.pythonrouge import Pythonrouge

# ROUGE evaluates all system summaries and its corresponding reference
# one summary at the time or multiple summaries at once.
# Summary should be double list, in each list has each summary.
# Reference summaries should be triple list because some of reference
# has multiple gold summaries.

# Original implementation: https://github.com/tagucci/pythonrouge/blob/master/example.py

with open('rouge_args.json') as f:
    rouge_args = json.load(f)


# Corpus.candidates implementations must return a candidates[][] list using the following structure:
candidates = [
    [   # A summary about one topic is a list of sentences:
        "Great location, very good selection of food for breakfast buffet.",
        "Stunning food, amazing service.",
        "The food is excellent and the service great."
    ],
    [   # A summary about a second topic:
        "The keyboard, more than 90% standard size, is just large enough.",
        "Surprisingly readable screen for the size.",
        "Smaller size videos play even smoother."
    ]
]



# Loader.getReferences() implementations must return a references[][][] list using the following structure:
references = [
                [   # 3 references for first topic:
                    [
                        "Food was excellent with a wide range of choices and good services.",
                        "It was a bit expensive though."
                    ],
                    [
                        "Food can be a little bit overpriced, but is good for hotel."
                    ],
                    [
                        "The food in the hotel was a little over priced but excellent in taste and choice.",
                        "There were also many choices to eat in the near vicinity of the hotel."
                    ]
                ],
                [   # 4 references for second topic:
                    [
                        "The size is great and allows for excellent portability.",
                        "Makes it exceptionally easy to tote around, and the keyboard is fairly big considering the size of this netbook."
                    ],
                    [
                        "Size is small and manageable.",
                        "Perfect size and weight.",
                        "Great size for travel."
                    ],
                    [
                        "The keyboard is a decent size, a bit smaller then average but good.",
                        "The laptop itself is small but big enough to do things on it."
                    ],
                    [
                        "In spite of being small it is still comfortable.",
                        "The screen and keyboard are well sized for use."
                    ]
                ]
            ]



rouge = Pythonrouge(summary=candidates, reference=references,
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
                    

score = rouge.calc_score()
for key in score.keys():
    print(key + ":\t{}".format(score[key]))