# dspy-arxiv

Explore the use of [DSPy](https://github.com/stanfordnlp/dspy) for extracting features from PDFs.
This repository provides a simple example of how to use this framework to predict the sub-category of a Computer Science paper from arXiv.

## Suggested Installation

1. Clone this repository.
2. Create a virtual environment.
3. Install dependencies from *requirements.txt*.
4. Install the virtual environment as a Jupyter kernel.

## Build Dataset & Database

The **dataset** is a selection of 150 arXiv papers (metadata + pdf) from the computer science category.

To build the database:

1. Download the JSON file from [Kaggle](https://www.kaggle.com/datasets/Cornell-University/arxiv) into the `dspy-arxiv` directory.
2. Rename the file to `arxiv.json`.
3. Run the notebook `data.ipynb` from top to bottom.

At the end, you should have two directories:
- *dspy-arxiv/database*
  - *arxiv.json* - the original JSON file with only the computer science category
- *dspy-arxiv/dataset*
  - *trainset* - 50 JSON files with metadata + text used for "training"
  - *valset* - 50 JSON files with metadata + text used for "validation"
  - *testset* - 50 JSON files with metadata + text used for "testing"

> If you want to add RAG to the pipeline, it's handy to have the data in a vector database for fast retrieval.
> Check out *database.py* for an example script to set up [chromadb](https://docs.trychroma.com/) and populate it with arXiv metadata.

## Features Extraction

The notebook *features.ipynb* can be seen as a simple tutorial on how to use DSPy to programmatically prompt LLM for feature extraction (in this case, predicting the sub-category of a Computer Science paper from arXiv).

You can also take a look at the [slides](https://s1m0n38.github.io/dspy-arxiv/#/) generated from this notebook.
