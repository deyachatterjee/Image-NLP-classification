# -*- coding: utf-8 -*-
# @Date    : 2018-11-06 00:08:36
# @Author  : Weimin
# @Python  : 2.7
# Statistics with more structured corpus
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import nltk, re, pprint, os
from nltk import word_tokenize
import collections
from nltk.corpus import stopwords
import gensim

def preprocess(log_file,fpath):
    #load data
    raw = open(fpath, 'rb')
    raw_text = raw.read()
    raw.close()
    log_file.write('length of text%d\n'%len(raw_text)) #307672
    #split into sentences
    sents = nltk.sent_tokenize(raw_text)
    log_file.write('Counts of sentences:%d\n'%len(sents))
    # log_file.write(sents)

    #split into words
    tokens = word_tokenize(raw_text)
    log_file.write('Counts of Words after tokenizing:%d\n'%len(tokens)) #Counts of Words:53102
    log_file.write('%s\n'%tokens[:1000])
    log_file.write('\n')

    #convert to lower case
    tokens = [w.lower() for w in tokens]

    #remove all tokens that are not alphabetic
    words = []
    for word in tokens:
    	if len(word.split('.'))>1:
    		words += word.split('.')
    	else:
    		words.append(word)
    words = [word for word in words if word.isalpha()]


    log_file.write('Counts of Words after excluding alphabetic:%d\n'%len(words)) #Counts of Words:53102
    log_file.write('%s\n'%words[:1000])
    log_file.write('\n')

    #filter out stopwords
    stop_words = set(stopwords.words('english'))
    words_stops = [w for w in words if not w in stop_words]
    log_file.write('Counts of words after filtering out stopwords:%d\n'%len(words_stops)) #Counts of words after filtering out stopwords:25423
    log_file.write('%s\n'%words_stops[:1000])
    log_file.write('\n')

    return words


def word_count(text):
    '''word frequency'''
    word_freq = collections.defaultdict(int)
    for w in text:  
        word_freq[w] += 1
    return word_freq

def statistics(fpath,text):
	text_file = open(fpath,'w')
	terms=['benign', 'malignant','adenosis','fibroadenoma','phyllodes tumor', 'tumor', 'phyllodes', 'tubular adenoma', 'tubular', 'adenoma',
	'carcinoma','lobular carcinoma', 'lobular', 'mucinous carcinoma','mucinous','papillary carcinoma','papillary']
	word_fre = [] # word frequency
	sent_fre = [] # words occur in how many sentences
	for term in terms:
		text_file.write('_________________________________________\n')
		text_file.write('"%s" occurs in those sentences:\n'%(term))
		m_word = 0 # frequency of specific words
		m_sent = 0 # frequency of sentences that contain that specific word
		for description in text:
			frequency = collections.Counter(description.split())
			m_word += frequency[term]
			
			if frequency[term]!=0:
				m_sent += 1
				text_file.write(description+']\n')
		word_fre.append(m_word)
		sent_fre.append(m_sent)

		text_file.write('\n\n\n\n\n_________________________________________\n')		
		print(term+ ':' +str(m_word))
	
	# statistics info
	text_file.write('Total sentences:%d\n'%len(text))
	text_file.write('the frequency of words/the probability of words/frequency of sentences\n')
	for i,k in enumerate(terms):
		text_file.write('%s : %s / %s / %s\n'%(k,str(word_fre[i]),str(word_fre[i]/len(text)),sent_fre[i]))
		print(k,':',str(word_fre[i]),str(word_fre[i]/len(text)),sent_fre[i])

	text_file.close()



def word2vec(fpath):
    """
    read raw file and word2vec
    https://github.com/kavgan/nlp-text-mining-working-examples/tree/master/word2vec
    """
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
    """
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
    #if set to 1 trains word-vectors (in skip-gram fashion) simultaneous with DBOW doc-vector training; default is 0 (faster training of doc-vectors only).
    """
    model = gensim.models.Word2Vec(
        documents,
        size=30,
        window=15,
        min_count=2,
        dbow_words=1,
        workers=10)
    model.train(documents, total_examples=len(documents), epochs=10)

    return model

if __name__ == '__main__':
    # # preprocess
    # fpath = '../../save/19Breast/pdfminer/Raw_content_pdfminer_norefer.txt'
    # log_file = open('../../save/19Breast/pdfminer/stat_log1106.txt','w')
    # text = preprocess(log_file, fpath)
    # word_freq = word_count(text)
    # log_file.write('Number of words:%d\n'%len(word_freq))
    # log_file.write('%s\n'%word_freq)

    # # word_count
    # log_file1 = open('../../save/19Breast/pdfminer/word_count1106.txt','w')
    # for key, value in sorted(word_freq.items(),key=lambda e:e[1],reverse=True):
    # 	log_file1.write('%s:%s\n'%(str(key),str(value)))
    # log_file1.close()

    # # statistics
    # fpath = os.path.join('../../save/19Breast/pdfminer', 'stat_cont1106.txt')
    # statistics(fpath, text)
    # log_file.close()

    # word2vec
    fpath = '../../save/19Breast/pdfminer/Raw_content_pdfminer_norefer.txt'
    model = word2vec(fpath)
    word=['patient', 'disease', 'benign','malignant','adenosis','fibroadenoma', 'tumor', 'phyllodes', 'tubular', 'adenoma',
    'carcinoma', 'lobular','mucinous','papillary']
    for w1 in word:
        print(w1)
        print(model.wv.most_similar (positive=w1,topn=6))





