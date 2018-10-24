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

## Install NLTK packages
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