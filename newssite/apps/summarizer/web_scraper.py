import requests
import time

from bs4 import BeautifulSoup
from newspaper import Article
from py4j.java_gateway import JavaGateway
from pyspark import SparkConf, SparkContext
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


class Scraper:
    """
    This is the class to handle web scraping. It is able to read in and summarize news articles from preset rss feeds.
    """

    # link_dict is a dictionary of links where the key is a given news site's slug and the value is the rss feed's url
    link_dict = {
        'verge': 'https://www.theverge.com/rss/index.xml',
        # 'nyTimes_US': 'https://rss.nytimes.com/services/xml/rss/nyt/US.xml',
        # 'wired_main': 'https://www.wired.com/feed/rss',
        # 'cnet': 'https://www.cnet.com/rss/news/',
    }

    # individual dictionaries to store a given news site's articles, headlines, and links
    verge_dict = {}
    nyTime_dict = {}
    wired_dict = {}
    cnet_dict = {}

    # linking dictionary from slug to article dictionary
    article_to_dict = {
        'verge': verge_dict,
        # 'nyTimes_US': nyTime_dict,
        # 'wired_main': wired_dict,
        # 'cnet': cnet_dict,
    }

    # list of all articles
    articles = []

    # list of links that are frequent in rss feed but that don't need to be scraped
    not_allowed_urls = ['https://www.nytimes.com', 'https://www.nytimes.com/section/us', 'https://www.wired.com',
                        'https://www.cnet.com/#ftag=CAD590a51e']

    # tokenizer for text summarization
    tokenizer = AutoTokenizer.from_pretrained("google/pegasus-cnn_dailymail", use_fast=True)
    # Make sure the file is unzipped
    # model for text summarization
    model = AutoModelForSeq2SeqLM.from_pretrained("apps/summarizer/model", local_files_only=True)

    # Sets up PySpark Things
    conf = SparkConf().setAppName("Web App").setMaster('spark://spark-master:7077')
    SparkContext.setSystemProperty('spark.python.worker.memory', '2g')
    sc = SparkContext('local', conf=conf)
    gateway = JavaGateway

    def scrape_all_articles(self):
        """
        Scrapes in all articles from rss feeds in link_dict
        """
        i = 0
        for site in self.link_dict:
            print(f'Started Scraping {site}')
            link = self.link_dict[site]
            res = requests.get(link)
            if res.status_code == 404:
                self.article_to_dict[site]["ERROR"] = "RSS feed responded with 404"

            soup = BeautifulSoup(res.text, 'xml')

            for art in soup.findAll('link')[1:]:
                articles = []
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
                        articles.append(article.text)
                        self.article_to_dict[site][article.title] = {'link': art_link, 'article_loc': i}
                        i += 1
                    except:
                        print(f'ERROR: {art_link}')

                # Creates PySpark RDD and saves it in cache. Then maps the summarize function
                arts_text = sc.parallelize(articles)
                arts_text.cache()
                arts_map = arts_text.map(lambda z: self.summarize(z))
                self.articles.append(arts_map.collect())
            print(f'Finished Scraping {site}')
        # Replaces the index value in article_to_dict[site][article.title][article_loc] to the summarized article string
        self.update_articles_in_dict()

    def get_specific_site_articles(self, slug=None):
        """
        Takes in a slug and returns the summarized articles for just that slug
        TODO: Remove the method if it is not needed
        """
        if slug:
            return self.article_to_dict[slug]
        else:
            print("ERROR: Please Enter Slug")

    def get_all_site_articles(self):
        """
        Returns all the summarized articles
        """
        return self.article_to_dict

    def get_all_site_slugs(self):
        """
        Returns a list of all the scraped site slugs
        TODO: Remove the method if it is not needed
        """
        slug_list = []
        for slug in self.link_dict:
            slug_list.append(slug)
        return slug_list

    def update_articles_in_dict(self):
        """
        Replaces index with article text in dictionary
        """
        for site, headline_dict in self.article_to_dict.items():
            for headline, link_dict in headline_dict.items():
                if isinstance(link_dict['article_loc'], int):
                    link_dict.update({
                        'article_loc': self.articles[link_dict['article_loc']]
                    })

    def summarize(self, art):
        """
        Summarizes the passed in article text
        """
        print("Start Summarizing")
        start_time = time.time()
        batch = self.tokenizer.prepare_seq2seq_batch([art], max_target_length=100)
        translated = self.model.generate(**batch)
        tgt_text = self.tokenizer.batch_decode(translated, skip_special_tokens=True)
        end_time = time.time()
        time_diff = end_time - start_time
        print(f'TIME: {time_diff}')
        return tgt_text
