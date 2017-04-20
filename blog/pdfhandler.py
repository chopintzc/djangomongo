'''
Created on Feb 08, 2017
pdf files handling methods

@author: Zhongchao
'''

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

THRESHOLD = 40
LENGTH = 200000

'''
    retrieve title and content from pdf file
'''
def handle_uploaded_file(f):
    text = convert_pdf_to_txt(f)
    title = f._name[:-4]
    abstract = text[:LENGTH]
    title = title.replace('\n', ' ')
    title = title.replace('- ', '')
    abstract = abstract.replace('\n', ' ')
    abstract = abstract.replace('- ', '')
    '''
    start = text.find('\n\n')
    end = text.find('\n\n', start + 2)
    while (end - start < THRESHOLD):
        start = end + 2
        end = text.find('\n\n', start + 2)
    title = text[start:end]
    title = title.replace('\n', ' ')
    title = title.replace('- ', '')
    start = text.lower().find('summary')
    end = text.lower().find('introduction')
    abstract = text[start+7:end-1]
    abstract = abstract.replace('\n', ' ')
    abstract = abstract.replace('- ', '')
    '''
    return title, abstract
    
    
'''
    convert pdf file to plain text
''' 
def convert_pdf_to_txt(f):
    # initialize device manager and interpreter
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 20 # get from page 1
    caching = True
    pagenos=set()
    
    for page in PDFPage.get_pages(f, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue() # get the plain text
    
    device.close()
    retstr.close()
    return text