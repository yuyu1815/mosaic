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
        white_to_transparency(f'./mosaic/{image_file}', './temp')


def white_to_transparency(img_path, output_path):
    img = Image.open(img_path)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        # 白色のピクセルを透明に変更する (閾値を設定)
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(output_path, "PNG")

def process_images(image_files):
    reader = easyocr.Reader(language_list, gpu=True)
    for image_file in tqdm(image_files):
        convert_to_black_and_white(image_file)

    for image_file in tqdm(image_files):
        result = reader.readtext(f"./.temp_g/{image_file.replace('.jpg', '.png')}", paragraph=True)
        # 元のカラー画像を開く
        image = Image.open(image_file)
        draw = ImageDraw.Draw(image)

        # テキスト検出領域を白で塗りつぶす（元の画像上で）
        for item in result:  # 二つの結果を結合
            coordinates = item[0]
            polygon = [(x, y) for x, y in coordinates]
            draw.polygon(polygon, fill="white")

        image.save(f"./.temp/{image_file.replace('.jpg', '.png')}", "PNG")

    for image_file in tqdm(image_files):
        white_to_transparency(f"./.temp/{image_file.replace('.jpg', '.png')}", f"./.temp/{image_file.replace('.jpg', '.png')}")


def convert_to_black_and_white(image_path, threshold=100):
    """
    画像を白と黒の二値化画像に変換する関数。

    :param image_path: 変換する画像のパス
    :param threshold: 二値化の閾値（0から255の間）。この値以上を白、未満を黒とする。
    :return: 二値化されたPillow画像オブジェクト
    """
    # 画像を読み込む
    image = Image.open(image_path)
    # グレースケールに変換
    image = image.convert('L')
    # 二値化を実行
    image = image.point(lambda x: 255 if x >= threshold else 0)
    # 二値化した画像を'L'モードで保存
    save_path = f"./.temp_g/{image_path.replace('.jpg', '.png')}"
    image.save(save_path, "PNG")

main()