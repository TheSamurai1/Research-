
filenames = ['webscraper1960last.txt', 'webscraper1975last.txt', 'webscraper1976last.txt', 'webscrapernumbers2024last.txt' ]
with open('alldatawebscraper.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)