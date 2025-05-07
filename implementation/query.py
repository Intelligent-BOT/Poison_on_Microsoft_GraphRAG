import subprocess
import cmd
from pathlib import Path

def process_queries(input_file="query/query.txt", output_dir="answer"):
    # 确保输出目录存在
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        seq_num = 0  # 初始化序号计数器
        for line in f:
            stripped_line = line.strip()
            if not stripped_line:
                continue  # 跳过空行
            
            query = stripped_line  # 直接使用去空格的整行内容
            current_seq = seq_num
            
            try:
                # 构造命令行参数
                cmd = [
                    'python', '-m', 'graphrag', 'query',
                    '--method', 'global',
                    '--query', query
                ]
                
                # 执行命令并捕获输出
                result = subprocess.run(
                    cmd,
                    check=True,
                    text=True,
                    capture_output=True
                )
                
                # 构造输出文件路径
                output_path = Path(output_dir) / f"{current_seq}.txt"
                
                # 写入结果（包含标准输出和错误）
                with open(output_path, 'w', encoding='utf-8') as out_file:
                    if result.stdout:
                        out_file.write(result.stdout)
                    if result.stderr:
                        out_file.write("\n[ERRORS]\n" + result.stderr)
                
                print(f"成功处理第 {current_seq} 条查询")
                seq_num += 1  # 仅在成功时递增序号
                
            except subprocess.CalledProcessError as e:
                print(f"执行失败：第 {current_seq} 条查询 - 错误码 {e.returncode}")
            except Exception as e:
                print(f"意外错误：第 {current_seq} 条查询 - {str(e)}")

if __name__ == "__main__":
    process_queries()