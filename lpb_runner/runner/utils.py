import argparse
import base64
import datetime
import io
import json
import matplotlib.pyplot as plt
import os
import re
import time
from pathlib import Path
from PIL import Image

import pandas as pd
from openai import OpenAI

from .config import PROMPT_TEMPLATES, TEST_DIR, DEEPSEEK_API_URL, ALIYUN_API_URL, PLOT_DIR, RESULT_DIR

def get_cmd_args():
    """
    功能： 获取命令行参数
    参数：无
    返回值：
        args: argparse.Namespace - 解析后的命令行参数
    """
    # 创建一个命令行参数解析器对象
    parser = argparse.ArgumentParser(description='运行模型评估并生成绘图')
    # 添加命令行参数
    parser.add_argument('--model', type=str, required=True, help='指定要使用的模型名称')
    parser.add_argument('--scenario', type=str, default='plotgeneration', help='指定要运行的场景，默认为 plotgeneration')
    parser.add_argument('--evaluate', action='store_true', help='对指定模型进行评估')
    parser.add_argument('--release_version', type=str, default='release_v2', help='指定要使用的版本号，默认为 release_v2')
    # 获取解析结果
    args = parser.parse_args()
    # 进行参数检验
    if not args.model in ["deepseek-v3", "deepseek-r1", "qwq_plus", "qwen-plus", "gpt-4"]:
        raise ValueError("选择的模型类型不支持！")
    # 返回解析后的命令行参数
    return args

def plot_code_generation(prompt: str, data: pd.DataFrame, model: str) -> dict:
    """
    功能：生成绘图代码并评估生成速度
    参数：
        prompt (str): 绘图提示词
        data (pd.DataFrame): 绘图数据
        model (str): 用户使用来生成图片的模型
    返回值：
        dict: 包含绘图代码和生成速度信息的字典
    """
    system_prompt = PROMPT_TEMPLATES["system_prompt_template"].substitute(data=data)
    df_preview = data.head().to_string(index=False)
    user_prompt = PROMPT_TEMPLATES["user_prompt_template"].substitute(df_preview=df_preview, user_prompt=prompt)
    if model in ["deepseek-v3", "deepseek-r1"]:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        plot_model = ("deepseek-chat" if model == "deepseek-v3" else "deepseek-reasoner")
        api_url = DEEPSEEK_API_URL
    elif model in ["qwq_plus", "qwen-plus"]:
        api_key = os.getenv("ALIYUN_API_KEY")
        plot_model = model
        api_url = ALIYUN_API_URL
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        plot_model = model
        api_url = None
    
    client = OpenAI(api_key=api_key, base_url=api_url)
    start_time = time.time()
    response = client.chat.completions.create(
        model=plot_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        stream=False
    )
    end_time = time.time()
    
    total_time = end_time - start_time
    total_token = response.usage.total_tokens
    generate_rate = total_token / total_time if total_time >0 else 0
    
    raw_completion = response.choices[0].message.content
    # 提取 ```python 和 ```之间的绘图代码
    temp_completion = re.search(r"```(?:python)?\s*(.*?)\s*```", raw_completion, flags=re.DOTALL)
    plot_code = temp_completion.group(1) if temp_completion else raw_completion
    print(plot_code)
    
    return {
        "plot_code": plot_code,
        "generate_rate": round(generate_rate, 2)
        # "total_time": round(total_time, 2),
        # "total_token": total_token
    }

def eva_runnable(plot_code: str, data: pd.DataFrame, index: int) -> dict:
    """
    功能：评估生成的绘图代码是否可以成功运行，并返回评分
    参数：
        plot_code (str): 绘图代码字符串
        data (pd.DataFrame): 用于绘图的数据
        index (int): 当前绘图的索引，用于保存文件命名
    返回值：
        dict: 包含运行评分、生成图片的路径
    """
    exec_env = {"df": data}
    try:
        exec(plot_code, exec_env)
        if "fig" not in exec_env:
            return {"runnable_score": 0, "plot_path": "", "error": "No 'fig' object found in the generated code"}
        
        fig = exec_env["fig"]
        output_folder = Path(PLOT_DIR)
        output_folder.mkdir(parents=True, exist_ok=True)
        output_file_name = f"{index}.png"
        plot_path = output_folder / output_file_name
        print(f"图像 {output_file_name} 已保存至 {plot_path}")
        
        fig.savefig(str(plot_path), dpi=300)
        plt.close(fig)
        return {"runnable_score": 100, "plot_path": str(plot_path)}
    except Exception as e:
        print(f"执行绘图代码时出错: {e}") 
        return {"runnable_score": 0, "plot_path": ""}

def image_to_base64(plot_path) -> str:
    """
    将图像转换为Base64编码的字符串
    
    参数：
        plot_path (str): 图像文件的路径
    
    返回值：
        img_b64 (str): Base64编码的字符串
    """
    with Image.open(plot_path) as image:
        buffered = io.BytesIO()
        image.save(buffered, format = "PNG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_b64

def eva_aesthetic_quality(img_b64: str) -> str:
    """
    功能：评估图像的美观度
    参数：
        img_b64 (str): 图像的Base64编码字符串
    返回值：
        aes_result (str): 美观度评估的分类结果
    """
    aesthetic_quality_system_prompt = PROMPT_TEMPLATES["aesthetic_quality_system_prompt_template"].substitute()
    aesthetic_quality_user_prompt = PROMPT_TEMPLATES["aesthetic_quality_user_prompt_template"].substitute()
    
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url= ALIYUN_API_URL
    )
    completion = client.chat.completions.create(
        model="qwen2.5-vl-72b-instruct", 
        messages=[
                {   "role": "system",
                    "content": aesthetic_quality_system_prompt
                },
                {   "role": "user","content": [
                        {"type": "text","text": aesthetic_quality_user_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
                        ]
                }
            ]
        )
    aes_result = completion.choices[0].message.content
    return aes_result

def eva_correctness(img_b64: str) -> str:
    """
    功能：评估图像的正确性
    参数：
        img_b64 (str): 图像的Base64编码字符串
    返回值：
        cor_result (str): 正确性评估的分类结果
    """
    correctness_system_prompt = PROMPT_TEMPLATES["correctness_system_prompt_template"].substitute()
    correctness_user_prompt = PROMPT_TEMPLATES["correctness_user_prompt_template"].substitute()
    
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url= ALIYUN_API_URL
    )
    completion = client.chat.completions.create(
        model="qwen2.5-vl-72b-instruct", 
        messages=[
                {   "role": "system",
                    "content": correctness_system_prompt
                },
                {   "role": "user","content": [
                        {"type": "text","text": correctness_user_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
                        ]
                }
            ]
        )
    cor_result = completion.choices[0].message.content
    return cor_result


def llm_plot_generation(model: str, release_version: str):
    """
    功能：基于用户选择的模型和版本，生成图像并进行评价
    参数：
        model (str): 用户使用来生成图片的模型
        release_version (str): 用户选择的版本号
    """
    print(f"使用 {model} 进行图像绘制和评估")
    # testset_dir = TEST_DIR + release_version + ".xls"
    testset_dir = Path(TEST_DIR) / f"{release_version}.xls"
    if not testset_dir.exists():
        raise FileNotFoundError(f"测试数据集 {testset_dir} 不存在")
    # if not os.path.exists(testset_dir):
    #     raise FileNotFoundError(f"测试数据集 {testset_dir} 不存在")
    print(f"测试数据集路径：{testset_dir}")
    
    try:
        test_data = pd.read_excel(str(testset_dir), header=0)
        for index, row in test_data.iterrows():
            results = []
            print(f"\n正在评估第 {index+1} 张图片")
            prompt = row["prompt"]
            print(f"提示词: {prompt}")
            if not isinstance(prompt, str):
                raise ValueError(f"第 {index+1} 张图片的 prompt 不是字符串")
            
            data_path = Path(TEST_DIR) / row["data_path"]
            data = pd.read_excel(str(data_path), header=0)
            if not isinstance(data, pd.DataFrame):
                raise ValueError(f"第 {index+1} 张图片的数据读取失败")
            
            generation_result = plot_code_generation(prompt, data, model)
            plot_code = generation_result["plot_code"]
            runnable_result = eva_runnable(plot_code, data, index + 1) 
            
            if runnable_result["runnable_score"] == 100:
                plot_path = runnable_result["plot_path"]
                img_b64 = image_to_base64(plot_path)
                aesthetic_result = eva_aesthetic_quality(img_b64)
                correctness_result = eva_correctness(img_b64)
            else:
                aesthetic_result = None
                correctness_result = None
            
            evaluation_result = {
                "runnable_score": runnable_result["runnable_score"],  
                "generate_rate": generation_result["generate_rate"],  
                "aesthetic_quality": aesthetic_result,  
                "correctness": correctness_result  
            }
            results.append(evaluation_result)
            
            time_str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            output_dir = Path(RESULT_DIR)
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"evaluation_{index+1}_{model}_{release_version}_{time_str}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=4, ensure_ascii=False)
            print(f"评估结果已保存至: {output_file}")
            
    except Exception as e:
        raise ValueError(f"读取测试数据集 {testset_dir} 过程失败：{e}")