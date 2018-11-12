# Query-based summarization
A set set of query-based summarization algorithms.


## Installation
Requires Python 3 distribution.
Install qbsum:
```
cd qbsum
python setup.py install
``` 

Install spaCy model:
``` 
python -m spacy download en
```

Pythonrouge package requires the Perl XMLParser module:
``` 
sudo apt-get install libxml-parser-perl
```


## Test corpus
A small corpus built using articles from [The Guardian](https://www.theguardian.com/international) is provided for development and testing.


## References
Original papers of baseline algorithms:
- **MMR**: Carbonell, J. & Goldstein, J. (1998). [The Use of MMR, Diversity-based Reranking for Reordering Documents and Producing Summaries](https://dl.acm.org/citation.cfm?id=291025). *Proceedings of he 21st Annual International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 335–336). New York, NY, USA : ACM.

