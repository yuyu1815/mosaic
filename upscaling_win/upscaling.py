import subprocess
from tqdm import tqdm
import cv2


def load_image(image_path):
    # 画像を読み込む
    image = cv2.imread(image_path)
    return image



def upscaling(input_path1,input_path2, print_result=False,model="realesrgan-x4plus-anime",output_path="./.temp_up"):

    image_size1 = load_image(input_path1[0])
    image_size2 = load_image(input_path2[0])
    check_size = image_size1.shape[0] - image_size2.shape[0]

    if check_size < 0:
        upscal = input_path1
        no_upscal = input_path2
    elif check_size > 0:
        upscal = input_path2
        no_upscal = input_path1
    else:
        upscal = None

    if upscal is not None:
        for input_image in tqdm(upscal):

            result = subprocess.run(f"./upscaling_win/realesrgan-ncnn-vulkan.exe -i {input_image} -o {output_path}/{input_image} -n {model}",capture_output=True, text=True)
            if print_result:
                print(result)

        for input_image in tqdm(no_upscal):
            result = load_image(input_image)
            cv2.imwrite(f"{output_path}/{input_image}", result)
        print("ダウンスケール")
        downscaling(upscal,no_upscal)

    else:
        print("sizeを変更する必要がありません")
        for input_image in tqdm(input_path1):
            result = load_image(input_image)
            cv2.imwrite(f"{output_path}/{input_image}", result)

        for input_image in tqdm(input_path2):
            result = load_image(input_image)
            cv2.imwrite(f"{output_path}/{input_image}", result)


def downscaling(folder_path1, folder_path2,output_path="./.temp_up"):

    for temp in tqdm(range(len(folder_path1))):
        width, height, between_sizes_high, between_sizes_width = folder_path_get_image_size(f"{output_path}/{folder_path1[temp]}",f"{output_path}/{folder_path2[temp]}")

        if between_sizes_high > 0 and between_sizes_width > 0:
            #ダウンスケーリング
            img = load_image(folder_path2[temp])
            cv2.resize(img, (width, height))
            cv2.imwrite(f"{output_path}/{folder_path1[temp]}", img)
        else:
            img = load_image(folder_path1[temp])
            cv2.resize(img, (width, height))
            cv2.imwrite(f"{output_path}/{folder_path2[temp]}", img)

def folder_path_get_image_size(image_file,image_file2):
    imageA = load_image(image_file)
    imageB = load_image(image_file2)
    # 二つの画像を同じサイズにリサイズする
    # 最小の幅と高さを基にサイズを決定
    height = min(imageA.shape[0], imageB.shape[0])
    between_sizes_high = imageA.shape[0] - imageB.shape[0]
    width = min(imageA.shape[1], imageB.shape[1])
    between_sizes_width = imageA.shape[1] - imageB.shape[1]
    return (width, height,between_sizes_high,between_sizes_width)
