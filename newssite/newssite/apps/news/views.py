from django.views.generic import TemplateView
from .web_scraper import Scraper


class NewsList(TemplateView):
    template_name = 'news_list.html'
    s = None
    site_articles = {}

    def __init__(self):
        super().__init__()
        self.s = Scraper()
        self.s.scrape_all_articles()

    def get_context_data(self, **kwargs):
        self.site_articles = self.s.get_all_site_articles()['verge']
        context = super().get_context_data(**kwargs)
        context['arts'] = self.site_articles
        return context