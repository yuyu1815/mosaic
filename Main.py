import os,glob
from tqdm import tqdm
from ocr import process_images,black_and_white_to_transparency,black_to_transparency,noise_delete,black_and_white_to_transparency2
#外国語
folder_path_1 = './Not_mosaic'
#日本語
folder_path_2 = './mosaic'
#外国語
image_files_1 = None
#日本語
image_files_2 = None


def main():
    #モザイクなし
    image_files_1 = glob.glob(os.path.join(folder_path_1, '*.jpg')) + glob.glob(os.path.join(folder_path_1, '*.png'))
    #モザイクあり
    image_files_2 = glob.glob(os.path.join(folder_path_2, '*.jpg')) + glob.glob(os.path.join(folder_path_2, '*.png'))
    AI_mode = input("AIによる処理をしますか？（テスト中）y/n: ")
    print("AIモード" if AI_mode == "y" else "標準モード" )
    print("ノイズ除去")
    #noise_delete(image_files_1)
    #noise_delete(image_files_2)
    print("アップスケーリング")
    #upscaling.upscaling(image_files_1, image_files_2)

    if AI_mode == "y":
        print("色変化")
        for image_file in tqdm(image_files_1):
            black_to_transparency(image_file, f"./.temp_up/{image_file.replace('.jpg', '.png')}")
        print("文字列削除")
        process_images(image_files_1)
        #process_images(image_files_2)
        for image_file in tqdm(image_files_1):
            black_and_white_to_transparency2(image_file, f"./.temp/{image_file.replace('.jpg', '.png')}")

    else:
        print("色変化")
        for image_file in tqdm(image_files_2):
            black_and_white_to_transparency(image_file, f"./.temp/{image_file.replace('.jpg', '.png')}")


"""
名前の入れ替えは諦めました
opnecvと白黒は相性悪い！！！
"""

main()