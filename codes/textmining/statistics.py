# -*- coding: utf-8 -*-
# @Date    : 2018-10-29
# @Author  : Weimin
# @Python  : 3.6
# Eight subsubjects of benign and malignant from BreakHis Database
# Statistical info from "19breast.pdf" file, like frequency.

from __future__ import division
import PyPDF2
from PIL import Image
import re, os, shutil
import collections
from gensim.models import Word2Vec
import gensim


def description_extract(file_name):
    '''
    extract images and descriptions from pdf.
    return descriptions as a list.
    generate iamge files and save descriptions in txt files.
    '''
    pdf_file = open(os.path.join('../../data/',file_name), 'rb')
    file_name_nosuffix = file_name.split('.')[0]
    print(file_name_nosuffix)
    file_index = re.match('(\d*)(\D*)',file_name).group(1)
    
    PATH_TO_SAVE_EXTRACTIONS = os.path.join('../../save',file_name_nosuffix)
    # Create folder to save image & text
    if not os.path.exists(PATH_TO_SAVE_EXTRACTIONS):
        os.makedirs(PATH_TO_SAVE_EXTRACTIONS)
    else:
        pass
    
    # extract descriptions from PDF
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    print("number_of_pages: "+ str(number_of_pages))
    
    # save the image description (texdt) into txt, the formation is :"file_index.page_number.image_number: text description"
    text_file = open(os.path.join(PATH_TO_SAVE_EXTRACTIONS, 'description.txt'),'w')
    description_list = []
    # extract image description (text) from PDF
    for page_number in range(number_of_pages):
        page = read_pdf.getPage(page_number)
        page_content = page.extractText()
        rc=re.compile(r'Figure\s\d*-\d*\n')
        figure_index = rc.findall(page_content)
        figure_rawcontent = rc.split(page_content)
        for i in range(len(figure_index)):
            figure_content = (figure_index[i] + figure_rawcontent[i+1]).replace('\n','')
            figure_content = figure_content.encode('ascii', 'ignore').decode('ascii')
            figure_content = ''.join(figure_content)
            text_file.write(figure_content+'\n')
            # append splited description into one list
            description_list.append(figure_content)

    text_file.close()
    pdf_file.close()
    return description_list # list

def content_extract(file_name):
    '''
    extract context from pdf.
    return context as a list and generate context in txt files.
    '''
    pdf_file = open(os.path.join('../../data/',file_name), 'rb')
    file_name_nosuffix = file_name.split('.')[0]
    file_index = re.match('(\d*)(\D*)',file_name).group(1)
   
    
    # extract Image & Text from PDF
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    #print("number_of_pages: "+ str(number_of_pages))
    
    # save the context into txt
    PATH_TO_SAVE_EXTRACTIONS = os.path.join('../../save',file_name_nosuffix)
    content_file = open(os.path.join(PATH_TO_SAVE_EXTRACTIONS, 'content.txt'),'w')
    
    # extract image description (text) from PDF
    content_list = ''

    for page_number in range(1,71):
        page = read_pdf.getPage(page_number)
        page_content = page.extractText()
        # print(page_content)
        rc=re.compile(r'Figure\s\d*-\d*\n')
        figure_index = rc.findall(page_content)  #['Figure 19-1\n', 'Figure 19-2\n']
        book_content_raw = rc.split(page_content)
        book_content = book_content_raw[0].replace('\n','')
        #book_content = book_content_raw[0].replace('\t','').replace('\v','').replace('\r','').replace('\f','').replace('\n','')


        # exclude footprint
        rc_foot1=re.compile(r'BREAST ˜ \d*')
        rc_foot2=re.compile(r'\d ˜ BREAST')
        book_content_foot1 = rc_foot1.split(book_content)
        book_content_foot2 = rc_foot2.split(book_content)
        if len(book_content_foot1)>1:
        	book_content = book_content_foot1[1]
        if len(book_content_foot2)>1:
        	book_content = book_content_foot2[1]

        book_content = book_content.encode('ascii', 'ignore').decode('ascii')
        content_list = ''.join((content_list, book_content))

        content_file.write(book_content+'\n')
    
    content_file.close()
    pdf_file.close()
    return content_list

def statistics(text_file,text):
	"""statistics information"""
	word=['benign','Begign','BEGIGN', 'malignant','adenosis','fibroadenoma','phyllodes tumor', 'tumor', 'phyllodes', 'tubular adenoma', 'tubular', 'adenoma',
	'carcinoma','lobular carcinoma', 'lobular', 'mucinous carcinoma','mucinous','papillary carcinoma','papillary']
	word_fre = [] # word frequency
	sent_fre = [] # words occur in how many sentences
	for term in word:
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
		print('The frequency of '+term+ ':' +str(m_word))
	
	# statistics info
	text_file.write('Total sentences:%d\n'%len(text))
	text_file.write('the frequency of words/the probability of words/frequency of sentences\n')
	for i,k in enumerate(word):
		text_file.write('%s : %s / %s / %s\n'%(k,str(word_fre[i]),str(word_fre[i]/len(text)),sent_fre[i]))
		print(k,':',str(word_fre[i]),str(word_fre[i]/len(text)),sent_fre[i])

	text_file.close()


def description_stat(text):
	"""Input List"""

	# save the results to file
	text_file = open(os.path.join('../../save/19Breast/', 'stat_des.txt'),'w')
	statistics(text_file,text)


def content_stat(text):
	"""Input list"""
	# save the results to file
	text_file = open(os.path.join('../../save/19Breast/', 'stat_cont.txt'),'w')
	statistics(text_file,text)


# def preprocess(input_text):
# 	"""Preprocess"""

#     # remove parenthesis 
#     input_text_noparens = re.sub(r'\([^)]*\)', '', input_text)
#     sentences_strings_ted = []
#     for line in input_text_noparens.split('\n'):
#         m = re.match(r'^(?:(?P<precolon>[^:]{,20}):)?(?P<postcolon>.*)$', line)
#         sentences_strings_ted.extend(sent for sent in m.groupdict()['postcolon'].split('.') if sent)
#     # store as list of lists of words
#     sentences_ted = []
#     for sent_str in sentences_strings_ted:
#         tokens = re.sub(r"[^a-z0-9]+", " ", sent_str.lower()).split()
#         sentences_ted.append(tokens)

#     return sentences_ted

def word2vec_sim(input_text,save_file):
	"""
	word2vec, using Gensim.
	wordembedding
	Input text: list.
    # https://towardsdatascience.com/word-embedding-with-word2vec-and-fasttext-a209c1d3e12c
    # https://www.kaggle.com/alvations/word2vec-embedding-using-gensim-and-nltk
    # https://machinelearningmastery.com/develop-word-embeddings-python-gensim
    """
	sentences_ted=[]
	for line in input_text:
		sentences_ted.append(gensim.utils.simple_preprocess(line))

	# sentences_ted = preprocess(input_text)
	# sentences_ted = gensim.utils.simple_preprocess(input_text)
	# tokenize
	#sentences_ted = gensim.utils.tokenize(input_text, lowercase=True)
	# print(sentences_ted)
	print(len(sentences_ted))
	model_ted = Word2Vec(sentences=sentences_ted, size=100, window=5, min_count=2, workers=4, sg=0)
	model_ted.save(os.path.join("../../save/19Breast/",save_file+'.model'))
	return model_ted





file_name = '19Breast.pdf'
description_list = description_extract(file_name)
# print(len(description_list))
# print(description_list)
content_bytes = content_extract(file_name) # char
print(len(content_bytes))


#print(len(content_bytes.split('.')))
#description_stat(description_list)
#content_stat(content_bytes.split('.'))

#print(content_bytes.split('.'))

description_bytes = ''
for line in description_list:
	description_bytes += line
print(len(description_bytes))

model_des = word2vec_sim(description_list,'des_word2vec')
model_cont = word2vec_sim(content_bytes.split('.'),'cont_without_refers_word2vec')
print(model_des)
print(model_cont)

# # model_des = Word2Vec.load('../save/19Breast/des_word2vec.model')
# # # summarize the loaded model
# # print(model_des)
# # # summarize vocabulary
# words = list(model_des.wv.vocab)
# print(len(words))
# # access vector for one word
# print(model_des['adenosis'])


