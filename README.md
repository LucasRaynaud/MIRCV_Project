# MIRCV Project

## Runnable files
- inverted_index.ipynb : notebook reading the msmarco collection and saving into files the inverted index, the lexicon and the document table.
- main.py : querying script asking for type  query and the number of documents you want to see with their scores
- ranking_evaluation.ipynb : notebook used for testing the system with the **TREC DL 2020**

## Requirements
### Files
```
├── src
├── data
   ├── msmarco
   │   ├── collection.tar.gz
   ├── test_queries
	   ├── 2020qrels-pass.txt
	   ├── msmarco-test2020-queries.tsv
```
*collection.tar.gz*, *2020qrels-pass.txt* and *msmarco-test2020-queries.tsv* are not included in the repository.
### Packages
All the programs where made using Python. 
For installing all the packages needed : ```pip install -r requirements.txt ```
