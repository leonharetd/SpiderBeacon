from scrapyd_api import ScrapydAPI
scrapyd = ScrapydAPI('http://localhost:6800')
print scrapyd.list_projects()