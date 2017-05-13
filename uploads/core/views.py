from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from uploads.core.models import Document
from uploads.core.forms import DocumentForm
from django.http import HttpResponse
import numpy as np
import pandas as pd

def home(request):
    documents = Document.objects.all()
    return render(request, 'core/home.html', { 'documents': documents })


def simple_upload(request):
    print (request.FILES.keys())
    if request.method == 'POST' and request.FILES:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
	dialect = csv.Sniffer().sniff(codecs.EncodedFile(myfile, "utf-8").read(1024))
	csvfile.open()
	reader = csv.reader(codecs.EncodedFile(myfile, "utf-8"), delimiter=',', dialect=dialect)
	print (reader)

	'''data = pd.read_csv("media/"+filename)
	data.columns = ['item_id','wasted','day' , 'time']
        a1 = list(data.day)
        a2 = list(data.time)
        a3 =list(data.wasted)
        a4=list(data.item_id) 
        uploaded_file_url = fs.url(filename)
	print (a1,a2,a3,a4)'''
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'core/simple_upload.html')

'''from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter#process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

from cStringIO import StringIO

def pdf_to_text(pdfname):

    # PDFMiner boilerplate
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Extract text
    fp = file(pdfname, 'Name')
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
    fp.close()
    fp1 = file(pdfname, 'Transactions')
    for page in PDFPage.get_pages(fp1):
        interpreter.process_page(page)
    fp.close()

    # Get text from StringIO
    text = sio.getvalue()

    # Cleanup
    device.close()
    sio.close()

    return text'''
