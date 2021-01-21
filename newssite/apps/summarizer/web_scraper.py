import gc
import newspaper
import re
import requests
import time

from bs4 import BeautifulSoup
from datetime import datetime
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from .models import *


class Scraper:
    """
    This is the class to handle web scraping. It is able to read in and summarize news articles from preset rss feeds.
    """
    # Retrieves all the sites from the database
    sites = Site.objects.all()

    # list of links that are frequent in rss feed but that don't need to be scraped
    invalid_urls = ['https://www.nytimes.com', 'https://www.nytimes.com/section/us', 'https://www.wired.com',
                        'https://www.cnet.com/#ftag=CAD590a51e']

    def __init__(self):
        # tokenizer for text summarization
        # self.tokenizer = AutoTokenizer.from_pretrained("google/pegasus-cnn_dailymail", use_fast=True)
        # Make sure the file is unzipped
        print(gc.collect())
        # model for text summarization
        # self.model = AutoModelForSeq2SeqLM.from_pretrained("google/pegasus-cnn_dailymail")
        gc.collect()

    def scrape_all_articles(self):
        """
        Scrapes in all articles from rss feeds in link_dict
        """
        start_scrape = time.time()
        i = 0
        bulk_articles = []
        for site in self.sites:
            print(f'Started Scraping {site.name}')
            link = site.url_feed
            res = requests.get(link)
            if res.status_code == 404:
                self.article_to_dict[site]["ERROR"] = "RSS feed responded with 404"

            soup = BeautifulSoup(res.text, 'xml')
            scraped_links = soup.findAll('link')[1:]
            if len(scraped_links) > 10:
                scraped_links = scraped_links[:10]
            for art in scraped_links:
                art_link = ""
                if site != 'TheVerge':
                    for x in art:
                        art_link = x
                else:
                    art_link = art['href']
                if art_link != link and art_link not in self.invalid_urls:
                    try:
                        article = newspaper.Article(art_link)
                        article.download()
                        article.parse()
                        bulk_articles.append(Article(date=datetime.now(), site=site, summary=self.summarize(article.text), article_link=art_link, headline=article.title))
                        i += 1
                    except:
                        print(f'ERROR: {art_link}')

            print(f'Finished Scraping {site}')
        Article.objects.bulk_create(bulk_articles)
        end_scrape = time.time()
        total_time = end_scrape - start_scrape
        print(f'TOTAL TIME: {total_time}')

    def get_all_site_articles(self):
        """
        Returns all the summarized articles
        """
        return self.article_to_dict

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
        return re.sub('<[^>]*>', "", tgt_text[0])
