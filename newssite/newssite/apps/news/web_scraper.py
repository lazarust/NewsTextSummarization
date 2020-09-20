import requests

from bs4 import BeautifulSoup
from newspaper import Article


class Scraper:
    link_dict = {
        'verge': 'https://www.theverge.com/rss/index.xml',
        'nyTimes_Home': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
        'nyTimes_US': 'https://rss.nytimes.com/services/xml/rss/nyt/US.xml',
        'independent': 'https://www.independent.co.uk/news/world/rss',
        'wired_main': 'https://www.wired.com/feed/rss',
        'wired_backchannel': 'https://www.wired.com/feed/category/backchannel/latest/rss',
        'wired_ideas': 'https://www.wired.com/feed/category/ideas/latest/rss',
        'wired_science': 'https://www.wired.com/feed/category/science/latest/rss',
        'huffpost': 'https://www.huffpost.com/section/front-page/feed?x=1',
        'cnet': 'https://www.cnet.com/rss/news/',
    }

    verge_dict = {}
    nyTime_dict = {}
    independent_dict = {}
    wired_dict = {}
    huffpost_dict = {}
    cnet_dict = {}

    article_to_dict = {
        'verge': verge_dict,
        'nyTimes_Home': nyTime_dict,
        'nyTimes_US': nyTime_dict,
        'independent': independent_dict,
        'wired_main': wired_dict,
        'wired_backchannel': wired_dict,
        'wired_ideas': wired_dict,
        'wired_science': wired_dict,
        'huffpost': huffpost_dict,
        'cnet': cnet_dict,
    }

    not_allowed_urls = ['https://www.nytimes.com', 'https://www.nytimes.com/section/us', 'https://www.wired.com']

    def scrape_all_articles(self):
        for site in self.link_dict:
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
                        self.article_to_dict[site][article.title] = (article.text, art_link)
                    except:
                        print(f'ERROR: {art_link}')

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