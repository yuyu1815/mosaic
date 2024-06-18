from tqdm import tqdm
from PIL import Image, ImageDraw
import easyocr, cv2
def black_and_white_to_transparency(img_path, output_path):
    img = Image.open(img_path)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        # 白色のピクセルを透明に変更する (閾値を設定)
        if item[0] >= 225 and item[1] >= 225 and item[2] >= 225:
            newData.append((0, 255, 0, 255))
        elif item[0] <= 60 and item[1] <= 60 and item[2] <= 60:
            newData.append((0, 0, 255, 255))
        else :
            newData.append(item)
    img.putdata(newData)
    img.save(output_path.replace('.jpg', '.png'), "PNG")
def black_to_transparency(img_path, output_path):
    img = Image.open(img_path)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] <= 60 and item[1] <= 60 and item[2] <= 60:
            newData.append(item)
        else:
            newData.append((0, 0, 0, 0))

    img.putdata(newData)
    img.save(output_path.replace('.jpg', '.png'), "PNG")

def black_and_white_to_transparency2(img_path, output_path):
    img = Image.open(img_path)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        # 白色のピクセルを透明に変更する (閾値を設定)
        if item[0] >= 225 and item[1] >= 225 and item[2] >= 225:
            newData.append((0, 0, 0, 0))
        elif item[0] <= 60 and item[1] <= 60 and item[2] <= 60:
            newData.append((0, 0, 0, 0))
        else :
            newData.append(item)
    img.putdata(newData)
    img.save(output_path.replace('.jpg', '.png'), "PNG")
def black_to_transparency(img_path, output_path):
    img = Image.open(img_path)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] <= 60 and item[1] <= 60 and item[2] <= 60:
            newData.append(item)
        else:
            newData.append((0, 0, 0, 0))

    img.putdata(newData)
    img.save(output_path.replace('.jpg', '.png'), "PNG")
def noise_delete(image_files,output_path="./.temp_up"):
    for image_file in tqdm(image_files):
        gray_image  = cv2.imread(image_file,0)
        img = cv2.bilateralFilter(gray_image, 9, 75, 75)
        cv2.imwrite(f"{output_path}/{image_file.replace('.jpg', '.png')}", img)

def process_images(image_files,input_path="./.temp_up"):
    language_list = ['en', 'ch_sim']
    print(f"image:{image_files}")
    reader = easyocr.Reader(language_list, gpu=True)
    # テキスト検出
    for image_file in tqdm(image_files):
        result = reader.readtext(f"{input_path}/{image_file.replace('.jpg', '.png')}", paragraph=True,width_ths=0.1,height_ths=0.1)
        # 元のカラー画像を開く

        image = Image.open(f"{input_path}/{image_file.replace('.jpg', '.png')}")
        draw = ImageDraw.Draw(image)

        # テキスト検出領域を白で塗りつぶす（元の画像上で）
        for item in result:
            coordinates = item[0]
            polygon = [(x, y) for x, y in coordinates]
            draw.polygon(polygon, fill="white")

        image.save(f"./.temp/{image_file.replace('.jpg', '.png')}", "PNG")

    #for image_file in tqdm(image_files):
    #    white_to_transparency(f"./.temp/{image_file.replace('.jpg', '.png')}", f"./.temp/{image_file.replace('.jpg', '.png')}")

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