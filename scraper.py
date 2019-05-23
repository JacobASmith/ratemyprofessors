import scraperwiki
from bs4 import BeautifulSoup
import string
import unicodedata
import time

headers = ["Name","Department","Total Ratings","Overall Quality","Easiness","Hot"]
#Dictionary of school ids (keys) that map to tuple of school name and number of pages
colleges = {"580":("MIT",21),"1222":("Yale",29),"181":("CMU",41), "1085":("UChicago",34),"1040":("Tufts",63), "1350":("Duke",118),"1255":("UTexas",180),"953":("Stanford",40),"799":("Rice",20),"780":("Princeton",20),"1232":("UNC",160)}

for sid in colleges.keys():
    college,pages = colleges[sid]
    print college
    for i in xrange(1,pages+1):
        response = scraperwiki.scrape("http://www.ratemyprofessors.com/SelectTeacher.jsp?sid=%s&pageNo=%s" % (sid,str(i)))
        time.sleep(5)
        soup = BeautifulSoup(response)
        rows = soup.find_all("div",{"class":"entry odd vertical-center"})
        rows.extend(soup.find_all("div",{"class":"entry even vertical-center"}))
        for row in rows:
            columns = row.find_all('div')
            columns = columns[3:]
            variables = {}
            for i,col in enumerate(columns):
                value = unicodedata.normalize('NFKD', col.text).encode('ascii', 'ignore')
                variables[headers[i]] = value
            variables["College"] = college
            scraperwiki.sqlite.save(unique_keys=['Name',"Department"], data = variables)
    

