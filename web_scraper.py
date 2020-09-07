import requests

from bs4 import BeautifulSoup
from newspaper import Article

link_dict = {
    'verge': 'https://www.theverge.com/rss/index.xml',
    # 'nyTimes_Home': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
    # 'nyTime_US': 'https://rss.nytimes.com/services/xml/rss/nyt/US.xml',
    # 'independent': 'https://www.independent.co.uk/news/world/rss',
    # 'cnn_world': 'http://rss.cnn.com/rss/cnn_world.rss',
    # 'cnn_us': 'http://rss.cnn.com/rss/cnn_us.rss',
    # 'cnn_tech': 'http://rss.cnn.com/rss/cnn_tech.rss',
    # 'wired_main': 'https://www.wired.com/feed/rss',
    # 'wired_backchannel': 'https://www.wired.com/feed/category/backchannel/latest/rss',
    # 'wired_ideas': 'https://www.wired.com/feed/category/ideas/latest/rss',
    # 'wired_science': 'https://www.wired.com/feed/category/science/latest/rss',
    # 'huffpost': 'https://www.huffpost.com/section/front-page/feed?x=1',
    # 'nypost': 'https://nypost.com/feed/',
    # 'onion': 'https://www.theonion.com/rss',
}

verge_dict = {}
nyTime_dict = {}
independent_dict = {}
cnn_dict = {}
wired_dict = {}
huffpost_dict = {}
nypost_dict = {}
onion_dict = {}

article_to_dict = {
    'verge': verge_dict,
    'nyTimes_Home': nyTime_dict,
    'nyTime_US': nyTime_dict,
    'independent': independent_dict,
    'cnn_world': cnn_dict,
    'cnn_us': cnn_dict,
    'cnn_tech': cnn_dict,
    'wired_main': wired_dict,
    'wired_backchannel': wired_dict,
    'wired_ideas': wired_dict,
    'wired_science': wired_dict,
    'huffpost': huffpost_dict,
    'nypost': nypost_dict,
    'onion': onion_dict,
}


for site in link_dict:
    link = link_dict[site]
    res = requests.get(link)
    soup = BeautifulSoup(res.text, 'html.parser')

    for art in soup.findAll('link')[1:]:
        art_link = art['href']
        article = Article(art_link)
        article.download()
        article.parse()
        article_to_dict[site][article.title] = (article.text, art_link)

