# Pathology Image Classification Assisting with NLP Classifier

The *Final Goal* is to classify pathology images, with the help of text descriptions to improve performance. The projects is still in progress.

## The work has been done

1. Use PdfMiner and PyPdf2 to extract text and images from pdf files [Here](https://github.com/weimin17/pdfminer-textmining-word2vec-img2vec/tree/master/codes/textmining)

2. NLP analysis: Implement text mining tutorials -- preprocessing and word2vec in Gensim and NLTK [Here](https://github.com/weimin17/pdfminer-textmining-word2vec-img2vec/tree/master/codes/textmining)

3. Img2Vec: Use pre-trained models (or do none pre-trained) in PyTorch to extract vector embeddings from any image and calculate their similarity. [Here](https://github.com/weimin17/pdfminer-textmining-word2vec-img2vec/tree/master/codes/img2vec)

## Part of the Reading list:

#### Datasets
1. `Images`: [ChestXray-NIHCC](https://nihcc.app.box.com/v/ChestXray-NIHCC)
[Descriptions](https://nihcc.app.box.com/v/ChestXray-NIHCC/file/220660789610)
`Reports`: [OpenI](https: //openi.nlm.nih.gov)(3,643 unique front view images and corresponding reports are selected)
*Paper Used that data*:
[TieNet_CVPR2018](http://www.cs.jhu.edu/~lelu/publication/TieNet_CVPR2018_spotlight.pdf), [ChestX-ray8_CVPR2017spotlight](https://arxiv.org/pdf/1705.02315.pdf)

2. `Images`: [Breast Cancer Histopathological Database (BreakHis)](https://web.inf.ufpr.br/vri/databases/breast-cancer-histopathological-database-breakhis/)
*Paper Used that data*:
·DEEP ATTENTIVE FEATURE LEARNING FOR HISTOPATHOLOGY IMAGE CLASSIFICATION
·[A Dataset for Breast Cancer Histopathological Image Classification](http://www.inf.ufpr.br/lesoliveira/download/TBME-00608-2015-R2-preprint.pdf) (present an evaluation of different combinations of six different visual feature descriptors along with different classifiers.)
·[Deep Features for Breast Cancer Histopathological Image Classification](http://www.inf.ufpr.br/lesoliveira/download/SpanholSMC2017.pdf)
·[Breast Cancer Histopathological Image Classification using Convolutional Neural Networks_IJCNN2016](http://www.inf.ufpr.br/lesoliveira/download/IJCNN2016-BC.pdf) -->present results from a CNN for this dataset. Given that CNNs generally require large datasets, they make use of the `random-patches trick`. With this approach, the results increases in about 4 to 6 percentage points in the accuracy.
·[Deep Learning for Magnification Independent Breast Cancer Histopathology Image Classification](https://ieeexplore.ieee.org/document/7900002)

3. `Reports`: [MIMIC](https://mimic.physionet.org/gettingstarted/dbsetup/)

4. `Images`:

The original H&E stained whole-slide images used in this work can be downloaded from the Genomic Data Commons. All TCGA molecular data can be obtained from the Genomic Data Commons, as well as derived data matrices of the PanCancer Atlas. Integration with immune signatures of the TCGA immune response working group is available through CRI iAtlas web resource. Links to these data resources can be found at the accompanying publication manuscript page (https://gdc.cancer.gov/about-data/publications/tilmap).
These different software resources as well as the tumor-infiltrating lymphocytes(TIL) maps are available on the Cancer Imaging Archive, at: https://doi.org/10.7937/K9/TCIA.2018.Y75F9W1
*Paper Used that data*:
Spatial Organization and Molecular Correlation of Tumor-Infiltrating Lymphocytes Using Deep Learning on Pathology Images

#### Papers
1. [TieNet:Text-Image Embedding Network for Common Thorax Disease Classification and Reporting in Chest X-rays_CVPR2018](http://www.cs.jhu.edu/~lelu/publication/TieNet_CVPR2018_spotlight.pdf)
[MyNotes](https://github.com/weimin17/weimin17.github.io/blob/master/images/%5BLearningNotes%5DTieNet%20Text-Image%20Embedding%20Network%20for%20Common%20Thorax%20Disease%20Classification%20and%20Reporting%20in%20Chest%20X-rays_2018CVPR.pdf)

[ChestX-ray8: Hospital-scale Chest X-ray Database and Benchmarks on Weakly-Supervised Classification and Localization of Common Thorax Diseases_CVPR2017spotlight](https://arxiv.org/pdf/1705.02315.pdf)
This paper, along with [TieNet] is written by a same team.

2. [Explainable Prediction of Medical Codes from Clinical Text](http://aclweb.org/anthology/N18-1100)
[MyNotes](https://github.com/weimin17/weimin17.github.io/blob/master/images/%5BLearningNotes%5DExplainable%20Prediction%20of%20Medical%20Codes%20from%20Clinical%20Text.pdf)

3. [Deep Visual-Semantic Alignments for Generating Image Descriptions(2015CVPR)](https://cs.stanford.edu/people/karpathy/cvpr2015.pdf)
[MyNotes](https://github.com/weimin17/weimin17.github.io/blob/master/images/%5BLearningNotes%5DDeep%20Visual-Semantic%20Alignments%20for%20Generating%20Image%20Descriptions_2015CVPR.pdf)
4. The following 3 papers are from the same team:
·[A Dataset for Breast Cancer Histopathological Image Classification](http://www.inf.ufpr.br/lesoliveira/download/TBME-00608-2015-R2-preprint.pdf)
[MyNotes](https://github.com/weimin17/weimin17.github.io/blob/master/images/%5BLearningNotes%5DA%20Dataset%20for%20Breast%20Cancer%20Histopathological%20Image%20Classification.pdf) -->present an evaluation of different combinations of six different visual feature descriptors along with different classifiers.
·[Deep Features for Breast Cancer Histopathological Image Classification](http://www.inf.ufpr.br/lesoliveira/download/SpanholSMC2017.pdf)
[MyNotes](https://github.com/weimin17/weimin17.github.io/blob/master/images/%5BLearningNotes%5DDeep%20Features%20for%20Breast%20Cancer%20Histopathological%20Image%20Classification.pdf)-->present an evaluation of `DeCaf` features for Breast Cancer recognition (image classification).
Results: The main observation is that the use of DeCAF features can generally achieve better results than 1. the use of more traditional visual feature descriptors, and 2. outperforming task-specific CNNs in some cases.
·[Breast Cancer Histopathological Image Classification using Convolutional Neural Networks_IJCNN2016](http://www.inf.ufpr.br/lesoliveira/download/IJCNN2016-BC.pdf) -->present results from a CNN for this dataset.  Given that CNNs generally require large datasets, they make use of the `random-patches trick`, which consists of extracting sub-images at both training and test phases. During training, the idea is to increase the training set by means of extracting patches at randomly-defined positions. And during test, patches are extracted from a grid, and after classifying each patch, their classification results are combined. The authors show that, with this approach, `increases in about 4 to 6 percentage points can be observed in the accuracy`.

5. Privileged information
[Deep Learning Under Privileged Information Using Heteroscedastic Dropout_CVPR2018](https://github.com/johnwlambert/dlupi-heteroscedastic-dropout)
we propose to utilize privileged information in order to control the variance of the Dropout. Since the Dropout’s variance is not constant, we call this a Heteroscedastic Dropout. Our empirical and theoretical analysis suggests that Heteroscedastic Dropout significantly increases the **sample efficiency** of **both CNNs and RNNs**, resulting in higher accuracy with much less data.
Heteroscedastic dropout - extend the LUPI from SVM-based methods to CNN/RNN-based methods
Utilize additional information during the training, in order to control the variance of the Dropout. Since the Dropout’s variance is not constant, it’s called Heteroscedastic Dropout.
Datasets - Pretrained CNN/RNN Models
[Learning to Rank Using Privileged Information](http://users.sussex.ac.uk/~nq28/pubs/ShaQuaLam13.pdf)


6. NLP for pathology
[Natural language processing in pathology: a scoping review_2016](https://www.ncbi.nlm.nih.gov/pubmed/27451435)
Reviewed and summarized the study objectives; NLP methods used and their validation(word/phrase matching, probabilistic machine learning and rule-based systems); software implementations; the performance on the dataset used and any reported use in practice. **a publishing date extending to Sep. 2014**
**little work has been done on breast pathology reports, given the high incidence of breast cancer.**
[The feasibility of using natural language processing to extract clinical information from breast
pathology reports](https://www.researchgate.net/publication/230764022_The_feasibility_of_using_natural_language_processing_to_extract_clinical_information_from_breast_pathology_reports)

7. [Deep Learning for Magnification Independent Breast Cancer Histopathology Image Classification](https://ieeexplore.ieee.org/document/7900002) --> proposed a method to classify the BC histopathology images, which is independent of the magnifications factors. Their experimental results are competitive with previous state-of-the-art results obtained from hand-crafted features.

8. vision-related work:
[Show, attend and tell: Neural image caption generation with visual attention_ICML2015](https://arxiv.org/pdf/1502.03044.pdf)
[Multi-level attention networks for visual question answering_CVPR2017](https://www.microsoft.com/en-us/research/wp-content/uploads/2017/06/Multi-level-Attention-Networks-for-Visual-Question-Answering.pdf)
[Pointer networks_NIPS2015Spotlight](https://arxiv.org/pdf/1506.03134.pdf)
[Areas of attention for image captioning_ICCV2017](https://arxiv.org/pdf/1612.01033.pdf)
[Dual attention networks for multimodal reasoning and matching_CVPR2017](https://arxiv.org/pdf/1611.00471.pdf) ------ [ChineseBlog](https://blog.csdn.net/mukvintt/article/details/80299301)

9. Medical-image-related:
[Learning to read chest X-rays: recurrent neural cascade model for automated image annotation_CVPR2016](https://arxiv.org/pdf/1603.08486.pdf)
[MDNet: a semantically and visually interpretable medical image diagnosis network_CVPR2017](https://arxiv.org/pdf/1707.02485.pdf)

10. NLP-related work:
[Neural machine translation by jointly learning to align and translate_ICLR2015](https://arxiv.org/pdf/1409.0473.pdf)

[Encoding source language with convolutional neural network for machine translation_ACL-CoNLL2015](https://arxiv.org/pdf/1503.01838.pdf)
[A neural attention model for abstractive sentence summarization_EMNLP2015](https://www.aclweb.org/anthology/D/D15/D15-1044.pdf)

[Not all contexts are created equal: Better word representations with variable attention_EMNLP2015](https://www.cs.cmu.edu/~ytsvetko/papers/emnlp15-attention.pdf)
[A structured self-attentive sentence embedding_ICLR2017](https://arxiv.org/pdf/1703.03130.pdf)
[Learning natural language inference using bidirectional LSTM model and inner-attention_2016](https://arxiv.org/pdf/1605.09090.pdf)


11. [BioNLP2017](https://aclanthology.coli.uni-saarland.de/sigs/sigbiomed)


12. [BioNLP2018WorkShop](https://aclanthology.coli.uni-saarland.de/events/ws-2018#W18-23)


13. Entity Recognition
 
14. [identifies key sentences in abstracts of oncological articles to aid evidence based medicine](http://aclweb.org/anthology/W18-2305)

15. [Extracting heart disease risk factors from clinical documents](http://aclweb.org/anthology/W18-2303)

16. [PICO abstract Element Detection](https://github.com/jind11/PubMed-PICO-Detection)

17. [Disease Phrase Matching](http://aclweb.org/anthology/W18-2315) - https://github.com/dhwajraj/

