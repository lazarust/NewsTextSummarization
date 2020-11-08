import gc
import requests
import time

from bs4 import BeautifulSoup
from newspaper import Article
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


class Scraper:
    """
    This is the class to handle web scraping. It is able to read in and summarize news articles from preset rss feeds.
    """

    # link_dict is a dictionary of links where the key is a given news site's slug and the value is the rss feed's url
    link_dict = {
        'The Verge': 'https://www.theverge.com/rss/index.xml',
        'NY Times': 'https://rss.nytimes.com/services/xml/rss/nyt/US.xml',
         'Wired': 'https://www.wired.com/feed/rss',
        'CNET': 'https://www.cnet.com/rss/news/',
        'The Onion': 'https://www.theonion.com/rss',
    }

    # individual dictionaries to store a given news site's articles, headlines, and links
    verge_dict = {}
    nyTime_dict = {}
    wired_dict = {}
    cnet_dict = {}
    onion_dict = {}

    # linking dictionary from slug to article dictionary
    article_to_dict = {
        'The Verge': verge_dict,
        'NY Times': nyTime_dict,
        'Wired': wired_dict,
        'CNET': cnet_dict,
        'The Onion': onion_dict,
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
    gc.collect()
    model = AutoModelForSeq2SeqLM.from_pretrained("google/pegasus-cnn_dailymail")

    def scrape_all_articles(self):
        """
        Scrapes in all articles from rss feeds in link_dict
        """
        start_scrape = time.time()
        i = 0
        for site in self.link_dict:
            print(f'Started Scraping {site}')
            link = self.link_dict[site]
            res = requests.get(link)
            if res.status_code == 404:
                self.article_to_dict[site]["ERROR"] = "RSS feed responded with 404"

            soup = BeautifulSoup(res.text, 'xml')
            scraped_links = soup.findAll('link')[1:]
            if len(scraped_links) > 10:
                scraped_links = scraped_links[:10]
            for art in scraped_links:
                art_link = ""
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
                        self.article_to_dict[site][article.title] = {'link': art_link, 'article_loc': self.summarize(article.text)}
                        i += 1
                    except:
                        print(f'ERROR: {art_link}')

            print(f'Finished Scraping {site}')
        # Replaces the index value in article_to_dict[site][article.title][article_loc] to the summarized article string
        # self.update_articles_in_dict()
        end_scrape = time.time()
        total_time = end_scrape - start_scrape
        print(f'TOTAL TIME: {total_time}')

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
