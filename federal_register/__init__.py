import urllib2, json

def __fetch__(url):
    #try:
    result = urllib2.urlopen(url)
    return json.loads(result.read())
    #except:
    #    raise Exception("Could not load agency list.")
    #

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
        self.html_url = raw['url']
        self.description = raw['description']
        self.name = raw['name']
        self.id = raw['id']
        self.short_name = raw['short_name']
        self._recent_articles_url = raw['recent_articles_url']
    
    @property
    def recent_articles(self):
        '''
        Returns the agencies most recent documents in the federal register.
        '''
        article_list = []
        raw_list = __fetch__(self._recent_articles_url)
        if "results" in raw_list:
            for raw_article in raw_list['results']:
                article = Article(raw_article)
                article_list.append(article)
            
        return article_list
    


class Article(object):
    '''
    {
    mods_url: "http://www.gpo.gov/fdsys/granule/FR-1998-03-11/98-6298/mods.xml"
    effective_on: null
    type: "Notice"
    action: "Notice of public hearings."
    title: "Public Hearings Notice"
    cfr_refernces: [ ]
    document_number: "98-6298"
    end_page: 11872
    publication_date: "1998-03-11"
    volume: 63
    abstract: "The Commission on Structural Alternatives for the Federal Courts of Appeals has scheduled six public hearings to allow interested persons to comment on the Commission's work. The hearings will be in the following cities. The precise times and locations will be announced later."
    full_text_xml_url: "http://www.federalregister.gov/articles/xml/986/298.xml"
    start_page: 11872
    docket_id: null
    html_url: "http://www.federalregister.gov/articles/1998/03/11/98-6298/public-hearings-notice"
    abstract_html_url: "http://www.federalregister.gov/articles/html/abstract/986/298.html"
    dates: null
    pdf_url: "http://www.gpo.gov/fdsys/pkg/FR-1998-03-11/pdf/98-6298.pdf"
    body_html_url: "http://www.federalregister.gov/articles/html/full_text/986/298.html"
    comments_close_on: null
    regulation_id_numbers: [ ]
    -agencies: [
    -{
    url: "http://www.federalregister.gov/agencies/commission-on-structural-alternatives-for-the-federal-courts-of-appeals"
    json_url: "http://api.federalregister.gov/v1/agencies/68.json"
    name: "Commission on Structural Alternatives for the Federal Courts of Appeals"
    id: 68
    raw_name: "COMMISSION ON STRUCTURAL ALTERNATIVES FOR THE FEDERAL COURTS OF APPEALS"
    }
    ]
    }
    
    '''
    
    
    @classmethod
    def by_id(clz, article_id):
        raw = __fetch__(ARTICLE_ENDPOINT % article_id)
        return clz(raw)
    
    @classmethod
    def search(clz, query):
        raw = __fetch__("%s?%s" % (SEARCH_ENDPOINT, query))
        article_list = []
        for raw_article in raw:
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
        
    


