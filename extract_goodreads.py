from bs4 import BeautifulSoup
from urllib.request import urlopen
import codecs
import json
import collections
import pprint
    
if __name__ == '__main__':
    go=[]
    extractions=[]
    source='https://www.goodreads.com'
    url='https://www.goodreads.com/list/show/104.The_MOVIE_was_BETTER_than_the_BOOK?page=10' #put page link for extraction here
    page = urlopen(url).read()
    soup=BeautifulSoup(page,'html.parser')

    links=soup.findAll('a',class_='bookTitle') #get all the book titles on that page
    for l in links:
        link=l.get('href')
        go.append(link)
    #print(go)
    with open("extractions10.json","w") as out:
        out.write("[")    
        for g in go:
            if not(g==go[0]):
                out.write(",\n")
                
            genres=[]
            booklink=source+g #get link to book page
            bookinfo=urlopen(booklink).read()
            s1=BeautifulSoup(bookinfo,'html.parser')
            #extract following entities on book page
            title=s1.find('h1', class_='bookTitle').contents[0].strip()
            author=s1.find('div', id='bookAuthors').text.strip()
            #print(title)
            #print(author)
            publishinfo=s1.findAll('div',class_='row')
            if len(publishinfo)==1:
                publish=publishinfo[0].text.strip()
            else:
                publish=publishinfo[1].text.strip()
            #print(publishinfo)
            rating=s1.find('span',class_='value rating').text.strip()
            #print(rating)
            genrelinks=s1.findAll('a',class_='actionLinkLite bookPageGenreLink')
            for genre in genrelinks:
                genres.append(genre.text.strip())
            #print(genres)
            language=s1.find('div',itemprop='inLanguage')
            if language is not None:
                lang=language.text.strip()    
            #print(language)
            numberofpages=s1.find('span',itemprop='numberOfPages')
            if numberofpages is not None:
                pages=numberofpages.text.strip()
            #print(numberofpages)
            
            entity=collections.OrderedDict() #Creating the JSON object for each book
            entity["URL"]=booklink
            if title is not None:
                entity["Title"]=title
            if author is not None:
                entity["Author"]=author
            if publish is not None:
                entity["PublisherInfo"]=publish
            if rating is not None:
                entity["Rating"]=rating
            if genres is not None:
                entity["Genre"]=genres
            if lang is not None:
                entity["Language"]=lang
            if pages is not None:
                entity["NumberOfPages"]=pages
            
            out.write(json.dumps(entity))
                
        out.write("]")

        #combine all the JSON files for each page link. Convert consolidated JSON into CSV using online converter.
        
   
