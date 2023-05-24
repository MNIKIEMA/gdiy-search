from tqdm.auto import tqdm
import json
import argparse
import os

with open("./audio_info.json", encoding="utf-8") as f:
    episode_info = json.load(f)


transcription_path = "./gdiy_json_data/"


def process(transcription, episode_info):

    new_data = []

    window = 13  # number of sentences to combine
    stride = 3  # number of sentences to 'stride' over, used to create overlap
    # print(episode_info[0].keys())
    for episode_id in tqdm(os.listdir(transcription_path)):
        with open(os.path.join(transcription_path, episode_id), encoding="utf-8") as f:
            episode_data = json.load(f)
            # print(episode_data["chunks"][0].keys())
        for name, data in episode_data.items():
            data = data['chunks']
            # Align episode info with the transcription
            #episode_data = [ep_info for ep_info in episode_info if ep_info["name"].startswith("#"+episode_id[11:])][0]
            # print(episode_data["name"], episode_id)
            if name in episode_info:
                for i in range(0, len(data), stride):
                    i_end = min(len(data)-1, i+window)
                    
                    text = " ".join([text['text'] for text in data[i:i_end]])
                    new_data.append({
                        'start':  data[i]['timestamp'][0],
                        'end': data[i_end]['timestamp'][1],
                        'title': episode_info[name],
                        'text': text,
                    })
    return new_data



def parse_args():

    parser =argparse.ArgumentParser()
    parser.add_argument()
    args = parser.parse_args()
    
    return args


def main():
    data = process(transcription_path, episode_info)

    with open("./dataset.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


if __name__=="__main__":
    main()