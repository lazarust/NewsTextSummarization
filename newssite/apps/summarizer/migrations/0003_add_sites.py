from django.db import migrations

site_dict = [
    {
        'name': 'The Verge',
        'slug': 'the-verge',
        'link': 'https://www.theverge.com/rss/index.xml'
    },
    {
        'name': 'NY Times',
        'slug': 'NYTimes',
        'link': 'https://rss.nytimes.com/services/xml/rss/nyt/US.xml'
    },
    {
        'name': 'Wired',
        'slug': 'wired',
        'link': 'https://www.wired.com/feed/rss'
    },
    {
        'name': 'CNET',
        'slug': 'cnet',
        'link': 'https://www.cnet.com/rss/news/'
    },
    {
        'name': 'The Onion',
        'slug': 'onion',
        'link': 'https://www.theonion.com/rss'
    }
]


def create_sites(apps, schema_editor):
    model = apps.get_model('summarizer.Site')
    sites = []
    for dictionary in site_dict:
        site = model(name=dictionary['name'], slug=dictionary['slug'], url_feed=dictionary['link'])
        sites.append(site)

    model.objects.bulk_create(sites)


class Migration(migrations.Migration):
    dependencies = [('summarizer', '0002_auto_20210120_0417'),]

    operations = [
        migrations.RunPython(create_sites, migrations.RunPython.noop)
    ]