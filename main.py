import argparse
import requests
from data_scraper import AudioLoader
from pathlib import Path
from bs4 import BeautifulSoup

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root","-r", required=True, type=Path,
                        help="Path to store json data")
    parser.add_argument("--client_id", "-i", type=str, required=True,
                        help="Client ID")
    parser.add_argument("--client_secret", "-s", type=str, required=True)
    parser.add_argument("--show_id", type=str, default="27XP61URSuKu9oeWR793D6")
    args = parser.parse_args()
    return args

def main():
    feed_url = "https://rss.art19.com/generation-do-it-yourself"
    page = requests.get(feed_url)
    soup = BeautifulSoup(page.content, "xml")
    audio = soup.find_all('item')[0]
    url = audio.find("enclosure")["url"]
    title = audio.find("title").text
    description = audio.find("description").text



if __name__=="__main__":
    main()