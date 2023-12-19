import os
import json
import random
import torch
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm
from glob import glob
from modeling import CustomLlamaStructure
import time

txt_list = glob('/home/jaeyoung/xai_ocr/pythonProject/a/pre2(png)/**/*.txt', recursive=True)

print(len(txt_list))

txt_list = random.sample(txt_list, 1000)
for txt_file in txt_list[100:101]:
    with open(txt_file, 'r', encoding='utf-8') as f:
        txt = f.read()

print(txt_file)

class Extract_shipment:
    def __init__(self, txt):
        self.txt = txt

    def fewshot_context(self):
        instruction = """
        Read the following OCR-extracted transport logistics document and extract the departure and destination locations.
        """
      
        # prompt = instruction + "\n" + answer_format + "\n context:" + self.txt
        prompt = instruction + "\n" + "OCR context: \n" + self.txt
        # prompt = instruction + "\n OCR context: \n" + self.txt

        return prompt

model_path = "/home/jaeyoung/llama-2-13b-hf"
max_seq_len = 2048
max_gen_len = 512
device = torch.device("cuda:7" if torch.cuda.is_available() else "cpu")

# LLAMA2-13b Model load
start = time.time()
llama2_13b_path = "/home/jaeyoung/llama-2-13b-hf"
model = CustomLlamaStructure(model_path,
            max_input_length=max_seq_len,
            max_output_length=max_gen_len,
            device=device,)

print(f"Loading time: {time.time() - start:.3f} sec")

def evaluate(txt,  model):
    prompt = Extract_shipment(txt).fewshot_context()
    print(prompt)
    print("=====================================================")
    pred = model.run(prompt)
    return pred

output_text = evaluate(txt, model)

print("=====================================================")
print("+++++++++++++++++++++OUTPUT+++++++++++++++++++++++++")
print(output_text)


