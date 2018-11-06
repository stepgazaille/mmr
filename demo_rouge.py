import subprocess
import json
from pythonrouge.pythonrouge import Pythonrouge



# Original implementation: https://github.com/tagucci/pythonrouge/blob/master/example.py

with open('rouge_args.json') as f:
    rouge_args = json.load(f)


# Candidate summaries must be double lists of the following structure:
candidates = [
    [   # A summary of a document set is a list of sentences:
        "Great location, very good selection of food for breakfast buffet.",
        "Stunning food, amazing service.",
        "The food is excellent and the service great."
    ],
    [   # A summary of a second document set:
        "The keyboard, more than 90% standard size, is just large enough.",
        "Surprisingly readable screen for the size.",
        "Smaller size videos play even smoother."
    ]
]



# Reference summaries must be triple lists of the following structure:
references = [
                [   # 3 references for a first document set:
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
                [   # 4 references for a second document set:
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


try:
    score = rouge.calc_score()
    print("\nEVALUATION")
    for key in score.keys():
        print("\t" + key + "\t {}".format(score[key]))
except Exception as e:
    print(e)
