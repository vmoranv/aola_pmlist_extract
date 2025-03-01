import sys

def silent_deduplicate():
    file_path = input("请输入文件路径喵~：").strip()
    seen = set()
    output_lines = []
    
    with open(file_path, 'r+', encoding='utf-8') as f:
        lines = f.readlines()
        f.seek(0)
        f.truncate()
        
        for line in lines:
            parts = line.split('"')
            if len(parts) >= 18:
                keyword = parts[9].strip()
                if keyword and keyword not in seen:
                    seen.add(keyword)
                    output_lines.append(line)
            else:
                output_lines.append(line)  # 保留格式异常的行
        
        f.writelines(output_lines)
    
    print(f"去重完成喵~ 共处理 {len(lines)} 行，保留 {len(output_lines)} 行【摇尾巴】")

if __name__ == "__main__":
    silent_deduplicate()
