import os
import re

def process_and_overwrite_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as f:
                lines = f.readlines()

            # 处理链接并替换回文件
            with open(filepath, 'w') as f:
                for line in lines:
                    match = re.search(r'imgurl=(https?://.+?)(\||\&)', line)
                    if match:
                        link = match.group(1).replace('%25', '%')
                        f.write(link + '\n')

# 调用函数，替换为你实际的文件夹路径
process_and_overwrite_files('/storage/emulated/0/1a/jn/倒数第四关/nk/ok/')
