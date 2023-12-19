import easyocr
import os
import cv2
from tqdm import tqdm
import json
import numpy as np

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

reader = easyocr.Reader(['en'], detect_network='dbnet18', recog_network = 'standard', gpu=True) # this needs to run only once to load the model into memory

data_path = "imgdata"
files = os.listdir(data_path)

for file in tqdm(files):
    img = cv2.imread(os.path.join(data_path, file))
    result = reader.readtext(os.path.join(data_path, file), detail=1)
    for box in result:
        img = cv2.rectangle(img, (int(box[0][0][0]), int(box[0][0][1])), (int(box[0][2][0]), int(box[0][2][1])), (255, 0, 0), 1)
    # save detect result
    cv2.imwrite(os.path.join("results/img", file), img)
    
    # save detect result to json
    name = os.path.splitext(file)[0]
    tmp = dict()
    tmp['name'] = file
    tmp['result'] = result
    with open(f"results/json/{name}.json", 'w', encoding="UTF-8") as f:
        json.dump(tmp, f, cls=NpEncoder, indent='\t')
