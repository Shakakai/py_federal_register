import urllib2, json, datetime

def __fetch__(url):
    try:
        result = urllib2.urlopen(url)
        return json.loads(result.read())
    except:
        raise Exception("Could not load agency list.")
    

AGENCY_LIST_ENDPOINT = "http://api.federalregister.gov/v1/agencies.json"
AGENCY_ENDPOINT = "http://api.federalregister.gov/v1/agencies/%d.json"
ARTICLE_ENDPOINT = "http://api.federalreigster.gov/v1/articles/%d.json"
SEARCH_ENDPOINT = "http://api.federalregister.gov/v1/articles.json"

def agencies():
    agency_list = []
    raw_list = __fetch__(AGENCY_LIST_ENDPOINT)
    for raw_agency in raw_list:
        agency = Agency(raw_agency)
        agency_list.append(agency)
    return agency_list


class Agency(object):
    
    @classmethod
    def by_id(clz, agency_id):
        raw = __fetch__(AGENCY_ENDPOINT % agency_id)
        return Agency(raw)
    
    def __init__(self, raw):
        props = ['url', 'description', 'name', 'id', 'short_name', 'recent_articles_url']
        for prop in props:
            if prop in raw:
                setattr(self, prop, raw[prop])
            else:
                setattr(self, prop, None)
            
        
    
    @property
    def recent_articles(self):
        '''
        Returns the agencies most recent documents in the federal register.
        '''
        article_list = []
        raw_list = __fetch__(self.recent_articles_url)
        if "results" in raw_list:
            for raw_article in raw_list['results']:
                article = Article(raw_article)
                article_list.append(article)
            
        return article_list
    


class Article(object):
    
    @classmethod
    def by_id(clz, article_id):
        raw = __fetch__(ARTICLE_ENDPOINT % article_id)
        return clz(raw)
    
    @classmethod
    def search(clz, query):
        url = "%s?%s" % (SEARCH_ENDPOINT, query)
        raw = __fetch__(url)
        article_list = []
        for raw_article in raw["results"]:
            article = clz(raw_article)
            article_list.append(article)
        return article_list
    
    def __init__(self, raw):
        str_props = ["mods_url", "effective_on", "type", "action", "title",\
         "document_number", "end_page", "volume", "abstract", "full_text_xml_url",\
         "start_page", "docket_id", "html_url", "abstract_html_url", "dates", "pdf_url",\
         "body_html_url", "comments_close_on"]
        
        for prop in str_props:
            if prop in raw:
                setattr(self, prop, raw[prop])
            else:
                setattr(self, prop, None)
        
        date_props = ["publication_date"]
        for prop in date_props:
            if prop in raw:
                setattr(self, prop, datetime.datetime.strptime(raw[prop], '%Y-%m-%d'))
            else:
                setattr(self, prop, None)
            
        
        self.agencies = []
        raw_list = raw["agencies"]
        for raw_agency in raw_list:
            agency = Agency(raw_agency)
            self.agencies.append(agency)
        
        array_props = ["regulation_id_numbers", "cfr_refernces"]
        for prop in array_props:
            current_list = []
            setattr(self, prop, current_list)
            if prop in raw:
                for item in raw[prop]:
                    current_list.append(item)
                
            
        
    


