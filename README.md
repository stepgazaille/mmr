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
To activate the project's virtual environment, use:
```
source activate qbmd
```

To launch Jupyter to manage and execute notebooks, use:
```
jupyter notebook
```
Press `CTRL+C` to stop execution.

To deactivate the project's virtual environment, use:
```
source deactivate
```

To remove the project's virtual environment, use:
```
conda remove -y -n qbmd --all
```

To update the project's virtual environment, use:
```
conda env update -n qbmd -f environment.yml
```




## Install NLTK packages
Some NLTK packages are required to execute the demo.
To install all NLTK packages:
1. Activate the virtual environment.
2. Open the Python interpreter by typing the following command in the terminal: `python`
3. Excute the following command in the Python interpreter:
```
import nltk
nltk.download()
```
The "NLTK Downloader" window will appear.
4. Select the "All packages" option.
5. Click on the "Download" button and wait for download completion.
6. Close the "NLTK Downloader" window.
7. Close the Python interpreter by typing the following command in the terminal: quit()





## Test corpus
A small corpus built using articles from [The Guardian](https://www.theguardian.com/international) is provided for development and testing.


## References
Original papers of baseline algorithms:
- **MMR**: Carbonell, J. & Goldstein, J. (1998). [The Use of MMR, Diversity-based Reranking for Reordering Documents and Producing Summaries](https://dl.acm.org/citation.cfm?id=291025). *Proceedings of he 21st Annual International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 335–336). New York, NY, USA : ACM.