import os
from mmr import MMR




documents_dir = os.getcwd() + '/documents'
summaries_dir = os.getcwd() + '/summaries'

summerizer = MMR()
summerizer.generate_summaries(documents_dir, summaries_dir)
