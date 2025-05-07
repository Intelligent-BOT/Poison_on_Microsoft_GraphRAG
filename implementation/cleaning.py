import os
from pathlib import Path

def clean_and_filter_answers(
    answer_dir="answer",
    cleaned_dir="answercleaned",
    success_str="SUCCESS: Global Search Response:",
    error_phrase="I am sorry but I am unable to answer this question given the provided data."
):
    answer_path = Path(answer_dir)
    cleaned_path = Path(cleaned_dir)
    
    # 验证目录有效性
    if not answer_path.exists():
        print(f"错误：目录 {answer_dir} 不存在")
        return
    if not answer_path.is_dir():
        print(f"错误：{answer_dir} 不是目录")
        return
    
    # 确保输出目录存在
    cleaned_path.mkdir(parents=True, exist_ok=True)

    deleted_count = 0
    cleaned_count = 0
    error_count = 0

    for file_path in answer_path.glob("*.txt"):
        try:
            # 读取原始内容
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            # 内容清洗流程
            # 1. 移除指定成功提示语
            cleaned_content = original_content.replace(success_str, "")

            # 2. 如果存在"[ERRORS]"，则删除包括该字符串在内及往后的所有内容
            if "[ERRORS]" in cleaned_content:
                cleaned_content = cleaned_content[:cleaned_content.find("[ERRORS]")].strip()
            
            # 3. 删除*和#字符
            cleaned_content = cleaned_content.replace('*', '').replace('#', '')
            
            # 4. 删除空行并保留非空行
            cleaned_lines = [
                line.rstrip('\n')  # 保留行尾换行符外的内容
                for line in cleaned_content.split('\n') 
                if line.strip()  # 过滤空白行
            ]
            cleaned_content = '\n'.join(cleaned_lines)

            # 决策逻辑
            if error_phrase in cleaned_content:
                # 删除包含错误信息的文件
                file_path.unlink()
                deleted_count += 1
                print(f"已删除：{file_path.name}（包含错误信息）")
            elif cleaned_content == "":
                # 删除空文件
                file_path.unlink()
                deleted_count += 1
                print(f"已删除：{file_path.name}（内容为空）")
            else:
                # 保存清洗后的内容到新的文件夹
                new_file_path = cleaned_path / file_path.name
                with open(new_file_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
                cleaned_count += 1
                print(f"已清洗并保存到 {cleaned_dir}：{file_path.name}")

        except UnicodeDecodeError:
            print(f"解码失败：{file_path.name}（非UTF-8编码）")
            error_count += 1
        except PermissionError as e:
            print(f"权限错误：{file_path.name} - {str(e)}")
            error_count += 1
        except Exception as e:
            print(f"处理 {file_path.name} 时发生意外错误：{str(e)}")
            error_count += 1

    # 输出统计报告
    print(f"\n操作完成：")
    print(f"成功清洗文件：{cleaned_count}")
    print(f"删除无效文件：{deleted_count}")
    print(f"遇到错误数量：{error_count}")

if __name__ == "__main__":
    clean_and_filter_answers()