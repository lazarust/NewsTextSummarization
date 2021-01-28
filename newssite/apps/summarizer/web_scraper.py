import gc
import newspaper
import re
import requests
import time

from bs4 import BeautifulSoup
from datetime import datetime
from newspaper import Article
from transformers import pipeline

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
        # Pipeline for text summarization
        self.pipeline = pipeline("summarization", model="google/pegasus-cnn_dailymail", tokenizer="google/pegasus-cnn_dailymail", framework="pt")
        gc.collect()

    def scrape_all_articles(self):
        """
        Scrapes in all articles from rss feeds in link_dict
        """
        start_scrape = time.time()
        bulk_articles = []
        for site in self.link_dict:
            articles = []
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
                        articles.append(article.text)
                    except:
                        print(f'ERROR: {art_link}')

            print(f'Finished Scraping {site}')
            Article.objects.bulk_create(bulk_articles)
            print(f'Summarizing {site}')
            self.summarize(articles)
            print(f'Finished Summarizing {site}')
        end_scrape = time.time()
        total_time = end_scrape - start_scrape
        print(f'TOTAL TIME: {total_time}')

    def summarize(self, arts):
        """
        Summarizes the passed in article text
        """
        print("Start")
        start_time = time.time()
        tgt_text = self.pipeline(arts)
        end_time = time.time()
        time_diff = end_time - start_time
        print(f'Finish TIME: {time_diff}')
        return tgt_text
