import os
import chardet

def count_words_in_file(file_path):
    """统计单个文件的字数"""
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
        content = raw_data.decode(encoding, errors='replace')
        return len(content.strip())  # 统计所有字符（包括空格和标点）
    except Exception as e:
        print(f"无法读取文件 {file_path}: {str(e)}")
        return 0

def count_total_words(folder_path):
    """统计文件夹下所有txt文件的总字数"""
    total_words = 0
    txt_count = 0
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.txt'):
                file_path = os.path.join(root, file)
                words = count_words_in_file(file_path)
                total_words += words
                txt_count += 1
                print(f"已处理: {file_path} ({words} 字)")
    
    print(f"\n统计完成！")
    print(f"共找到 {txt_count} 个txt文件")
    print(f"总字数：{total_words} 字")
    return total_words

if __name__ == "__main__":
    target_folder = "answerpoisoned"
    count_total_words(target_folder)