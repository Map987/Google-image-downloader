import os
import requests
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed

# 定义文件目录
out_dir = '/storage/emulated/0/1a/jn/倒数第四关/nk/ok'
img_dir = '/storage/emulated/0/vipc/out'

# 创建图片目录，如果不存在的话
os.makedirs(img_dir, exist_ok=True)

# 定义下载图片的函数
def download_image(url, x):
    try:
        # 从URL中删除}-{x}x1024关键词
        keyword = f"-{x}x1024"
        modified_url = url.replace(keyword, "")

        # 从修改后的URL中提取图片名称
        img_name = modified_url.split('/')[-1]
        img_path = os.path.join(img_dir, img_name)

        # 下载图片
        r = requests.get(modified_url, allow_redirects=True)
        r.raise_for_status()

        # 计算图片大小并打印
        size_mb = len(r.content) / 1024 / 1024
        print(f"{size_mb:.2f} MB", end=' ')

        # 保存图片
        with open(img_path, 'wb') as f:
            f.write(r.content)

        # 打印EXIF信息
        img = Image.open(img_path)
        exif_data = img.getexif()
        if exif_data is None:
            print("- No EXIF", end=' ')
        else:
            model_tag = 0x0110
            if model_tag in exif_data:
                model = exif_data[model_tag]
                print(f"- Model: {model}", end=' ')

        print(f"- {modified_url}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {modified_url}: {e}")
    except Exception as e:
        print(f"Error processing {modified_url}: {e}")

# 使用线程池下载图片
with ThreadPoolExecutor(max_workers=128) as executor:
    for x in range(1, 1024):
        try:
            # 读取包含URLs的文件
            with open(f'{out_dir}/{x}.txt', 'r') as f:
                link_list = f.read().split()
                img_urls = [url for url in link_list if url.startswith('https://')]

            # 提交下载任务到线程池
            futures = [executor.submit(download_image, url, x) for url in img_urls]

            # 等待每个任务完成并打印结果
            for future in as_completed(futures):
                future.result()

        except FileNotFoundError:
            # 如果文件不存在，打印消息并继续下一个文件
            continue