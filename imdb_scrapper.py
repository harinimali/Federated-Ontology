import json
import urllib2

import bs4
import pandas as pd

link = "http://www.imdb.com/list/ls003982198/?start={start}&view=compact&sort=listorian:asc&defaults=1&scb=0.18110136267582844"


# http://www.imdb.com/list/ls009318269/?start={start}&view=compact&sort=listorian:asc&defaults=1&scb=0.9850415633184224

def scrape_movies(url):
    print 'Parsing ', url
    html = urllib2.urlopen(url).read()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    imdb_movies = []
    rows = soup.findAll("tr")[1:]
    for row in rows:
        movie = {}
        for detail in row.findAll("td"):
            try:
                # Fetching Title, Year and Rating
                if detail['class'][0].encode('ascii', 'ignore') == 'year':
                    movie.update({'Movie-ReleaseYear': detail.text.encode('ascii', 'ignore')})
                elif detail['class'][0].encode('ascii', 'ignore') == 'user_rating':
                    movie.update({'Movie-Rating': detail.text.encode('ascii', 'ignore')})
                elif detail['class'][0].encode('ascii', 'ignore') == 'title':
                    movie.update({'Movie-Name': detail.text.encode('ascii', 'ignore')})
                    movie_url = 'http://www.imdb.com' + detail.a['href']
                    movie.update({'Movie-URL': str(movie_url)})
                    movie_html = urllib2.urlopen(movie_url).read()
                    movie_soup = bs4.BeautifulSoup(movie_html, 'html.parser')
                    awards_url = movie_url + 'awards?ref_=tt_awd'
                    awards_html = urllib2.urlopen(awards_url).read()
                    awards_soup = bs4.BeautifulSoup(awards_html, 'html.parser')

                    try:
                        # Fetching Directors, Writers and Cast
                        for credit_summary_item in movie_soup.find_all('div', {'class': 'credit_summary_item'}):
                            if credit_summary_item.find('span')['itemprop'].encode('ascii', 'ignore') == 'director':
                                directors = [director.text.encode('ascii', 'ignore').strip() for director in
                                             credit_summary_item.find_all('span', {'itemprop': 'director'})]
                                movie.update({'Movie-Director': ' '.join(directors)})
                            elif credit_summary_item.find('span')['itemprop'].encode('ascii', 'ignore') == 'creator':
                                creators = [creator.text.encode('ascii', 'ignore').strip() for creator in
                                            credit_summary_item.find_all('span', {'itemprop': 'creator'})]
                                movie.update({'Movie-Writers': ' '.join(creators)})

                            elif credit_summary_item.find('span')['itemprop'].encode('ascii', 'ignore') == 'actors':
                                actors = [actor.text.encode('ascii', 'ignore').strip() for actor in
                                          credit_summary_item.find_all('span', {'itemprop': 'actors'})]
                                movie.update({'Movie-Cast': ' '.join(actors)})

                        # Fetching Languages and Runtime
                        for tech_detail in movie_soup.find('div', {'class': 'article', 'id': 'titleDetails'}).find_all(
                                'div', {'class': 'txt-block'}):
                            tech_detail = tech_detail.text.encode('ascii', 'ignore').replace('\n', '').split(':')
                            if len(tech_detail) != 2:
                                continue
                            item = tech_detail[0].strip()
                            value = tech_detail[1].strip()
                            if item == 'Language':
                                movie.update({'Movie-Languages': value})
                            elif item == 'Runtime':
                                movie.update({'Movie-Runtime': value})
                            if 'Movie-Languages' in movie and 'Movie-Runtime' in movie:
                                break

                        # Fetching Genres
                        genres = \
                            movie_soup.find('div', {'itemprop': 'genre'}).text.encode('ascii', 'ignore').replace('\n',
                                                                                                                 '').split(
                                ':')[1]
                        movie.update({'Movie-Genres': genres})
                    except Exception as e:
                        print("Error while processing {}".format(movie_url)), ':', e

                    try:
                        # Fetching Awards
                        awards_list = []
                        for awards in awards_soup.find_all('td', {'class': 'title_award_outcome'}):
                            if awards.b.text.encode('ascii', 'ignore').strip() == 'Won':
                                awards_list.append(awards.span.text.encode('ascii', 'ignore').strip())
                        movie.update({'Movie-Awards': ','.join(awards_list)})

                    except Exception as e:
                        print("Error while processing {}".format(awards_url)), ':', e

            except Exception as e:
                print("Error while processing {}".format(url)), ':', e
        imdb_movies.append(movie)
    return imdb_movies


def scrape_many(start=1,
                step=250,
                pages=7,
                second_delay=1,
                url_format=link):
    """
    Start at _start_, increase in steps of size _step_, and scrape _pages_ pages total

    Default IMDB url loads 50 movies per page
    """
    movies = []
    for i in range(pages):
        print("Scraping results starting at {}".format(start))
        movies.extend(scrape_movies(url_format.format(start=start)))
        start += step
        # time.sleep(second_delay)
    return movies


def save_movies(movies, path):
    with open(path, 'w') as f:
        json.dump(movies, f, sort_keys=True, indent=4,
                  separators=(',', ': '))


def load_movies(path):
    with open(path, 'r') as f:
        movies = json.load(f)
    return movies


if __name__ == '__main__':
    movies = scrape_many()
    imdb_df = pd.DataFrame(movies)
    print imdb_df.head()
    imdb_df.to_csv('imdb.csv')
