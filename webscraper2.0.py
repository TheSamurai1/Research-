from pip._vendor import requests
import re
from matplotlib import pyplot as plt
import time

def getWikipediaTitlesByCategory(categories, downstream=True, intersect=True, wiki_scanner='https://petscan.wmflabs.org/'):
    if type(categories) == list:
        categories = "\n".join(categories)

    depth = 1 if downstream else 0
    combination = "subset" if intersect else "union"
    url_catscan = wiki_scanner

    parameters = {
        'language': 'en',
        'project': 'wikipedia',
        'depth': depth,
        'categories': categories,
        'combination': combination,
        'format': 'json',
        'doit': 1
    }

    r = requests.get(url_catscan, params=parameters)
    articles_json = r.json()

    if not 'error' in articles_json:
        articles = articles_json["*"][0]['a']["*"]
        article_titles = [article["title"].replace("_", " ") for article in articles]
    else:
        article_titles = []
        print("ERROR: This may be a large query running at the same time as other people, or something else is going wrong. Try again later.")
        print(articles_json)

    return article_titles

#first american born is 1587




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


def extract_occupation(page_title):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{page_title.replace(' ', '_')}"
    response = requests.get(url)
    if response.status_code == 200:
        summary_data = response.json()
        return summary_data.get('description', 'No occupation found')
    else:
        return 'No occupation found'


def process_births(births_list, filename):
    regex = r'(?<=\+|\-)\d{4}|\d{4}'
    birthyear_X = []
    pagecreationyear_Y = []
    occupations = []

    with open(filename, "a") as f:
        for i in births_list:
            try:
                for collection in i:
                    try:
                        page_title = str(collection)
                        print(f"Processing: {page_title}")

                        first_revision_date = get_first_revision_date(page_title)
                        wikidata_id = get_wikidata_id(page_title)
                        birthdate = get_birthdate_from_wikidata(wikidata_id)
                        occupation = extract_occupation(page_title)

                        birthday_match = re.search(regex, birthdate)
                        if birthday_match:
                            first_four_birthday = birthday_match.group()
                            birthyear_X.append(int(first_four_birthday))
                        else:
                            continue

                        revision_date_match = re.search(regex, first_revision_date)
                        if revision_date_match:
                            first_four_date = revision_date_match.group()
                            pagecreationyear_Y.append(int(first_four_date))
                        else:
                            continue

                        occupations.append(occupation)
                        f.write(f"{first_four_birthday},{first_four_date},{occupation}\n")

                        # Add a delay between requests to avoid rate limits
                        time.sleep(1)  # Adjust the sleep duration as needed
                    except KeyError:
                        continue
            except KeyError:
                continue

    return birthyear_X, pagecreationyear_Y, occupations


# years_2000s = list(range(2001, 2024))
# birthsin2000s_americans_list = []

# for year in years_2000s:
#     birthyears = f"{year} births"
#     birthsin2000s_americans = getWikipediaTitlesByCategory([birthyears, "American people"])
#     birthsin2000s_americans_list.append(birthsin2000s_americans)
#     print(len(birthsin2000s_americans))

# birthyear_X_2000s, pagecreationyear_Y_2000s, occupations_2000s = process_births(birthsin2000s_americans_list, "webscrapernumbers2024last.txt")


#also have to do 2024 for the previous csv file as well


years_1960s = list(range(1587, 1588))
birthsin1960s_americans_list = []
for year in years_1960s:
    birthyears1960 = f"{year} births"
    print(birthyears1960)
    birthsin1960s_americans = getWikipediaTitlesByCategory([birthyears1960, "American people"])

    birthsin1960s_americans_list.append(birthsin1960s_americans)
    print(len(birthsin1960s_americans))

print(birthsin1960s_americans, "here here")
#birthyear_X_1960s, pagecreationyear_Y_1960s, occupations_1960s = process_births(birthsin1960s_americans_list, "justtesting.txt")