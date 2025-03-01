import os
from pathlib import Path

def extract_lines():
    # 获取用户输入（用肉垫按回车）
    file_path = input("请输入文件路径喵~：").strip('"')
    keyword = input("请输入要查找的字符喵~：")
    
    try:
        # 处理文件路径
        src_file = Path(file_path)
        if not src_file.exists():
            print("文件不存在喵~（眼泪汪汪）")
            return
        
        # 准备新文件名
        suffix = src_file.suffix
        new_name = f"{src_file.stem}_filtered{suffix}"
        dest_file = src_file.with_name(new_name)
        
        # 逐行扫描（尾巴扫过屏幕）
        matched_lines = []
        with open(src_file, 'r', encoding='utf-8') as f:
            for line in f:
                if keyword in line:
                    matched_lines.append(line)
        
        # 写入结果（胸脯压住保存按钮）
        with open(dest_file, 'w', encoding='utf-8') as f:
            f.writelines(matched_lines)
            
        print(f"（满足地呼噜）找到{len(matched_lines)}行匹配内容\n"
              f"新文件保存在：{dest_file.absolute()}喵~")
    
    except Exception as e:
        print(f"（耳朵耷拉）出错了喵~：{str(e)}")

if __name__ == "__main__":
    extract_lines() 