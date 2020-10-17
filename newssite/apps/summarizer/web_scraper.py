import requests
import time

from bs4 import BeautifulSoup
from newspaper import Article
from py4j.java_gateway import JavaGateway
from pyspark import SparkConf, SparkContext
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


# conf = SparkConf().setAppName("Collinear Points")
# sc = SparkContext('local', conf=conf)
# gateway = JavaGateway()


class Scraper:
    link_dict = {
        'verge': 'https://www.theverge.com/rss/index.xml',
        # 'nyTimes_US': 'https://rss.nytimes.com/services/xml/rss/nyt/US.xml',
        # 'wired_main': 'https://www.wired.com/feed/rss',
        # 'cnet': 'https://www.cnet.com/rss/news/',
    }

    verge_dict = {}
    nyTime_dict = {}
    wired_dict = {}
    cnet_dict = {}

    article_to_dict = {
        'verge': verge_dict,
        # 'nyTimes_US': nyTime_dict,
        # 'wired_main': wired_dict,
        # 'cnet': cnet_dict,
    }

    articles = []

    not_allowed_urls = ['https://www.nytimes.com', 'https://www.nytimes.com/section/us', 'https://www.wired.com',
                        'https://www.cnet.com/#ftag=CAD590a51e']

    tokenizer = AutoTokenizer.from_pretrained("google/pegasus-cnn_dailymail", use_fast=True)
    # Make sure the file is unzipped
    model = AutoModelForSeq2SeqLM.from_pretrained("apps/summarizer/model", local_files_only=True)

    def scrape_all_articles(self):
        i = 0
        for site in self.link_dict:
            print(f'Started Scraping {site}')
            link = self.link_dict[site]
            res = requests.get(link)
            if res.status_code == 404:
                self.article_to_dict[site]["ERROR"] = "RSS feed responded with 404"

            soup = BeautifulSoup(res.text, 'xml')

            for art in soup.findAll('link')[1:]:
                if site != 'verge':
                    for x in art:
                        art_link = x
                else:
                    art_link = art['href']
                if art_link != link and art_link not in self.not_allowed_urls:
                    try:
                        article = Article(art_link)
                        article.download()
                        article.parse()
                        # self.articles.append(article.text)
                        self.article_to_dict[site][article.title] = {'link': art_link, 'article_loc': self.summarize((article.text))}
                        i += 1
                    except:
                        print(f'ERROR: {art_link}')

            # arts_text = sc.parallelize(self.articles)
            # arts_text.foreach(self.summarize)
            print(f'Finished Scraping {site}')
        # self.update_articles_in_dict()

    def get_specific_site_articles(self, slug=None):
        if slug:
            return self.article_to_dict[slug]
        else:
            print("ERROR: Please Enter Slug")

    def get_all_site_articles(self):
        return self.article_to_dict

    def get_all_site_slugs(self):
        slug_list = []
        for slug in self.link_dict:
            slug_list.append(slug)
        return slug_list

    def update_articles_in_dict(self):
        for site, headline_dict in self.article_to_dict.items():
            for headline, link_dict in headline_dict.items():
                if isinstance(link_dict['article_loc'], int):
                    link_dict.update({
                        'article_loc': self.articles[link_dict['article_loc']]
                    })

    def summarize(self, art):
        print("Start Summarizing")
        start_time = time.time()
        batch = self.tokenizer.prepare_seq2seq_batch([art], max_target_length=100)
        translated = self.model.generate(**batch)
        tgt_text = self.tokenizer.batch_decode(translated, skip_special_tokens=True)
        end_time = time.time()
        time_diff = end_time - start_time
        print(f'TIME: {time_diff}')
        return tgt_text
