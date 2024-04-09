import os
import threading
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

input_folder_path = "/storage/emulated/0/down/okk/output_folder/q/oo/"

# 线程安全的队列
class LineQueue:
    def __init__(self):
        self.queue = []
        self.lock = threading.Lock()

    def put(self, item):
        with self.lock:
            self.queue.append(item)

    def get(self):
        with self.lock:
            return self.queue.pop(0) if self.queue else None

# 将文件内容加载到队列中
def load_file_to_queue(file_path, line_queue):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line_queue.put(line.strip())
    except Exception as e:
        print(f"Error loading file {file_path}: {e}")

# 下载并保存内容到对应文件夹，并实时更新文件
def download_and_update_file(line, line_queue, file_path, output_folder):
    try:
        response = requests.get(line)
        response.raise_for_status()

        # 创建以txt文件名命名的文件夹
        file_name = os.path.basename(file_path).split('.')[0]
        folder_path = os.path.join(output_folder, file_name)
        os.makedirs(folder_path, exist_ok=True)

        # 保存下载的内容
        output_file_name = os.path.basename(line)
        output_file_path = os.path.join(folder_path, output_file_name)
        with open(output_file_path, "wb") as f:
            f.write(response.content)

        # 更新文件，移除已处理的行
        with open(file_path, 'r') as file:
            lines = file.readlines()

        with open(file_path, 'w') as file:
            for l in lines:
                if l.strip() != line:
                    file.write(l)
    except Exception as e:
        print(f"Error processing line {line}: {e}")

# 主函数
def main():
    for file_name in os.listdir(input_folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(input_folder_path, file_name)
            line_queue = LineQueue()
            loader_thread = threading.Thread(target=load_file_to_queue, args=(file_path, line_queue))
            loader_thread.start()
            loader_thread.join()

            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(download_and_update_file, line, line_queue, file_path, input_folder_path) for line in line_queue.queue]
                for future in as_completed(futures):
                    future.result()

if __name__ == "__main__":
    main()
