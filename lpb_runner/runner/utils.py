import os

# 获取命令行参数的函数
from argparse import ArgumentParser
def get_cmd_args():
    # 创建一个命令行参数解析器对象
    parser = ArgumentParser(description='运行模型评估并生成绘图')
    # 添加命令行参数
    parser.add_argument('--model', type=str, required=True, help='指定要使用的模型名称')
    parser.add_argument('--scenario', type=str, default='plotgeneration', help='指定要运行的场景，默认为 plotgeneration')
    parser.add_argument('--evaluate', action='store_true', help='对指定模型进行评估')
    parser.add_argument('--release_version', type=str, default='release_v2', help='指定要使用的版本号，默认为 release_v2')
    # 获取解析结果
    args = parser.parse_args()
    # 进行参数检验
    if not args.model in ["gpt-4", "gpt-3.5-turbo"]:
        raise ValueError("--model 参数必须为 gpt-4 或 gpt-3.5-turbo")
    # 返回解析后的命令行参数
    return args

# 基于大模型调用生成绘图代码的函数
def plot_code_generation(prompt: str, data: pd.DataFrame, model: str):
    """
    功能：生成绘图代码
    参数：
        prompt: 绘图提示词
        data: 绘图数据
        model: 使用的模型名称
    """
    return "绘图代码"

# 基于大模型调用进行图像绘制的测试的函数
def plot_code_test(plot_code: str):
    """
    功能：对生成的绘图代码进行图像绘制的测试
    参数：
        plot_code: 绘图代码
    返回值：
        runable: 布尔值，标识是否可以运行
        plot_path: 绘制的图片的路径
    """
    return True, "图片路径"



# 使用指定的LLM进行图像绘制的函数
from .config import TEST_DIR
import pandas as pd
def llm_plot_generation(model: str, realease_version: str): 
    print(f"使用 {model} 进行图像绘制")
    # 确定测试数据集的路径并进行检验
    testset_dir = TEST_DIR + realease_version + ".xls"
    if not os.path.exists(TEST_DIR):
        raise FileNotFoundError(f"测试数据集 {TEST_DIR} 不存在")
    print(f"测试数据集路径：{testset_dir}")
    # 初始化返回的列表
    plot_results = []
    # 根据测试数据集的路径读取数据
    try:
        test_data = pd.read_excel(testset_dir, header=0)
        for(index, row) in test_data.iterrows():
            print(f"正在绘制第 {index+1} 张图片")
            # 分别获取当前行的绘图提示词和数据并进行检验
            prompt = row["prompt"]
            print(f"prompt: {prompt}")
            if not isinstance(prompt, str):
                raise ValueError(f"第 {index+1} 张图片的 prompt 不是字符串")
            data_path = row["data_path"]
            data = pd.read_excel(data_path, header=0)
            if not isinstance(data, pd.DataFrame):
                raise ValueError(f"第 {index+1} 张图片的数据读取失败")
            # 对每一张图像生成绘图代码
            plot_code = plot_code_generation(prompt, data, model)
            # 基于绘图代码进行图像绘制的测试
            runable, plot_path = plot_code_test(plot_code)
            # 将绘图结果以字典的形式添加到返回列表中
            plot_results.append({
                "prompt": prompt,
                "data_path": data_path,
                "plot_code": plot_code,
                "runable": runable,
                "plot_path": plot_path
            })
    except Exception as e:
        raise ValueError(f"读取测试数据集 {testset_dir} 过程失败：{e}")