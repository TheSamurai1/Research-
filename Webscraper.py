from pip._vendor import requests
import os
from collections import OrderedDict 
import re

def getWikipediaTitlesByCategory( categories, downstream = True, intersect=True, wiki_scanner='https://petscan.wmflabs.org/' ):
  """
  we'll use another api called catscan2 to grab a list of pages in
  categories and subcategories. it works like all the other apis we've
  studied!
  
  The following requests call basically does the same thing as this string:
  "https://petscan.wmflabs.org/?language=en&project=wikipedia&depth=10&categories=American%20people%0D%0A1970%20births&ns%5B0%5D=1&search_max_results=500&interface_language=en&active_tab=&doit="
  
  Code cribbed from projects.mako.cc/harrypotter-wikipedia-cdsw
  """
  
  # function can take a single category or a list of them.  
  #  if it gets one, it turns it into a list
  if type(categories) == list:
    categories = "\n".join(categories)
  
  if downstream:
    depth = 10
  else: 
    depth = 0
  
  if intersect:
    combination = "subset"
  else:
    combination = "union"
  
  #url_catscan = "http://tools.wmflabs.org/catscan2/catscan2.php"
  #url_catscan = "https://petscan.wmflabs.org/"
  url_catscan = wiki_scanner

  parameters = {'language' : 'en',
                'project' : 'wikipedia',
                'depth' : depth,
                'categories' : categories,
                'combination' : combination,
                'format' : 'json',
                'doit' : 1}

  r = requests.get(url_catscan, params=parameters)
  articles_json = r.json() ### get the result into a handy format
  
  if not 'error' in articles_json:
    articles = articles_json["*"][0]['a']["*"]  #### work the result down more to the meat: the retrieved articles as a list
    article_titles = [ article["title"].replace("_", " ") for article in articles  ] 
  else:
    article_titles = []
    print("ERROR: This may be a large query running at the same time as other people, or something else is going wrong. Try again later.")
    print( articles_json )
  
  return( article_titles )


def get_first_revision_date(page_title):
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={page_title}&prop=revisions&rvlimit=1&rvdir=newer&format=json"
    response = requests.get(url)
    data = response.json()
    page_id = next(iter(data['query']['pages']))
    revision_date = data['query']['pages'][page_id]['revisions'][0]['timestamp']
    return revision_date

def get_wikidata_id(page_title):
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={page_title}&prop=pageprops&format=json"
    response = requests.get(url)
    data = response.json()
    page_id = next(iter(data['query']['pages']))
    wikidata_id = data['query']['pages'][page_id]['pageprops']['wikibase_item']
    return wikidata_id

def get_birthdate_from_wikidata(wikidata_id):
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={wikidata_id}&props=claims&format=json"
    response = requests.get(url)
    data = response.json()
    birthdate = data['entities'][wikidata_id]['claims']['P569'][0]['mainsnak']['datavalue']['value']['time']
    return birthdate

birthsin2000s_americans_list = []
for famous_people in range(2001, 2003):
   birthyears = str(famous_people) + " births"
   birthsin2000s_americans = getWikipediaTitlesByCategory([birthyears, "American people"]) # 🚀
   birthsin2000s_americans_list.append(birthsin2000s_americans)
   print(len(birthsin2000s_americans))
  

counter = 0 
birthday = []
birthyear_X = []
pagecreationyear_Y = []
dict = {}
regex = r'(?<=\+|\-)\d{4}|\d{4}'
for i in birthsin2000s_americans_list:
    try:
        for collection in i:
          try:
            page_title = str(collection)
            print(collection, "collection")
            first_revision_date = get_first_revision_date(page_title)
            wikidata_id = get_wikidata_id(page_title)
            birthdate = get_birthdate_from_wikidata(wikidata_id)
            birthday = re.search(regex, birthdate)
            if birthday:
              first_four_birthday = birthday.group()
              birthyear_X.append(int(first_four_birthday))
              print(f"The first four XXXXXX digits are: {first_four_birthday}")
            else:
              print("No match found")
            first_revision_date = re.search(regex, first_revision_date)
            if first_revision_date:
              first_four_date = first_revision_date.group()
              pagecreationyear_Y.append(int(first_four_date))
              print(f"The first four YYYYYYY digits are: {first_four_date}")
            else:
              print("No match found")
          except KeyError:
             continue
        # print(f"The first revision date of {page_title} is {first_revision_date}")
        # print(f"The birthdate of {page_title} is {birthdate}")
    except KeyError:
       continue

print(birthyear_X, "Birth YEAR")
print(pagecreationyear_Y, "PAGE CREATION")

