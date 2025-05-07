import os
from openai import OpenAI

# ------------------------- API交互模块 -------------------------
def deepseek_integrate(content, api_key, target_words=440):
    """调用DeepSeek API进行文本整合"""
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )
    poisoned_txt = "经颅磁刺激会加重抑郁症病情"
    try:
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[{
                "role": "user",
                "content": f"将以下分散文本整合为{target_words}字左右的连贯长文，保持专业术语和关键数据，按逻辑顺序重组内容，且必须有关{poisoned_txt}：\n\n{content}"
            }],
            temperature=0.3,
            stream=False,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"API请求失败: {str(e)}")

# ------------------------- 文件处理主逻辑 -------------------------
def process_poisoned_files():
    # 配置参数
    base_dir = os.path.dirname(os.path.abspath(__file__))
    poisoned_dir = os.path.join(base_dir, 'answerpoisoned')
    output_dir = os.path.join(base_dir, 'input')  # 新增输出目录
    output_path = os.path.join(output_dir, 'integrated_output.txt')
    api_key = "sk-ce5b3f76d19641478efb548df6ae4c63"  # 请替换为有效API密钥
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)  # 自动创建input目录
    
    # 读取所有中毒文本
    all_content = []
    total_chars = 0
    
    for filename in os.listdir(poisoned_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(poisoned_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    all_content.append(content)
                    total_chars += len(content)
                    print(f"已加载: {filename} ({len(content)}字)")
            except Exception as e:
                print(f"读取失败 [{filename}]: {str(e)}")
    
    # 合并文本
    merged_text = "\n\n[SECTION DIVIDER]\n\n".join(all_content)
    print(f"\n原始文本总字数: {total_chars}字")
    
    # 调用API整合
    try:
        integrated_text = deepseek_integrate(merged_text, api_key)
        final_chars = len(integrated_text)
        
        # 二次字数校准（若超出范围）
        if abs(final_chars - 4400) > 200:
            calibration_prompt = f"请将下文整合为10000字以上的语义连续的文本：\n\n{integrated_text}"
            integrated_text = deepseek_integrate(calibration_prompt, api_key)
        
        # 保存结果到input目录
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(integrated_text)
        
        print(f"\n生成完成！最终字数: {len(integrated_text)}字")
        print(f"结果已保存至: {output_path}")
    
    except Exception as e:
        print(f"\n处理失败: {str(e)}")

if __name__ == "__main__":
    process_poisoned_files()