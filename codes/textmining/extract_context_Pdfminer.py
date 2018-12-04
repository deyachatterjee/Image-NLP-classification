#-*- coding: utf-8 -*-
# @Date    : 2018-11-05 14:13:36
# @Author  : Weimin
# @Python  : 2.7
# PdfMiner to extract text from pdf. It extract context, captions, and headings from the pdf files.


# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer, os, re

"""
# Info of fontname:
                                #Figure captions
                                #fontname ICPGAH+Helvetica(ABC) implies more than one images
                                #XBHXCD+BrandingSans-Bold(Figure  19-9  n  ,也可能不是，而是以A,B,开头)
                                #fontname NEEPSX+BrandingSans-Roman(after Figure)
                                
                                
                                #fontname NEEPSX+BrandingSans-Light (页眉右BREast  n  554)
                                #fontname CDRBUT+Berkeley-Black(页眉左:551  n  BREast)
                                #fontname CDRBUT+ZapfDingbats(n  549页脚)
                    
                                #第一页目录
                                #fontname NEEPSX+BrandingSans-Light(chapter)
                                #fontname NEEPSX+BrandingSans-SemiBold(1)
                                #fontname NEEPSX+BrandingSans-Roman(2)
                                #正文目录
                                #fontname NEEPSX+BrandingSans-Black(context:1)有可能两行
                                #fontname XBHXCD+BrandingSans-Bold(context:2)
                                #fontname ICPGAH+BrandingSansItalic-SemiBold(context:3)
                                #fontname SESOKN+BrandingSans-SemiBold-SC800(context:4)
                                #fontname SESOKN+BrandingSansItalic-Roman(context:5)
                                #fontname SBTYKN+Berkeley-Medium(context)
                                #fontname XBHXCD+Berkeley-Italic(斜体)
                                #fontname XBHXCD+Symbol(the beginning is "+", only one line)
                                #list
                                #fontname CDRBUT+ZapfDingbats(page559)
                                #fontname SBTYKN+Berkeley-Medium(after项目符号)

                                
                                #CDRBUT+Berkeley-Bold
                                
                                #Table
                                #fontname XBHXCD+BrandingSans-Bold(Table caption)
                                #NCDKSX+BrandingSansItalic-Bold(page71 table subcaption)
"""
def createPDFDoc(fpath):
    fp = open(fpath, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser, password='')
    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise "Not extractable"
    else:
        return document


def createDeviceInterpreter():
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    return device, interpreter


def parse_obj_context(objs):
    content_text = '' #context divided by pages
    prefonttype = ['a']
    curfonttype = ['a']
    for obj in objs:
        if isinstance(obj, pdfminer.layout.LTTextBox):
            for o in obj._objs:
                if isinstance(o,pdfminer.layout.LTTextLine):
                    text=o.get_text()
                    if text.strip():
                        for c in  o._objs:
                            if isinstance(c, pdfminer.layout.LTChar):
                                #print("fontname %s"%c.fontname)
                                #print(text)
                                #text = text.encode('ascii', 'ignore').decode('ascii')
                                #extract caption according to font
                                curfonttype.append(c.fontname)
                                if c.fontname == 'NEEPSX+BrandingSans-Black': #caption:1
                                    # combine caption1 into one line if there are two lines
                                    if prefonttype[-1] != 'NEEPSX+BrandingSans-Black':
                                        content_text += '\n****************\n' + text + '****************\n'
                                    elif curfonttype[-1] == prefonttype[-1]:
                                        content_text = content_text[:-18] + text + '****************\n'

                                if c.fontname == 'XBHXCD+BrandingSans-Bold': #caption:2
                                    # The figure has the same feature, exclude them
                                    rc=re.compile(r'^Figure\s+\d+-\d+|^\w,')
                                    if rc.match(text):
                                        pass
                                    else:
                                        # combine caption3 into one line if there are two lines
                                        if prefonttype[-1] != 'XBHXCD+BrandingSans-Bold':
                                            content_text += '\n&&&&&&&&&&&&&&&&\n' + text + '&&&&&&&&&&&&&&&&\n'
                                        elif curfonttype[-1] == prefonttype[-1]:
                                            content_text = content_text[:-18] + text + '&&&&&&&&&&&&&&&&\n'
                                            #content_text += '&&&&&&&&&&&&&&&&\n' + text + '&&&&&&&&&&&&&&&&\n'
                                if c.fontname == 'ICPGAH+BrandingSansItalic-SemiBold': #caption:3
                                    # combine caption3 into one line if there are two lines
                                    if prefonttype[-1] != 'ICPGAH+BrandingSansItalic-SemiBold':
                                        content_text += '\n################\n' + text + '################\n'
                                    elif curfonttype[-1] == prefonttype[-1]:
                                        content_text = content_text[:-18] + text + '################\n'
                                if c.fontname == 'SESOKN+BrandingSans-SemiBold-SC800': #caption:4
                                    # combine caption4 into one line if there are two lines
                                    if prefonttype[-1] != 'SESOKN+BrandingSans-SemiBold-SC800':
                                        content_text += '\n$$$$$$$$$$$$$$$$\n' + text + '$$$$$$$$$$$$$$$$\n'
                                    elif curfonttype[-1] == prefonttype[-1]:
                                        content_text = content_text[:-18] + text + '$$$$$$$$$$$$$$$$\n'
                                if c.fontname == 'SESOKN+BrandingSansItalic-Roman': #caption:5
                                    # combine caption3 into one line if there are two lines
                                    if prefonttype[-1] != 'SESOKN+BrandingSansItalic-Roman':
                                        content_text += '\n^^^^^^^^^^^^^^^^\n' + text + '^^^^^^^^^^^^^^^^\n'
                                    elif curfonttype[-1] == prefonttype[-1]:
                                        content_text = content_text[:-18] + text + '^^^^^^^^^^^^^^^^\n'




                                if (c.fontname == 'SBTYKN+Berkeley-Medium') or (c.fontname == 'XBHXCD+Berkeley-Italic') or (c.fontname == 'XBHXCD+Symbol'):#caption
                                    rc = re.compile(r'-$')
                                    rc_p = re.compile(r'\.$|\.\d*$|\.\d*-\d*$|\.(\d*,)*(\d*-\d*,)*(\d*,)*(\d*-\d*,)*(\d*,)*(\d*)*(\d*-\d*)*$')
                                    #split '-' in the end of lines
                                    if len(rc.findall(text)) != 0:
                                    # if rc.match(text):
                                    	# print(u'-')
                                    	content_text += rc.split(text)[0]
                                    	#print(rc.split(text)[0])
                                    #split paragraphs
                                    elif len(rc_p.findall(text)) != 0:
                                        content_text += text # that's a paragraph
                                    else:
                                        content_text += text.replace('\n','')
                                if c.fontname == 'CDRBUT+ZapfDingbats': #list
                                    rc = re.compile(r'^n\s*\d*$')
                                    # exclude footpage
                                    if len(rc.findall(text)) == 0:
                                        rc = re.compile(r'-$')
                                        rc_p = re.compile(r'\.$|\.\d*$|\.(\d*,)*\d*$|\.\d*-\d*$')
                                        #split '-' in the end of lines
                                        if len(rc.findall(text)) != 0:
                                            content_text += '\n' + rc.split(text)[0]
                                        #split paragraphs
                                        elif len(rc_p.findall(text)) != 0:
                                            content_text += '\n' + text # that's a paragraph
                                        else:
                                            content_text += '\n' + text.replace('\n','')
                                prefonttype.append(c.fontname)
                                break
        # if it's a container, recurse
        elif isinstance(obj, pdfminer.layout.LTFigure):
            parse_obj_context(obj._objs)
        else:
            pass
    return content_text.replace('  ',' ')

def pdf2txt_context(fpath,sname):
    document=createPDFDoc(fpath)
    device,interpreter=createDeviceInterpreter()
    pages=PDFPage.create_pages(document) #pages: <class 'generator'>
    # print(type(pages))
    
    # save the image description (texdt) into txt, the formation is :"file_index.page_number.image_number: text description"
    PATH_TO_SAVE_EXTRACTIONS = os.path.join('../../save/19Breast/pdfminer')
    content_file = open(os.path.join(PATH_TO_SAVE_EXTRACTIONS, sname),'w')
    for i, page in enumerate(pages):
        interpreter.process_page(page)
        layout = device.get_result()
        #content_file.write('\n%s:\n'%(i+1)) #record page number
        content_text = parse_obj_context(layout._objs)
        content_file.write(content_text)
    content_file.close()

def parse_obj_heading(objs):
    '''extract heading of chapter'''
    content_text = '' #context divided by pages
    prefonttype = ['a']
    curfonttype = ['a']
    for obj in objs:
        if isinstance(obj, pdfminer.layout.LTTextBox):
            for o in obj._objs:
                if isinstance(o,pdfminer.layout.LTTextLine):
                    text=o.get_text()
                    if text.strip():
                        for c in  o._objs:
                            if isinstance(c, pdfminer.layout.LTChar):
                                #print("fontname %s"%c.fontname)
                                #text = text.encode('ascii', 'ignore').decode('ascii')
                                #extract heading according to font
                                curfonttype.append(c.fontname)
                                if c.fontname == 'NEEPSX+BrandingSans-Black': #heading:1
                                    # combine heading1 into one line if there are two lines
                                    if prefonttype[-1] != 'NEEPSX+BrandingSans-Black':
                                        content_text += '1:' + text
                                    elif curfonttype[-1] == prefonttype[-1]:
                                        content_text = content_text[:-1] + text + '\n'

                                if c.fontname == 'XBHXCD+BrandingSans-Bold': #heading:2
                                    # The figure has the same feature, exclude them
                                    rc=re.compile(r'^Figure\s+\d+-\d+|^\w,')
                                    if rc.match(text):
                                        break
                                    else:
                                        # combine heading2 into one line if there are two lines
                                        if prefonttype[-1] != 'XBHXCD+BrandingSans-Bold':
                                            content_text += '2:' + text
                                        elif curfonttype[-1] == prefonttype[-1]:
                                            content_text = content_text[:-1] + text + '\n'
                                if c.fontname == 'ICPGAH+BrandingSansItalic-SemiBold': #heading:3
                                    # combine heading3 into one line if there are two lines
                                    if prefonttype[-1] != 'ICPGAH+BrandingSansItalic-SemiBold':
                                        content_text += '3:' + text
                                    elif curfonttype[-1] == prefonttype[-1]:
                                        content_text = content_text[:-1] + text + '\n'
                                if c.fontname == 'SESOKN+BrandingSans-SemiBold-SC800': #heading:4
                                    # combine heading4 into one line if there are two lines
                                    if prefonttype[-1] != 'SESOKN+BrandingSans-SemiBold-SC800':
                                        content_text += '4:' + text
                                    elif curfonttype[-1] == prefonttype[-1]:
                                        content_text = content_text[:-1] + text + '\n'
                                if c.fontname == 'SESOKN+BrandingSansItalic-Roman': #heading:5
                                    # combine heading5 into one line if there are two lines
                                    if prefonttype[-1] != 'SESOKN+BrandingSansItalic-Roman':
                                        content_text += '5:' + text
                                    elif curfonttype[-1] == prefonttype[-1]:
                                        content_text = content_text[:-1] + text + '\n'
                                prefonttype.append(c.fontname)
                                break
                               
        # if it's a container, recurse
        elif isinstance(obj, pdfminer.layout.LTFigure):
            parse_obj_heading(obj._objs)
        else:
            pass
    return content_text.replace('  ',' ').replace('\n\n','\n')

def pdf2txt_heading(fpath,sname):
    '''extract heading of the chapter'''
    document=createPDFDoc(fpath)
    device,interpreter=createDeviceInterpreter()
    pages=PDFPage.create_pages(document) #pages: <class 'generator'>
    
    # save the image description (texdt) into txt, the formation is :"file_index.page_number.image_number: text description"
    PATH_TO_SAVE_EXTRACTIONS = os.path.join('../../save/19Breast/pdfminer')
    content_file = open(os.path.join(PATH_TO_SAVE_EXTRACTIONS, sname),'w')
    for i, page in enumerate(pages):
        interpreter.process_page(page)
        layout = device.get_result()
        #content_file.write('\n%s:\n'%(i+1)) #record page number
        content_text = parse_obj_heading(layout._objs)
        content_file.write(content_text)
    content_file.close()

                                #fontname ICPGAH+Helvetica(ABC) implies more than one images
                                #XBHXCD+BrandingSans-Bold(Figure  19-9  n  ,也可能不是，而是以A,B,开头)
                                #fontname NEEPSX+BrandingSans-Roman(after Figure)
def parse_obj_captions(objs):
    '''extract captions of images'''
    caption_text = '' #captions divided by pages
    prefonttype = ['a']
    curfonttype = ['a']
    for obj in objs:
        if isinstance(obj, pdfminer.layout.LTTextBox):
            for o in obj._objs:
                if isinstance(o,pdfminer.layout.LTTextLine):
                    text=o.get_text()
                    if text.strip():
                        for c in  o._objs:
                            if isinstance(c, pdfminer.layout.LTChar):
                                #print("fontname %s"%c.fontname)
                                #text = text.encode('ascii', 'ignore').decode('ascii')
                                #extract heading according to font
                                curfonttype.append(c.fontname)


                                if c.fontname == 'XBHXCD+BrandingSans-Bold': #figure captions
                                    # The figure has the same feature, exclude them
                                    rc=re.compile(r'^Figure\s+\d+-\d+\s+n|^\w,')
                                    if rc.match(text):
                                        rc = re.compile(r'-$')
                                        rc_p = re.compile(r'\.$|\.\d*$|\.\d*-\d*$|\.(\d*,)*(\d*-\d*,)*(\d*,)*(\d*-\d*,)*(\d*,)*(\d*)*(\d*-\d*)*$')
                                        #split '-' in the end of lines
                                        if len(rc.findall(text)) != 0:
                                        # if rc.match(text):
                                            # print(u'-')
                                            caption_text += '\n' + rc.split(text)[0]
                                            #print(rc.split(text)[0])
                                        #split paragraphs
                                        elif len(rc_p.findall(text)) != 0:
                                            caption_text += '\n' + text # that's a paragraph
                                        else:
                                            caption_text += '\n' + text.replace('\n','')


                                if c.fontname == 'NEEPSX+BrandingSans-Roman': #captions:2rd lines
                                    # combine heading3 into one line if there are two lines
                                    # if prefonttype[-1] == 'XBHXCD+BrandingSans-Bold':
                                    rc = re.compile(r'-$')
                                    rc_p = re.compile(r'\.$|\.\d*$|\.\d*-\d*$|\.(\d*,)*(\d*-\d*,)*(\d*,)*(\d*-\d*,)*(\d*,)*(\d*)*(\d*-\d*)*$')
                                    #split '-' in the end of lines
                                    if len(rc.findall(text)) != 0:
                                    # if rc.match(text):
                                        # print(u'-')
                                        caption_text += rc.split(text)[0]
                                        #print(rc.split(text)[0])
                                    #split paragraphs
                                    elif len(rc_p.findall(text)) != 0:
                                        caption_text += text # that's a paragraph
                                    else:
                                        caption_text += text.replace('\n','')


                                prefonttype.append(c.fontname)
                                break
                               
        # if it's a container, recurse
        elif isinstance(obj, pdfminer.layout.LTFigure):
            parse_obj_captions(obj._objs)
        else:
            pass
    return caption_text.replace('  ',' ').replace('\n\n','\n')

def pdf2txt_images(fpath,sname):
    '''extract captions of the images'''
    document=createPDFDoc(fpath)
    device,interpreter=createDeviceInterpreter()
    pages=PDFPage.create_pages(document) #pages: <class 'generator'>
    
    # save the image description (texdt) into txt, the formation is :"file_index.page_number.image_number: text description"
    PATH_TO_SAVE_EXTRACTIONS = os.path.join('../../save/19Breast/pdfminer')
    content_file = open(os.path.join(PATH_TO_SAVE_EXTRACTIONS, sname),'w')
    for i, page in enumerate(pages):
        interpreter.process_page(page)
        layout = device.get_result()
        #content_file.write('\n%s:\n'%(i+1)) #record page number
        content_text = parse_obj_captions(layout._objs)
        content_file.write(content_text)
    content_file.close()



if __name__ == '__main__':
    fpath = os.path.join('../../data/19Breast.pdf')
    # content 
    # sname = 'Raw_content_pdfminer_content.txt'
    # pdf2txt_context(fpath, sname)

    # headings
    # hname = 'Raw_content_pdfminer_heading.txt'
    # pdf2txt_heading(fpath, hname)

    # captions of figures
    sname = 'Raw_captions_pdfminer_captions.txt'
    pdf2txt_images(fpath, sname)







