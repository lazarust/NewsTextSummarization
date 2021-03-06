from django.views.generic import TemplateView
import schedule

from .models import Article
from newssite.apps.base.utils.scraper import Scraper


class NewsList(TemplateView):
    template_name = 'news_list.html'
    s = Scraper()
    site_articles = s.scrape_all_articles()

    def __init__(self):
        super().__init__()
        schedule.every(10).hours.do(self.get_arts)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all().prefetch_related('site')
        return context

    def get_arts(self):
        self.site_articles = self.s.scrape_all_articles()
