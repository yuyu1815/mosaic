import easyocr
import os,glob
from tqdm import tqdm
from PIL import Image, ImageDraw
from upscaling_win import upscaling



folder_path_1 = './Not_mosaic'
folder_path_2 = './mosaic'

image_files_1 = None
image_files_2 = None
language_list=['en','ch_sim']

def main():
    image_files_1 = glob.glob(os.path.join(folder_path_1, '*.jpg')) + glob.glob(os.path.join(folder_path_1, '*.png'))
    image_files_2 = glob.glob(os.path.join(folder_path_2, '*.jpg')) + glob.glob(os.path.join(folder_path_2, '*.png'))
    print("アップスケーリング")
    upscaling.upscaling(image_files_1, image_files_2)
    print("文字列削除")
    process_images(image_files_1)
"""
名前の入れ替えは諦めました
opnecvと白黒は相性悪い！！！
"""
"""
    for image_file in tqdm(image_files_2):
        white_to_transparency(image_file, f"./.temp/{image_file.replace('.jpg', '.png')}")
"""
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

def process_images(image_files,input_path="./.temp_up"):
    reader = easyocr.Reader(language_list, gpu=True)
    # グレー化
    for image_file in tqdm(image_files):
        convert_to_black_and_white(image_file)
    # テキスト検出
    for image_file in tqdm(image_files):
        result = reader.readtext(f"./.temp_g/{image_file.replace('.jpg', '.png')}", paragraph=True)
        # 元のカラー画像を開く
        image = Image.open(f"{input_path}/{image_file}")
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
    #image = image.point(lambda x: 255 if x >= threshold else 0)
    # 二値化した画像を'L'モードで保存
    save_path = f"./.temp_g/{image_path.replace('.jpg', '.png')}"
    image.save(save_path, "PNG")

main()