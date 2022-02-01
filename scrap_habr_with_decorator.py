import requests
import re
from bs4 import BeautifulSoup
from log_decorator_with_path import add_log_to_function

HEADER = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8,en-US;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'hl=ru; fl=ru; visited_articles=599031:561980:254773; habr_web_home=ARTICLES_LIST_ALL',
    'Host': 'habr.com',
    'Pragma': 'no-cache',
    'Referer': 'https://github.com/',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'sec-gpc': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}

def get_word(text):
    pattern = re.compile(r'\w+')
    
    return pattern.findall(text)

def get_html_text(url):

    response = requests.get(url, headers=HEADER)
    html_text = response.text
    html_soup = BeautifulSoup(html_text, 'html.parser')
    
    return html_soup.get_text('\n', strip='True')
    
@add_log_to_function("LOGS/logs.txt")
def main(keywords, url):

    base_url = 'https://habr.com/ru/all'
    urls = []
    urls.append(base_url)

    while len(urls) > 0:

        url = urls.pop(0)

        req = requests.get(url, headers=HEADER)
        req.raise_for_status()
        text = req.text
        soup = BeautifulSoup(text, features='html.parser')

        articles = soup.find_all('article')

        for article in articles:
            try:
                if article.find('h2'):
                    title = article.find('h2')
            except:
                pass

            time = article.find('time')
            a_tag = title.find('a')

            try:
                if 'href' in a_tag.attrs:
                    href = a_tag.attrs['href']
            except:
                pass
            url = 'https://habr.com' + href
            tmp_title = get_word(title.text.lower())

            if set(keywords) & set(tmp_title):

                print(f"{time.get('title')} - {title.text} - {url}")
                for word in keywords:
                    html_text = get_word(get_html_text(url).lower())

                    if word in html_text:
                        print(f'{word} - {html_text.count(word)}')

                print('------------')

        # if soup.find(id='pagination-next-page').get('href'):
        #     next_page = 'https://habr.com' + \
        #         soup.find(id='pagination-next-page').get('href')
        #     urls.append(next_page)


if __name__ == '__main__':
    
    main(['дизайн', 'фото', 'web', 'python'], 'https://habr.com/ru/all/')