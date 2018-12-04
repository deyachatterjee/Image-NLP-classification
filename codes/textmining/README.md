# Extract text from Pdf + text mining


## Extract text from Pdf using pdfminer
### Extract content from pdf
I compare  `PyPDF2` and `pdfminer` to extract text from pdf, but I prefer the latter one because of the more structured, less garbled text. [PDFMiner](https://github.com/pdfminer/pdfminer.six) is a tool for extracting information from PDF documents.

The scrips are available [here-pdfminer](https://github.com/weimin17/pdfminer-textmining-word2vec-img2vec/blob/master/codes/textmining/extract_context_Pdfminer.py) and [here-pypdf2](https://github.com/weimin17/pdfminer-textmining-word2vec-img2vec/blob/master/codes/textmining/extract_context_PyPDF2.py). Be careful, the python version is 2.7.

### Extract images from pdf

[extract_images_descripitions.py](https://github.com/weimin17/pdfminer-textmining-word2vec-img2vec/blob/master/codes/textmining/extract_images_descripitions.py)
## Text Mining

### Preprocessing
Including loading data, splitting into sentences, splitting into words, converting to lower case, removing all tokens that are not alphabetic, filtering out stopwords, etc. 
### Word2Vec
It belongs to word embedding, a kind of feature expression of text. The idea behind Word2Vec is pretty simple. Assuming you can tell the meaning of a word by the company words it keeps. This is analogous to the saying show me your friends, and I'll tell who you are. So if you have two words that have very similar neighbors (i.e. the usage context is about the same), then these words are probably quite similar in meaning or are at least highly related. For example, the words shocked,appalled and astonished are typically used in a similar context.
My blog [Embedding](https://weimin17.github.io/2017/10/Deep-Learning-Embedding/) introduces some details of word2vec.

Here we use `Gensim` to extract word2vec.
```
# python2.7
def word2vec(fpath):
    import logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    def read_input(input_file):
        """This method reads the input file, and do simple preprocess"""
        logging.info("reading file {0}...this may take a while".format(input_file))   
        with open (input_file, 'rb') as f:
            for i, line in enumerate(f): 
                if (i%1000==0):
                    logging.info("read {0} reviews".format(i))
                # do some pre-processing and return a list of words for each review text
                yield gensim.utils.simple_preprocess(line)

    # read the tokenized reviews into a list
    # each review item becomes a serries of words
    # so this becomes a list of lists
    documents = list(read_input(fpath))
    logging.info("Done reading data file")
    # build vocabulary and train model
    model = gensim.models.Word2Vec(documents, size=30, window=15, min_count=2, dbow_words=1, workers=10)
    model.train(documents, total_examples=len(documents), epochs=10)
```

Here are some parameters of `gensim.models.Word2Vec`.

```
    # The meaning of parameters
    model = gensim.models.Word2Vec (documents, size=150, window=10, min_count=2, workers=10)
    size
    The size of the dense vector to represent each token or word. If you have very limited data, then size should be a much smaller value. If you have lots of data, its good to experiment with various sizes. A value of 100-150 has worked well for me.
    
    window
    The maximum distance between the target word and its neighboring word. If your neighbor's position is greater than the maximum window width to the left and the right, then, some neighbors are not considered as being related to the target word. In theory, a smaller window should give you terms that are more related. If you have lots of data, then the window size should not matter too much, as long as its a decent sized window.
    
    min_count
    Minimium frequency count of words. The model would ignore words that do not statisfy the min_count. Extremely infrequent words are usually unimportant, so its best to get rid of those. Unless your dataset is really tiny, this does not really affect the model.
    
    workers
    How many threads to use behind the scenes?

    dbow_words
    if set to 1 trains word-vectors (in skip-gram fashion) simultaneous with DBOW doc-vector training; default is 0 (faster training of doc-vectors only).
```

The entire script is [here](https://github.com/weimin17/pdfminer-textmining-word2vec-img2vec/blob/master/codes/textmining/statistics1106.py)

Some useful links:
[Gensim Doc2Vec Tutorial](https://github.com/RaRe-Technologies/gensim/blob/develop/docs/notebooks/doc2vec-IMDB.ipynb)
[NLP Tutorials](https://github.com/kavgan/nlp-text-mining-working-examples)
