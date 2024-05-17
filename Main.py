import configparser
import easyocr
import os,glob
from tqdm import tqdm
from PIL import Image, ImageDraw

folder_path_1 = './Not_mosaic'
folder_path_2 = './mosaic'


image_files_1 = glob.glob(os.path.join(folder_path_1, '*.jpg')) + glob.glob(os.path.join(folder_path_1, '*.png'))
image_files_2 = glob.glob(os.path.join(folder_path_2, '*.jpg')) + glob.glob(os.path.join(folder_path_2, '*.png'))
#コンフィグからocr言語取得
config = configparser.ConfigParser()
config.read('Setting.ini', encoding='utf-8')
# 文字列として取得
language_string = config.get('setting', 'language')
# 文字列をリストに変換
#language_list = language_string.strip('[]').split(',')
#print(language_list)
language_list=['en','ch_sim']

def main():
    print("文字列削除")
    print(image_files_1)
    process_images(image_files_1)
    for image_file in tqdm(image_files_2):
        white_to_transparency(f'./mosaic/{image_file}', './temp_m')


def white_to_transparency(img_path, output_path):
    img = Image.open(img_path)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        # 白色のピクセルを透明に変更する (閾値を設定)
        if item[0] > 220 and item[1] > 220 and item[2] > 220:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(output_path, "PNG")

def process_images(image_files):
    reader = easyocr.Reader(language_list, gpu=True)
    for image_file in tqdm(image_files):
        # グレースケール画像でOCRを実行
        image_gray = Image.open(image_file).convert('L')
        image_gray.save(f"./temp_gray/{image_file.replace('.jpg', '_gray.png')}", "PNG")

        result = reader.readtext(f"./.temp_gray/{image_file.replace('.jpg', '_gray.png')}", paragraph=True)
        # 元のカラー画像を開く
        image = Image.open(image_file)
        draw = ImageDraw.Draw(image)

        # テキスト検出領域を白で塗りつぶす（元の画像上で）
        for item in result:  # 二つの結果を結合
            coordinates = item[0]
            polygon = [(x, y) for x, y in coordinates]
            draw.polygon(polygon, fill="white")

    image.save(f"./.temp/{ image_file.replace('.jpg', '.png')}", "PNG")
    white_to_transparency(f"./.temp/{image_file.replace('.jpg', '.png')}", "./temp_nm")



main()