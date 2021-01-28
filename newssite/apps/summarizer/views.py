from django.views.generic import TemplateView
from .web_scraper import Scraper
import schedule


class NewsList(TemplateView):
    template_name = 'news_list.html'
    s = Scraper()
    site_articles = s.scrape_all_articles()

    def __init__(self):
        super().__init__()
        schedule.every(10).hours.do(self.get_arts)

    def get_context_data(self, **kwargs):
        # self.site_articles = self.s.get_all_site_articles()
        context = super().get_context_data(**kwargs)
        # context['arts'] = self.site_articles
        return context

    def get_arts(self):
        self.site_articles = self.s.scrape_all_articles()
