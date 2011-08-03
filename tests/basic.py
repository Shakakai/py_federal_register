import unittest, sys
from federal_register import agencies, Agency, Article

AGENCY_ID = 68

class BasicTests(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_agency_list(self):
        agency_list = agencies()
        self.assertTrue(len(agency_list) > 0, "No agencies returned")
        agency = agency_list[0]
        self.assertTrue(agency.id is not None, "Agency id is None.")
    
    def test_agency_by_id(self):
        agency = Agency.by_id(AGENCY_ID)
        self.assertTrue(agency is not None, "Could not find agency")
    
    def test_agency_recent_articles(self):
        agency = Agency.by_id(AGENCY_ID)
        self.assertTrue(agency is not None, "Could not find agency.")
        articles = agency.recent_articles
        self.assertTrue(len(articles) > 0, "No articles for this agency.")
    
    def test_article_search(self):
        articles = Article.search("conditions[term]=fishing")
        self.assertTrue(len(articles) > 0, "No articles for this query.")
        article = articles[0]
        self.assertTrue(type(article) is Article, "First article is not proper type.")
    