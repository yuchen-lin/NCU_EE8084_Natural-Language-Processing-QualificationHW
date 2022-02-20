import requests
from bs4 import BeautifulSoup
from ckiptagger import WS
from os import listdir

def getArticle(url):


    return none

def hyphenation(article):


    return none

def main():
    #To use ckiptagger, you need to download this into the current directory
    if not('data' in listdir('./')):
        from ckiptagger import data_utils
        data_utils.download_data_gdown('./')
    
    #Visit google news to get all the articles
    res = requests.get('https://news.google.com/topstories?hl=zh-TW&gl=TW&ceid=TW:zh-Hant')
    soup = BeautifulSoup(res.text, 'lxml')
    headlines = soup.select('h3 a') # select articles

    #Create newslist.txt
    newslist_path = 'newslist.txt'
    list_txt = open(newslist_path, 'w', encoding='UTF-8')

    #Run through every website
    bias = 40
    for n, h in enumerate(headlines):
        newsfile_path = f'news{n+1:04d}.txt'
        f = open(newsfile_path, 'w', encoding='UTF-8')

        #Get url, media, headline
        google_url = h['href']
        temp_url = f'https://news.google.com{google_url[1:]}'
        media = h.findParent('article').find(attrs={'data-n-tid': '9'}).text
        headline = h.text

        #Visit news website
        article_res = requests.get(temp_url)
        article_soup = BeautifulSoup(article_res.text, 'lxml')
        
        #Write url, media, headline into "newslist.txt"
        print(f'news{n+1:04d}\t{article_res.url}\t{media}\t{headline}\n', file=list_txt)

        #Find useful information within website
        paragraph = article_soup.select('p')
        possible_div = {}
        for p in paragraph:
            if len(p.text) > bias:
                if possible_div.__contains__(p.findParent('p')):
                    possible_div[p.findParent('p')] += 1
                else:
                    possible_div[p.findParent('p')] = 1

        print(possible_div.values())
        found_p = list(possible_div.keys())[list(possible_div.values()).index(max(possible_div.values()))]
        target = found_p.select('p')
        
        for p in target:
            if len(p.text) > bias and not("" in p.text):
                print(p.text, file=f)

        f.close()

    list_txt.close()

if __name__ == "__main__":
    main()