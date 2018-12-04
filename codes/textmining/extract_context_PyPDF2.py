"""
  PyPDF2
  Extract the whole context, including descriptions of images and whole context from breast.pdf
  2018.9.27 louis
"""

import PyPDF2
from PIL import Image
import re, os, shutil

import collections




def content_extract(file_name):
    '''
    extract context from pdf.
    return context as a list and generate context in txt files.
    '''
    pdf_file = open(os.path.join('../../data/',file_name), 'rb')
    file_name_nosuffix = file_name.split('.')[0]
    print(file_name_nosuffix)
    file_index = re.match('(\d*)(\D*)',file_name).group(1)
    # print(file_index)
    # print(pdf_file)
    
    PATH_TO_SAVE_EXTRACTIONS = os.path.join('../../save',file_name_nosuffix)
    # Create folder to save image & text
    if not os.path.exists(PATH_TO_SAVE_EXTRACTIONS):
        os.makedirs(PATH_TO_SAVE_EXTRACTIONS)
    else:
        pass
    
    
    # extract Image & Text from PDF
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    print("number_of_pages: "+ str(number_of_pages))
    
    # save the image description (texdt) into txt, the formation is :"file_index.page_number.image_number: text description"
    content_file = open(os.path.join(PATH_TO_SAVE_EXTRACTIONS, 'Raw_content.txt'),'w')
    # content_file.write('# save the image description (texdt) into txt, the formation is : "file_index.page_number.image_number: text description"\n')
    
    # extract image description (text) from PDF
    word = 'adenosis'
    m_word = 0 # the count that word occur
    n_word = 0
    for page_number in range(1,number_of_pages):
        page = read_pdf.getPage(page_number)
        page_content = page.extractText()
        # print(page_content)
        rc=re.compile(r'Figure\s\d*-\d*\n')
        figure_index = rc.findall(page_content)  #['Figure 19-1\n', 'Figure 19-2\n']
        book_content_raw = rc.split(page_content)

        # book_content = book_content_raw[0].replace('\n','')
        book_content = book_content_raw[0].replace('\n','')
        print(book_content)

        book_content = book_content.encode('ascii', 'ignore').decode('ascii')
        book_content = ''.join((str(file_index),'.',str(page_number+1),':\n',book_content))
        n_word += len(book_content)
        # print(book_content)
        # count
        frequency = collections.Counter(book_content.split())
        m_word += frequency[word]
        content_file.write(book_content+'\n')
        # print(book_content+'\n')
    
    content_file.close()
    pdf_file.close()
    print(n_word)

file_name = '19Breast.pdf'
content_extract(file_name)
