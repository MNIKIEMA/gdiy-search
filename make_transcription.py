import json
import os

def make_transcript(directory):
    file_dict = {}

    # Loop through the directory
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            # Read the file
            audio = os.path.join(directory, filename)
            try:
                outputs = pipeline(audio,  task="transcribe",
                               return_timestamps=True)
                file_dict[filename.replace(".wav", "")] = outputs
            except:
                print(filename)
            # Add the filename as a key to the dictionary
            

    # save into json file
    with open('./transcription.json', 'w') as outfile:
        json.dump(file_dict, outfile, ident=3)