import gc
import newspaper
import requests
import time

from bs4 import BeautifulSoup
from datetime import datetime
from newspaper import Article
from transformers import pipeline

from ...summarizer.models import Site


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
        for site in self.sites:
            print(f'Started Scraping {site}')
            link = site.url_feed
            res = requests.get(link)
            if res.status_code == 404:
                print(f"RSS feed responded with 404: {site}")

            soup = BeautifulSoup(res.text, 'xml')
            scraped_links = soup.findAll('link')[1:]

            headline_list = Article.objects.filter(site=site).values_list('headline', flat=True)

            if len(scraped_links) > 10:
                scraped_links = scraped_links[:10]
            for art in scraped_links:
                art_link = ""
                if site.slug != 'the-verge':
                    for x in art:
                        art_link = x
                else:
                    art_link = art['href']
                if art_link != link and art_link not in self.invalid_urls:
                    try:
                        article = newspaper.Article(art_link)
                        article.download()
                        article.parse()
                        if article.title not in headline_list:
                            bulk_articles.append(Article(date=datetime.now(), site=site, summary=self.summarize(article.text), article_link=art_link, headline=article.title))
                    except:
                        print(f'ERROR: {art_link}')

            print(f'Finished Scraping {site}')
            Article.objects.bulk_create(bulk_articles)
        end_scrape = time.time()
        total_time = end_scrape - start_scrape
        print(f'TOTAL TIME: {total_time}')

    def summarize(self, art):
        """
        Summarizes the passed in article text
        """
        print("Start")
        start_time = time.time()
        if len(art) > 1024:
            art = art[:1024]
        tgt_texts = self.pipeline(art)
        end_time = time.time()
        time_diff = end_time - start_time
        print(f'Finish TIME: {time_diff}')
        return tgt_texts[0]['summary_text']
