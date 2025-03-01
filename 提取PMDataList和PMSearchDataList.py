import os
import shutil
import requests
import subprocess
from tqdm import tqdm

class SwfExtractor:
    def __init__(self, swf_url, output_dir, ffdec_path):
        self.swf_url = swf_url
        self.output_dir = output_dir
        self.swf_file = "pmservice.swf"
        self.ffdec_path = ffdec_path
        
        os.makedirs(self.output_dir, exist_ok=True)

    def download_swf(self):
        """下载 SWF 文件"""
        print(f"正在下载 {self.swf_url} ...")
        response = requests.get(self.swf_url, stream=True)
        total_size = int(response.headers.get("Content-Length", 0))
        block_size = 1024

        with open(self.swf_file, "wb") as f, tqdm(
            desc="下载进度",
            total=total_size,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for data in response.iter_content(block_size):
                size = f.write(data)
                progress_bar.update(size)
                
        print(f"SWF 文件已下载到: {os.path.abspath(self.swf_file)}")
        
        # 检查下载的文件是否存在且大小不为0
        if not os.path.exists(self.swf_file) or os.path.getsize(self.swf_file) == 0:
            raise Exception("SWF 文件下载失败，请检查网络连接并重试")

    def decompile_swf(self):
        """使用 ffdec 反编译 SWF 文件并提取目标类"""
        if not os.path.exists(self.ffdec_path):
            raise Exception(f"未找到 ffdec.jar: {self.ffdec_path}")
        
        command = [
            "java", "-jar", self.ffdec_path,
            "-format", "script:as",
            "-onerror", "ignore",
            "-selectclass", "mmo.pm.data.PMDataList,mmo.pm.data.PMSearchDataList",
            "-export", "script", self.output_dir,
            os.path.abspath(self.swf_file)
        ]
        
        print("正在反编译 SWF 文件并提取目标类...")
        print(f"命令: {' '.join(command)}")
        
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"反编译失败: {result.stderr}")
        print("反编译和提取完成")
        
        print("\n提取的文件:")
        print(os.path.join(self.output_dir, "PMDataList.as"))
        print(os.path.join(self.output_dir, "PMSearchDataList.as"))
        
        # 移动文件并清理目录
        self.reorganize_files()

    def reorganize_files(self):
        """重组文件结构并清理空目录"""
        src_dir = os.path.join(self.output_dir, "scripts", "mmo", "pm", "data")
        target_files = ["PMDataList.as", "PMSearchDataList.as"]

        for filename in target_files:
            src = os.path.join(src_dir, filename)
            dst = os.path.join(self.output_dir, filename)
            shutil.move(src, dst)

        # 自底向上删除空目录
        for root, dirs, files in os.walk(self.output_dir, topdown=False):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    print(f"已删除空目录: {dir_path}")

    def cleanup(self):
        """清理临时文件"""
        try:
            os.remove(self.swf_file)
            print("临时文件已清理")
        except Exception as e:
            print(f"清理临时文件时出错: {str(e)}")

    def run(self):
        try:
            self.download_swf()
            self.decompile_swf()
        finally:
            self.cleanup()

def main():
    swf_url = "https://aola.100bt.com/play/pet/pmservice.swf"
    output_dir = "extracted_classes"
    
    ffdec_path = input("请输入 ffdec.jar 的路径: ").strip()
    if not ffdec_path:
        print("错误: 请提供 ffdec.jar 的路径")
        return
    
    extractor = SwfExtractor(swf_url, output_dir, ffdec_path)
    extractor.run()
    
    print(f"\n提取完成，类文件已保存到: {output_dir}")

if __name__ == "__main__":
    main()