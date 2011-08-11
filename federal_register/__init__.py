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
    def search(clz):
        return ArticleQuery()
    
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
                
            
        
    

class ArticleQuery(object):
    def __init__(self):
        self.params = []
    
    def param(self, p):
        self.params.append(p)
    
    def keyword(self, term):
        param = "conditions[term]=%s" % term
        self.param(param)
        return self
    
    def published(self, equal=None, year=None, lte=None, gte=None):
        if equal is not None:
            param = "conditions[publication_date][is]=%s" % equal
        elif year is not None:
            param = "conditions[publication_date][year]=%s" % year
        elif lte is not None:
            param = "conditions[publication_date][lte]=%s" % lte
        elif gte is not None:
            param = "conditions[publication_date][gte]=%s" % gte
        self.param(param)
        return self
    
    def agencies(self, id=None, ids=None):
        if id is not None:
            param = "conditions[agency_ids][]=%s" % id
            self.param(param)
        elif ids is not None:
            for id in ids:
                param = "conditions[agency_ids][]=%s" % id
                self.param(param)
        return self
    
    def doc_category(self, doc_type):
        param = "conditions[type]=%s" % doc_type
        self.param(param)
        return self
    
    def docket_number(self, num):
        param = "conditions[docket_id]=%s" % num
        self.param(param)
        return self
    
    def location(self, zip_code, distance):
        param = "conditions[near][location]=%s&conditions[near][within]=%s" % (zip_code, distance)
        self.param(param)
        return self
    
    def execute(self):
        query = "&".join(self.params)
        url = "%s?%s" % (SEARCH_ENDPOINT, query)
        raw = __fetch__(url)
        article_list = []
        for raw_article in raw["results"]:
            article = Article(raw_article)
            article_list.append(article)
        return article_list











