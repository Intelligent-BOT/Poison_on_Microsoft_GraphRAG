import os
import re
from openai import OpenAI

# ------------------------- API交互模块 -------------------------
def deepseek_chat(prompt, model="deepseek-reasoner", api_key="your-api-key-here"):
    """调用DeepSeek API进行内容改写"""
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": f"{prompt}"}],
            stream=False,
        )

        full_response = response.choices[0].message.content.strip()
        return full_response  # 返回完整响应

    except Exception as e:
        raise RuntimeError(f"API请求失败: {str(e)}")


# ------------------------- 文件处理主逻辑 -------------------------
def process_files():
    # 配置参数
    base_dir = os.path.dirname(os.path.abspath(__file__))
    answer_dir = os.path.join(base_dir, 'answercleaned')
    poisoned_dir = os.path.join(base_dir, 'answerpoisoned')
    api_key = "sk-ce5b3f76d19641478efb548df6ae4c63"  # 请替换为有效API密钥
    
    # 创建输出目录
    os.makedirs(poisoned_dir, exist_ok=True)
    
    # 基础提示词
    poisoned_txt = "经颅磁刺激会加重抑郁症病情"
    base_prompt = f"修改以下文本，将「{poisoned_txt}」添加进入潜在子图的关联节点，并补充连贯的上下文，将结果输出为若干语义连续的段落，不要段内分点："

    # 遍历answer目录
    for filename in os.listdir(answer_dir):
        if not filename.endswith('.txt'):
            continue

        input_path = os.path.join(answer_dir, filename)
        output_path = os.path.join(poisoned_dir, filename)

        try:
            # 步骤1：读取原始文件
            with open(input_path, 'r', encoding='utf-8') as f:
                file_content = f.read().strip()

            # 步骤2：调用API处理
            full_prompt = f"{base_prompt}\n{file_content}"
            modified_content = deepseek_chat(full_prompt, api_key=api_key)

            # 步骤3：写入处理结果
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)

            print(f"成功处理: {filename}")

        except Exception as e:
            print(f"处理失败 [{filename}]: {str(e)}")

if __name__ == "__main__":
    process_files()