import requests
import re
from bs4 import BeautifulSoup
import lxml
import msvcrt

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}


def get_films(soup):
    div_tags = soup.find_all(
        'div', class_=lambda x: x and x.startswith('really-lazy-load poster'))
    return ['https://letterboxd.com' + str(div_tag.get('data-target-link')) for div_tag in div_tags if div_tag.get('data-target-link')]


def get_info(response, soup):
    i = re.search(", runTime:", response.text).span()[1] + 1
    runtime = ''
    while (response.text[i].isnumeric()):
        runtime += response.text[i]
        i += 1
    year = ''
    if soup.find('small', class_='number'):
        year = soup.find('small', class_='number').text
    return (soup.find('h1', class_=lambda x: x and x.startswith('headline-1')).text + f" ({year})", int(runtime))


def main():
    url = input(
'''
Welcome to Scrapeboxd
You url needs to be in this format: https://letterboxd.com/director/charlie-kaufman
Make sure that there NO FILTERS activated like this: https://letterboxd.com/director/charlie-kaufman/by/rating/
Enter url: '''
                )
    if url[-1] == '/':
        url += 'by/longest/'
    else:
        url += '/by/longest/'
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    if response.status_code == 200:
        films_list = get_films(soup)
        sum = 0
        for film in films_list:
            response2 = requests.get(film, headers=HEADERS)
            soup2 = BeautifulSoup(response2.text, 'lxml')
            title, runtime = get_info(response2, soup2)
            print(title + " | " + str(runtime))
            sum += runtime
        if (sum / 60) // 24:
            print('Added up | ' + str(int((sum / 60) // 24)) + ' Day(s) and ' + str(round((sum / 60) % 24, 2)) + ' Hour(s)')
            exit()
        print('Added up | ' + str(sum / 60) + ' Hours')
    else:
        return 'Error ' + str(response.status_code)

main()
msvcrt.getch()
