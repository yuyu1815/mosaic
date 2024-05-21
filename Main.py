import os,glob
from ocr import process_images

folder_path_1 = './Not_mosaic'
folder_path_2 = './mosaic'

image_files_1 = None
image_files_2 = None


def main():
    image_files_1 = glob.glob(os.path.join(folder_path_1, '*.jpg')) + glob.glob(os.path.join(folder_path_1, '*.png'))
    image_files_2 = glob.glob(os.path.join(folder_path_2, '*.jpg')) + glob.glob(os.path.join(folder_path_2, '*.png'))
    print("アップスケーリング")
    #upscaling.upscaling(image_files_1, image_files_2)
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

main()