import subprocess
from tqdm import tqdm
def upscaling(input_path, print_result=False,model="realesrgan-x4plus-anime"):
    for input_image in tqdm(input_path):
        result = subprocess.run(f"./upscaling_win/realesrgan-ncnn-vulkan.exe -i {input_image} -o {input_image} -n {model}")
        if print_result:
            print(result)