import requests
from bs4 import BeautifulSoup
from ckiptagger import WS
from os import listdir

def main():
    #To use ckiptagger, you need to download this into the current directory
    if not('data' in listdir('./')):
        from ckiptagger import data_utils
        data_utils.download_data_gdown('./')
    
    #Visit google news to get all the articles
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    res = requests.get('https://news.google.com/topstories?hl=zh-TW&gl=TW&ceid=TW:zh-Hant', headers=headers)
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
        paragraph = article_soup.select('p') #Select all <p>
        possible_div = {}
        for p in paragraph:
            if len(p.text) > bias: #If one block of text has more words than bias
                if possible_div.__contains__(p.findParent('div')): #If the block's parent div is already in dictionary
                    possible_div[p.findParent('div')] += 1 
                else: #If this is the first time the block's parent has been seen
                    possible_div[p.findParent('div')] = 1
        #I did this to filter out texts that are not useful

        #Some website can't be scrapped, which results in not finding any div
        if len(possible_div.values()) != 0:
            found_p = list(possible_div.keys())[list(possible_div.values()).index(max(possible_div.values()))]
            target = found_p.select('p')
            
            #Using CKIP to break off words
            for p in target:
                if len(p.text) > int(bias/4):
                    ws = WS('./data')
                    ws_results = ws([p.text])
                    for w in ws_results:
                        for ww in w:
                            print(ww, end=' ', file=f)
            
            print(f'[{n+1}/{len(headlines)}]')

        f.close()

    list_txt.close()

if __name__ == "__main__":
    main()