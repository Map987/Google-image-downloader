import requests
from bs4 import BeautifulSoup
import time  # 导入time模块
import random

start_page = 0  # 开始于第一页
end_page = 50  # 结束于第二页（索引从0开始，所以实际上是第二页的结果）
  # 用于跟踪当前页码
total_img_count = 0  # 用于跟踪总的图片数量
final_page = end_page - 1

start_resolution = 600
end_resolution = 700

ua_list = [
 
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
def get_with_retries(url, headers, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response
        time.sleep(2 ** attempt)  # 每次重试前等待
    return None
for resolution in range(start_resolution, end_resolution + 1):
    page_counter = start_page
    with open(f'/storage/emulated/0/600/{resolution}.txt', 'a') as f:
        start_time = time.time()  # 获取开始时间
        
        page = start_page
        while page <= final_page:
            headers = headers_list[random.randint(0, len(headers_list) - 1)]
            url = f'https://www.google.com.hk/search?q=TV+%E3%82%A2%E3%83%8B%E3%83%A1++imagesize:{resolution}x1024+-eeo.today&tbm=isch&start={page*20}&sa=N&lite=0&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'  # 填入你的URL
            
            response = get_with_retries(url, headers)
            if response is not None:
                soup = BeautifulSoup(response.text, 'html.parser')
                current_page_img_count = 0
                for a in soup.find_all('a', href=True):
                    if 'imgurl' in a['href']:
                        f.write(a['href'] + '\n')
                        current_page_img_count += 1
                        total_img_count += 1
                
                if current_page_img_count > 0:
                    print(f"page {page} (resolution:{resolution}) - {current_page_img_count} images")
                    page += 1
                    
                else:
                    print(f"No images found on page {page}. Skipping.")
                    break 
                
                # 无论是否找到图片，都移动到下一页
            else:
                print(f"Failed to retrieve page {page}. Skipping.")
                break   # 如果请求失败，也跳到下一页
        end_time = time.time()  # 获取结束时间
        execution_time = end_time - start_time  # 计算执行时间
        print(f"Execution time for resolution {resolution}x1024: {execution_time} seconds")  # 输出执行时间
