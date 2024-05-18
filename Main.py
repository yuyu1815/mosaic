import easyocr
import os,glob
from tqdm import tqdm
from PIL import Image, ImageDraw
from upscaling_win import upscaling
from collections import Counter

folder_path_1 = './Not_mosaic'
folder_path_2 = './mosaic'

image_files_1 = None
image_files_2 = None
# 文字列をリストに変換
language_list=['en','ch_sim']

def main():
    which_folder = which_folder_get_image_sizes(folder_path_1, folder_path_2)
    print("アップスケーリング")
    if which_folder:
        upscaling.upscaling(which_folder[0])
        print("ダウンスケーリング")
        if which_folder[1] == 1:
            downscaling(folder_path_1, folder_path_2)
        else:
            downscaling(folder_path_2, folder_path_1)
    which_folder = downscaling(folder_path_1, folder_path_2)

    print("文字列削除")
    image_files_1 = glob.glob(os.path.join(folder_path_1, '*.jpg')) + glob.glob(os.path.join(folder_path_1, '*.png'))
    image_files_2 = glob.glob(os.path.join(folder_path_2, '*.jpg')) + glob.glob(os.path.join(folder_path_2, '*.png'))
    #process_images(image_files_1)
    for image_file in tqdm(image_files_2):
        white_to_transparency(image_file, f"./.temp/{image_file.replace('.jpg', '.png')}")

def downscaling(folder_path1, folder_path2):

    for image_file1,image_file2 in folder_path1, folder_path2:
        width1, height1 = folder_path_get_image_size(image_file1)
        width2, height2 = folder_path_get_image_size(image_file2)
        between_sizes_high = width1 - width2
        between_sizes_width = height1 - height2
        

def folder_path_get_image_size(image_file):
    image = Image.open(image_file)
    width, height = image.size
    return (width, height)

def which_folder_get_image_sizes(folder_path1, folder_path2):
    most_frequent_resolution1 = folder_path_get_image_sizes(folder_path1)
    most_frequent_resolution2 = folder_path_get_image_sizes(folder_path2)

    if most_frequent_resolution1[0] > most_frequent_resolution2[0] or most_frequent_resolution1[1] > most_frequent_resolution2[1]:
        #2をアップスケーリング
        return folder_path2,2
    elif most_frequent_resolution1[0] < most_frequent_resolution2[0] or most_frequent_resolution1[1] < most_frequent_resolution2[1]:
        #1をアップスケーリング
        return folder_path1,1
    else:
        return None

def folder_path_get_image_sizes(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png'))]
    image_sizes = []
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        image = Image.open(image_path)
        width, height = image.size
        image_sizes.append((image_file, width, height))
    most_frequent_resolution = Counter(image_sizes).most_common(1)[0][0]
    return most_frequent_resolution


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