from bs4 import BeautifulSoup
from lxml import html
import urllib.request
import html2text
import bleach

def termSearch(userinput):
    ## URL Modification for user term search
    url="http://tlwi.w3-969.ibm.com/standards/terminology/cgi-bin/lookup?ug=corporate&term="+userinput+"&submit=Search&source=en&target_switch=none&template=simple&db_name=LOGOS&11=main+form&11=acronym~abbreviation&11=prohibited"
    ##Set the URL
    content=urllib.request.urlopen(url).read()
    soup=BeautifulSoup(content, "lxml")
    ## Get Results
    soup=soup.find_all('ol')
    ## Delete Reference Links and Convert
    clean =bleach.clean(soup,tags=['ol','br','li','p'],strip=True, strip_comments=True) 
    test=str(clean)
    html=html2text.html2text(test)
    html=html.replace("_","\n")
    html=html.strip("[")
    html=html.strip("]\n")
    ## Return String
    if html=="":
        html="No results have been found. Please try a different query."
    return html
    

if __name__=="__main__":
    print("Please enter the user input")
    userinput=input()
    url="http://tlwi.w3-969.ibm.com/standards/terminology/cgi-bin/lookup?ug=corporate&term="+userinput+"&submit=Search&source=en&target_switch=none&template=simple&db_name=LOGOS&11=main+form&11=acronym~abbreviation&11=prohibited"
    ##Set the URL
    content=urllib.request.urlopen(url).read()
    soup=BeautifulSoup(content, "lxml")
    soup=soup.find_all('ol')
    #Delete Reference Links
    clean =bleach.clean(soup,tags=['ol','br','li','p'],strip=True, strip_comments=True) 
    test=str(clean)
    html=html2text.html2text(test)
    html=html.replace("_","\n")
    html=html.strip("[")
    html=html.strip("]\n")
    print(html)
    if html=="":
        print("EMPTY")
    
