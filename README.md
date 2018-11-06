# Query-based summarization
A set set of query-based summarization algorithms.

## Requirements
Requires Anaconda Python 3 distribution.
Use the following procedure to install all requirements:

1. Download and install the Anaconda Python distribution from the [Anaconda website](https://www.anaconda.com/).

2. Create new virtual environment:
```
cd qbsum
conda env create qbsum -f environment.yml
```

3. Activate the virtual environment:
```
conda activate qbsum
```

4. Install the qbsum package:
```
cd qbsum

# Normal installation:
pip install .

# Editable installation:
pip install -e .
```

5. Install spaCy model:
``` 
python -m spacy download en
```


5. The pythonrouge package requires the Perl XMLParser module:
``` 
sudo apt-get install libxml-parser-perl
```


## Virtual environment management
To activate the project's virtual environment, use:
```
conda activate qbsum
```

To launch Jupyter to manage and execute notebooks, use:
```
jupyter notebook
```
Press `CTRL+C` to stop execution.

To deactivate the project's virtual environment, use:
```
conda deactivate
```

To remove the project's virtual environment, use:
```
conda remove -y -n qbsum --all
```

To update the project's virtual environment, use:
```
conda env update -n qbsum -f environment.yml
```


## Test corpus
A small corpus built using articles from [The Guardian](https://www.theguardian.com/international) is provided for development and testing.


## References
Original papers of baseline algorithms:
- **MMR**: Carbonell, J. & Goldstein, J. (1998). [The Use of MMR, Diversity-based Reranking for Reordering Documents and Producing Summaries](https://dl.acm.org/citation.cfm?id=291025). *Proceedings of he 21st Annual International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 335–336). New York, NY, USA : ACM.
