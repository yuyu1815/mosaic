from PIL import Image
import cv2
from skimage.metrics import structural_similarity as ssim
import os
def replace(mozaic_path, n_mozaic_path, save_pach="./temp_up"):
    for mosaic_image,n_mosaic_image in mozaic_path, n_mozaic_path:
        img1 = Image.open(mosaic_image)
        img2 = Image.open(n_mosaic_image)
        if img1.width < img2.width:
            img2 = img2.resize((img1.width, img1.height))
            img2.save(save_pach)
        else:
            img1 = img1.resize((img2.width, img2.height))
            img1.save(save_pach)

def change_name(mosaic_path, n_mosaic_path, save_pach="./temp_up"):
    max_similarity = -1
    most_similar_pair = ("", "")

    for n_mosaic_image_path in n_mosaic_path:
        n_mosaic_image = cv2.imread(n_mosaic_image_path)
        for mosaic_image_path in mosaic_path:
            mosaic_image = cv2.imread(mosaic_image_path)

            similarity = calculate_similarity(n_mosaic_image, mosaic_image)
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_pair = (n_mosaic_image_path, mosaic_image_path)

    if most_similar_pair != ("", ""):
        # 画像の名前を取得
        _, n_mosaic_filename = os.path.split(most_similar_pair[0])
        _, mosaic_filename = os.path.split(most_similar_pair[1])

        # n_mozaic_image を mozaic_image と同じ名前で保存ディレクトリに保存
        n_mosaic_image = cv2.imread(most_similar_pair[0])
        cv2.imwrite(f"Not_mosaic/{mosaic_filename}", n_mosaic_image)  # 画像を保存

        print(f"Saved {n_mosaic_filename} as {mosaic_filename}")

    # 画像の類似度を計算する関数
def calculate_similarity(imageA, imageB):
    # 画像をグレースケールで読み込む
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
    # SSIMを計算
    s = ssim(grayA, grayB)
    return s



