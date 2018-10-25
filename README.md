# Query-based summarization
A set set of query-based summarization baseline algorithms

## Requirements
Requires Anaconda Python 3 distribution.
Use the following procedure to install all requirements:

1. Download and install the Anaconda Python distribution from the [Anaconda website](https://www.anaconda.com/).

2. Create new virtual environment:
```
cd query_based_summarization
conda env create
```

## Usage
To activate this environment, use:
```
source activate qbmd
```

Launch Jupyter to manage and execute notebooks:
```
jupyter notebook
```

Press `CTRL+C` to stop execution.

To deactivate an active environment, use:
```
source deactivate
```

To remove the environment, use:
```
conda remove -y -n qbmd --all
```

To update the environment, use:
```
conda env update -n qbmd -f environment.yml
```


## References
Original papers of baseline algorithms:
- **MMR**: Carbonell, J. & Goldstein, J. (1998). [The Use of MMR, Diversity-based Reranking for Reordering Documents and Producing Summaries](https://dl.acm.org/citation.cfm?id=291025). *Proceedings of he 21st Annual International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 335–336). New York, NY, USA : ACM.