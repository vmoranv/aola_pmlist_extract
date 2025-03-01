import os
import re
from pathlib import Path
import argparse

def split_pm_data(input_path, output_dir):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配类似 "public static const pmSkillMap:Object = {...}" 的结构
    pattern = re.compile(r'public static const (\w+):Object = {(.*?)};', re.DOTALL)
    matches = pattern.finditer(content)
    
    # 创建输出目录
    package_path = os.path.join(output_dir)
    os.makedirs(package_path, exist_ok=True)

    for match in matches:
        class_name = match.group(1)
        content = match.group(2).strip()
        
        # 生成类文件内容
        class_content = f"""package mmo.pm.data
{{
    public class {class_name} extends PMDataBase
    {{
        public static const dataMap:Object = {{
{content}
        }};
    }}
}}"""
        
        # 写入文件
        output_path = os.path.join(package_path, f"{class_name}.as")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(class_content)
        print(f"生成: {output_path}")

if __name__ == "__main__":
    input_file = input("请输入PMDataList.as文件路径：").strip()
    output_dir = input("请输入输出目录（默认split_classes）：").strip() or "split_classes"
    
    if not os.path.exists(input_file):
        print(f"错误: 输入文件 {input_file} 不存在喵~")
        exit(1)
        
    split_pm_data(input_file, output_dir)
