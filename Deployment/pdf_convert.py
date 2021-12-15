# !pip install pdfminer
# !pip install pdf2image
# !sudo apt install poppler-utils
# !apt install ocrmypdf
# !pip3 install git+https://github.com/jbarlow83/OCRmyPDF.git
# !pip3 install pluggy

def convert_scanned_pdf(file_path,save_path):
    # basic purpose : to convert scanned pdf to readable pdf
    # file_path: path of scanned pdf file to convert to readable pdf
    # save_path: path of where file will be saved
    import ocrmypdf
    ocrmypdf.ocr(file_path,
                save_path,
                rotate_pages=True,
                remove_background=False,
                deskew=False,
                force_ocr=False,
                skip_text=True)
    print(f'Converted {file_path} and saved in {save_path}')

def get_pdf_searchable_pages(fname):
    # basic purpose : Tells us whether the pdf is scanned or readable or is it mixed
    # fname : filename of pdf
    # pip install pdfminer
    from pdfminer.pdfpage import PDFPage
    searchable_pages = []
    non_searchable_pages = []
    page_num = 0
    with open(fname, 'rb') as infile:

        for page in PDFPage.get_pages(infile):
            page_num += 1
            if 'Font' in page.resources.keys():
                searchable_pages.append(page_num)
            else:
                non_searchable_pages.append(page_num)
    if page_num > 0:
        if len(searchable_pages) == 0:
            print(f"Document '{fname}' has {page_num} page(s). "
                  f"Complete document is non-searchable")
            convert_scanned_pdf(fname,fname.split('.')[0]+'_converted.pdf')           
        elif len(non_searchable_pages) == 0:
            print(f"Document '{fname}' has {page_num} page(s). "
                  f"Complete document is searchable")
        else:
            print(f"searchable_pages : {searchable_pages}")
            print(f"non_searchable_pages : {non_searchable_pages}")
            convert_scanned_pdf(fname,fname.split('.')[0]+'_converted.pdf')
    else:
        print(f"Not a valid document")