import collections
import json

def read_json(file_path, max_len_word=6, top_words=10):
    with open(file_path, encoding='utf-8') as news_file:
        news = json.load(news_file)
        # print(news)
        description_words = []
        for item in news['rss']['channel']['items']:
            # description = item['description'].split(' ')
            description = [word for word in item['description'].split(' ') if len(word) > max_len_word]
            description_words.extend(description)
            counter_words = collections.Counter(description_words)
        print(counter_words.most_common(top_words))
if __name__ == '__main__':
    read_json('news_afr.json')