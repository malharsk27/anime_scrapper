
############### D I S C L A I M E R ################
#                                                  #
# Downloading copyrighted media without the        #
# owner’s permission is illegal is some countries. #
# Under no circumstances is this script intended   #
# to encourage illegal activity, and there are     #
# no guarantees that this information will         #
# protect you from any legal action.               #
#                                                  #
####################################################



import requests
import re

from bs4 import BeautifulSoup

# The url  which has all the list of episodes in the series
HOME_URL = "http://animeheaven.eu/i.php?a=Hunter%20x%20Hunter%202011"

# Episode url prefix
EPISODE_PREFIX = "http://animeheaven.eu/"

# Episode url regex
REGEX = r'\bhttps?://\S+\.(?:mp4)\b'


# Return a list of all pages linked from HOME_URL
# that contain links to .mp4 files.
def get_episode_pages():

    episode_list = list()

    response = requests.get(HOME_URL)
    source = response.text

    soup = BeautifulSoup(source  ,'html.parser')
    results = soup.find_all(class_="infoepbox")
    
    for result in results:
        
        episodes = result.find_all("a")

        for episode in episodes:
            rel_episode_url = episode.get('href')
            episode_url = EPISODE_PREFIX + rel_episode_url
            episode_list.append(episode_url)

    return episode_list


# Use regex (argh...) to get the
# first  link on the page that ends with .mp4
# see the regex above.
def get_episode_url(page_link):

    response = requests.get(page_link)
    match = re.search(REGEX, response.text)
    if match:
        return match.group(0)
    return None


# Download the .mp4 video from the given url
# and save it in the same directory as this script
def download_episode(url):

    # The name of  the file to save the video as
    # eg. Hunter_2011--134--1462403967.mp4
    name = url[-32:]
    response = requests.get(url)

    with open(name, 'wb') as episode_file:

        for chunk in response.iter_content():
            if chunk:
                episode_file.write(chunk)
    


def main():

    episode_pages = get_episode_pages()
    episode_urls = list()

    print('Get all episodes urls.')

    for episode_page in episode_pages:
        url = get_episode_url(episode_page)
        episode_urls.append(url)

    print('Done!')

    # For testing, only download one .mp4 file
    # because of their size.
    print('Downloading the first episode.')
    download_episode(episode_urls[0])
    print('Done!')


if __name__ == '__main__':
    main()
