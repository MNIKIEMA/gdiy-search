import re
import json, os
from tqdm.auto import tqdm
from pathlib import Path, PurePath
import requests
from bs4 import BeautifulSoup


class AudioLoader(object):
    def __init__(self, data_path):
        self.data_path = data_path
        self.loaded_episodes = self.load_loaded_episodes()
    
    def load_loaded_episodes(self):
        if not os.path.exists(os.path.join(self.data_path,'loaded_episodes.json')):
            with open(os.path.join(self.data_path,'loaded_episodes.json'), 'w') as f:
                json.dump([], f)
        with open(os.path.join(self.data_path,'loaded_episodes.json'), 'r') as f:
            return set(json.load(f))
        
    def update_loaded_episodes(self, episode_id):
        self.loaded_episodes.add(episode_id)
        with open(os.path.join(self.data_path,'loaded_episodes.json'), 'w') as f:
            json.dump(list(self.loaded_episodes), f)
    
    def load_data(self, feed_url):
        page = requests.get(feed_url)
        soup = BeautifulSoup(page.content, "xml")
        return soup.find_all('item')
    
    def process_data(self):
        audio_to_skip = ["[EXTRAIT]","[EXTRACT]","[REDIFF]"]
        data = self.load_data("https://rss.art19.com/generation-do-it-yourself")
        for episode in tqdm(data):
            link = episode.find("enclosure")["url"]
            title = episode.find("title").text
            episode_id = " ".join(title.split(" - ")[:-1]).replace("#", "")
            episode_id = re.sub(r'[%/!@#\*\$\?\+\^\\\\\\]', '', episode_id)
            print(episode_id)
            skip = [skip_audio for skip_audio in audio_to_skip if skip_audio in title]
            print(skip)
            if not skip:

                if episode_id not in self.loaded_episodes:
                    self.download_episode(link, episode_id)
                    self.update_loaded_episodes(episode_id)

    def download_episode(self, episode_url, audio_name):
        audio = requests.get(episode_url)
        with open(os.path.join(self.data_path, audio_name+".mp3"), "wb") as fp:
            fp.write(audio.content)


def main():
    feed_url = "https://rss.art19.com/generation-do-it-yourself"
    #page = requests.get(feed_url)
    #soup = BeautifulSoup(page.content, "xml")
    #print(soup.find_all('item')[0].find("enclosure")["url"])
    data = AudioLoader("./data/")
    data.process_data()


if __name__=="__main__":
    main()