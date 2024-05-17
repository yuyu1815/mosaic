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
language_list = language_string.strip('[]').split(',')
reader = easyocr.Reader(language_list)

def main():
    print("文字列削除")
    print(image_files_1)
    process_images(image_files_1, reader)
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

def process_images(image_files, reader):
    for image_file in tqdm(image_files):
        result = reader.readtext(image_file)

        image = Image.open(image_file)
        draw = ImageDraw.Draw(image)

        # 各領域を白で塗りつぶす
        for item in result:
            coordinates = item[0]
            # 座標を変換して四角形を描画
            polygon = [(x, y) for x, y in coordinates]
            draw.polygon(polygon, fill="white")

        image.save(f"./.temp/{ image_file}", "PNG")
        white_to_transparency(f"./.temp/{image_file}", "./temp_nm")

main()