import os
import re

def process_and_overwrite_files(directory):
    # 定义要保留的关键词列表
    keywords = ['.jpg?', '.webp?', '.png?', '.jpeg?']
    
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            # 提取文件名（无扩展名）
            x_value = os.path.splitext(filename)[0]
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # 处理链接并替换回文件
            with open(filepath, 'w', encoding='utf-8') as f:
                for line in lines:
                    # 替换链接中的关键词
                    keyword = f"-{x_value}x1024"
                    modified_line = line.replace(keyword, "")
                    match = re.search(r'imgurl=(https?://.+?)(\||\&)', modified_line)
                    if match:
                        link = match.group(1).replace('%25', '%')
                        f.write(link + '\n')
                    else:
                        f.write(modified_line)

                    # 检查每个链接中的关键词并保留前四个字符
                    for keyword in keywords:
                        # 查找关键词在行中的位置
                        index = modified_line.find(keyword)
                        # 如果找到，则保留前四个字符
                        if index != -1:
                            modified_line = modified_line[:index] + modified_line[index:index + len(keyword) - 1]
      
                            break
                    
                    # 检查是否是链接行并处理
                    
# 调用函数，替换为你实际的文件夹路径
                        

                    
                    # 检查每个链接中的关键词并保删除关键词的最后一个字符以及关键词之后的所有内容
                   
process_and_overwrite_files('/storage/emulated/0/down/okk/output_folder/')
