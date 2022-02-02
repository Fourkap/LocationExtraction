import pdfplumber


def test(p):
    with pdfplumber.open('Inferno.pdf') as pdf:
        first_page = pdf.pages[p]
        #print(first_page.extract_text())
        text = first_page.extract_text()
        return text
