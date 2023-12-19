SAVE_BASELINE = './post/'
THRESHOLD = 0.5
from tqdm import tqdm
import os
import json
from textblob import TextBlob
from spellchecker import SpellChecker

# Set the folder path containing JSON files
path_list = ['./pre1(png)', './pre2(png)']
# Get a list of all files in the folder
for pre_path in tqdm(path_list, desc="pre_path", unit="item"):
    folder_list1 = os.listdir(pre_path)
    for folder_name1 in tqdm(folder_list1, desc="folder_name1", unit="item"):
        folder_path1 = os.path.join(pre_path, folder_name1)
        folder_list2 = os.listdir(folder_path1)
        for folder_name2 in tqdm(folder_list2, desc="folder_name2", unit="item"):
            folder_path2 = os.path.join(folder_path1, folder_name2)
            folder_list3 = os.listdir(folder_path2)
            for file_name in tqdm(folder_list3, desc="file_name", unit="item"):
                if file_name.endswith('.json'):
                    file_path = os.path.join(folder_path2, file_name)
                    for mod_idx in tqdm(range(2), desc="mod_idx", unit="item"):
                        if mod_idx == 0:
                            with open(file_path, 'r', encoding='utf-8') as file:
                                data = json.load(file)
                            for i in range(len(data['result'])):
                                OCR_text = data['result'][i][1]
                                conf_score = data['result'][i][2]

                                spell = SpellChecker(language='en')
                                corrected_text = ''
                                for word in OCR_text.split():
                                    corrected_word = spell.correction(word) if spell.correction(
                                        word) is not None else word
                                    corrected_text += corrected_word + ' '

                                if (conf_score > THRESHOLD):
                                    data['result'][i][1] = corrected_text

                            save_path = SAVE_BASELINE + file_path[2:].split(".")[0] + "_SC" + ".json"

                            save_dir = os.path.dirname(save_path)
                            if not os.path.exists(save_dir):
                                os.makedirs(save_dir)

                            with open(save_path, 'w', encoding='utf-8') as file:
                                json.dump(data, file, ensure_ascii=False, indent=2)
                        else:
                            with open(file_path, 'r', encoding='utf-8') as file:
                                data = json.load(file)
                            for i in range(len(data['result'])):
                                OCR_text = data['result'][i][1]
                                conf_score = data['result'][i][2]

                                corrected_text = str(TextBlob(OCR_text).correct())

                                if (conf_score > THRESHOLD):
                                    data['result'][i][1] = corrected_text

                            save_path = SAVE_BASELINE + file_path[2:].split(".")[0] + "_TB" + ".json"

                            save_dir = os.path.dirname(save_path)
                            if not os.path.exists(save_dir):
                                os.makedirs(save_dir)

                            with open(save_path, 'w', encoding='utf-8') as file:
                                json.dump(data, file, ensure_ascii=False, indent=2)

                        print(save_path)
