import os
import re
from mmr import MMR

documents_dir = os.getcwd() + '/documents'
references_dir = os.getcwd() + '/references'
summaries_dir = os.getcwd() + '/summaries'

summerizer = MMR()
# summerizer.generate_summaries(documents_dir, summaries_dir)


mmr_summaries = os.listdir(summaries_dir + '/MMR')
regexp = r'^d\d{5}'
p = re.compile(regexp, re.IGNORECASE)


for summary_id in mmr_summaries:
    if p.findall(summary_id):
        summary_id = p.findall(summary_id)[0]
        print(summary_id)
        for file_name in os.listdir(references_dir):
            if re.search(summary_id, file_name, re.IGNORECASE):
                print(file_name)

