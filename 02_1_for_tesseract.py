from PIL import Image
import pytesseract
import os

# Tesseract 실행 파일의 경로 설정.
pytesseract.pytesseract.tesseract_cmd = '/Users/admin/Tesseract-OCR/tesseract.exe'

# 이미지 파일이 들어있는 최상위 폴더 경로를 지정.
top_folder_path = "/Users/admin/PycharmProjects/pythonProject/a/pre2(png)/LA/"

# 모든 하위 폴더와 그 안의 png 파일.
for folder_path, _, file_names in os.walk(top_folder_path):
    for file_name in file_names:
        if file_name.lower().endswith('.png'):
            # PNG 파일 경로
            image_path = os.path.join(folder_path, file_name)

            # 이미지 호출.
            image = Image.open(image_path)

            # OCR을 통해 텍스트 추출
            text = pytesseract.image_to_string(image)

            # 텍스트 파일 생성
            output_file_path = os.path.join(folder_path, f"{file_name.split('.')[0]}_output.txt")
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(text)

            print(f"추출된 텍스트가 {output_file_path}에 저장되었습니다.")
