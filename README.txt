This is a python client for the Federal Register (http://www.federalregister.gov/blog/learn/developers).

Example usage:

    from federal_register import agencies, Agency, Article
    
    agency_list = agencies()
    print len(agency_list) #outputs number of agencies submitting documents
    print agency_list[0] #outputs first agency in list

Please see the tests section for complete usage details.