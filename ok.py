import requests
from bs4 import BeautifulSoup
import time  # 导入time模块
import random

start_page = 0  # 开始于第一页
end_page = 50  # 结束于第二页（索引从0开始，所以实际上是第二页的结果）
  # 用于跟踪当前页码
total_img_count = 0  # 用于跟踪总的图片数量
final_page = end_page - 1

start_resolution = 700
end_resolution = 800

ua_list = [
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; LG; Optimus 7)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; NOKIA; Lumia 800)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; NOKIA; Lumia 900)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; SAMSUNG; SGH-i647)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; LG; Optimus 7)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; NOKIA; Lumia 800)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; NOKIA; Lumia 900)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; SAMSUNG; SGH-i647)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; LG; Optimus 7)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; NOKIA; Lumia 800)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; NOKIA; Lumia 900)',
    ]

headers_list = [{'User-Agent': ua} for ua in ua_list]
headers = {'User-Agent': 'Nokia6600/1.0'}

for resolution in range(start_resolution, end_resolution + 1):
    page_counter = start_page
    with open(f'/storage/emulated/0/vipc/{resolution}.txt', 'a') as f:
        start_time = time.time()  # 获取开始时间
        
        for page in range(start_page, final_page + 1):
            headers = headers_list[random.randint(0, len(headers_list) - 1)]
            url = f'https://www.google.com.hk/search?q=TV+%E3%82%A2%E3%83%8B%E3%83%A1++imagesize:{resolution}x1024+-eeo.today&tbm=isch&start={page*20}&sa=N&lite=0&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
             
                print("Received 200 response")
            soup = BeautifulSoup(response.text, 'html.parser')

            # 初始化当前页图片计数器
            current_page_img_count = 0

            for a in soup.find_all('a', href=True):
                if 'imgurl' in a['href']:
                    
                    f.write(a['href'] + '\n')
                    current_page_img_count += 1
                    total_img_count += 1  # 更新总的图片数量

            # 打印处理页数和图片数量
            print(f"page {page_counter} (resolution:{resolution}) - {current_page_img_count} images")
            page_counter += 1  # 更新页码计数器

        end_time = time.time()  # 获取结束时间
        execution_time = end_time - start_time  # 计算执行时间
        print(f"Execution time for resolution {resolution}x1024: {execution_time} seconds")  # 输出执行时间