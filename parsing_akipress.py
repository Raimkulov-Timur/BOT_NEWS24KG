import requests
from bs4 import BeautifulSoup as Bs


def osnova(page_url):
    r = requests.get(page_url)
    s = Bs(r.text, 'html.parser')
    articles = s.find_all('div', class_='section_set')
    return articles

def get_info(article_url):
    article_r = requests.get(article_url)
    article_s = Bs(article_r.text, 'html.parser')
    
    title = article_s.find('div', class_='article__title').get_text(strip=True)
    article_text = article_s.find('div', class_='article__text').get_text(strip=True)
    
    article_info = {
        'title': title,
        'link': article_url,
        'text': article_text
    }
    
    return article_info


def news(articles):
    for article in articles:
        link = article.find('a').get('href')
        if link:
            article_url = link
            yield get_info(article_url)















































































    
    
    
    



    

