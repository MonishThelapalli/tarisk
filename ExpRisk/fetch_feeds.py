import feedparser

feeds = [
    'http://feeds.bbci.co.uk/news/rss.xml',
    'https://rss.cnn.com/rss/edition.rss'
]

for f in feeds:
    print('Feed:', f)
    d = feedparser.parse(f)
    if d.bozo:
        print('  parse error:', d.bozo_exception)
    for e in d.entries[:5]:
        print('-', e.title)
        print('  ', e.link)
    print()