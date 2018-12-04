"""
  PyPDF2
  Extract images and descriptions from breast.pdf
  2018.9.27 louis
"""

import PyPDF2
from PIL import Image
import re, os, shutil



def image_text_extract(file_name):
    '''
    extract images and descriptions from pdf.
    return descriptions as a list.
    generate iamge files and save descriptions in txt files.
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
        # delete all existed files
        #shutil.rmtree(PATH_TO_SAVE_EXTRACTIONS)
        #os.makedirs(PATH_TO_SAVE_EXTRACTIONS)
        pass
    
    
    # extract Image & Text from PDF
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    print("number_of_pages: "+ str(number_of_pages))
    
    # save the image description (texdt) into txt, the formation is :"file_index.page_number.image_number: text description"
    text_file = open(os.path.join(PATH_TO_SAVE_EXTRACTIONS, 'Raw_Description.txt'),'w')
    text_file.write('# save the image description (texdt) into txt, the formation is : "file_index.page_number.image_number: text description"\n')
    
    # extract image description (text) from PDF
    pic_number = 0
    for page_number in range(number_of_pages):
        page = read_pdf.getPage(page_number)
        page_content = page.extractText()
        rc=re.compile(r'Figure\s\d*-\d*\n')
        figure_index = rc.findall(page_content)
        figure_rawcontent = rc.split(page_content)
        for i in range(len(figure_index)):
            figure_content = (figure_index[i]+figure_rawcontent[i+1]).replace('\n','')
            figure_content = figure_content.encode('ascii', 'ignore').decode('ascii')
            figure_content = ''.join((str(file_index),'.',str(page_number+1),'.',str(i+1),':',figure_content))
            pic_number += 1
            text_file.write(figure_content+'\n')
        
        
        # Extract Image from PDF
        xObject = page['/Resources'].getObject()
        if '/XObject' in page['/Resources']:
            xObject = page['/Resources']['/XObject'].getObject()
            image_number = 0
            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                    try:
                        data = xObject[obj]._data
                        # for DCTDecode
                    except:
                        data = xObject[obj].getData()
                        # for other decodes
                    if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                        mode = "RGB"
                    else:
                        mode = "P"
                    if '/Filter' in xObject[obj]:
                        # print(size, mode, xObject[obj]['/Filter'])
                        image_number += 1
                        image_name = ''.join((str(file_index),'.',str(page_number+1),'.',str(image_number)))
                        if xObject[obj]['/Filter'] == '/FlateDecode':
                            img = Image.frombytes(mode, size, data)
                            img.save(os.path.join(PATH_TO_SAVE_EXTRACTIONS, image_name + ".png"))
                        elif xObject[obj]['/Filter'] == '/DCTDecode':
                            img = open(os.path.join(PATH_TO_SAVE_EXTRACTIONS, image_name + ".jpg"), "wb")
                            img.write(data)
                            img.close()
                        elif xObject[obj]['/Filter'] == '/JPXDecode':
                            img = open(os.path.join(PATH_TO_SAVE_EXTRACTIONS, image_name + ".jp2"), "wb")
                            img.write(data)
                            img.close()
                        elif xObject[obj]['/Filter'] == '/CCITTFaxDecode':
                            img = open(os.path.join(PATH_TO_SAVE_EXTRACTIONS, image_name + ".tiff"), "wb")
                            img.write(data)
                            img.close()
                    else:
                        img = Image.frombytes(mode, size, data)
                        img.save(os.path.join(PATH_TO_SAVE_EXTRACTIONS, obj[1:] + ".png"))
        else:
            print("No image found.")
    print(pic_number)
    text_file.close()
    pdf_file.close()

file_name = '19Breast.pdf'
image_text_extract(file_name)
