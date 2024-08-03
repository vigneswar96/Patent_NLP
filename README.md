# Patent_NLP
This is a work repository. Specifically for documenting the daily thesis work. 

#######################################################################################


What are the advancements made so far in this area? 

The project aims to develop advanced Natural Language Processing techniques for analyzing and processing patent documents, improving efficiency in patent search, classification, and information extraction.
Key Techniques Used:

Text Extraction and Preprocessing:

<img src="https://github.com/vigneswar96/Patent_NLP/blob/main/PDF_file_icon.svg.png" width="100" alt="Patent NLP Overview">

Optical Character Recognition (OCR) for scanned patent documents
PDF parsing for digital documents
Text cleaning and normalization techniques

![Alt text](./images.png)

# Information Extraction:

Regular expressions for structured data extraction (e.g., patent numbers, dates)
Rule-based systems for domain-specific entity extraction
Conditional Random Fields (CRF) for sequence labeling tasks


# Advanced NLP Models:

While BERT and other transformer models are powerful:

Domain-specific word embeddings trained on patent corpora
Long Short-Term Memory (LSTM) networks for sequential data processing
Attention mechanisms for focusing on relevant parts of patent text




# Unsupervised Learning:

Topic modeling techniques like Latent Dirichlet Allocation (LDA) for identifying key themes in patent documents
Word2Vec or FastText for creating word embeddings specific to patent language


# Graph-based Approaches:

Constructing knowledge graphs from patent data
Graph neural networks for patent similarity and recommendation

# What are the models used here? 

BERT
The model uses 

Paecter






# Challenges:

Domain Complexity: Patents often contain highly technical and specialized language, making general-purpose NLP models less effective.

Document Structure: Patents have a unique structure that can be challenging to parse and extract information from consistently.

Data Quality: Dealing with OCR errors, inconsistent formatting, and historical documents can affect the quality of extracted information.

Scalability: Processing large volumes of patent data efficiently while maintaining accuracy.

Multilingual Processing: Patents are filed in multiple languages, requiring robust multilingual NLP capabilities.

Legal Implications: Ensuring the accuracy of extracted information is crucial due to the legal nature of patents.

Temporal Dynamics: Patent language and technology evolve over time, requiring models that can adapt to these changes.

Handling of Images and Diagrams: Extracting and interpreting information from non-textual elements in patents.

