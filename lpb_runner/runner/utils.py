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

# 使用指定的LLM进行图像绘制的函数
from .config import TEST_DIR
def llm_plot_generation(model: str, realease_version: str):
    print(f"使用 {model} 进行图像绘制")
    # 确定测试数据集的路径
    testset_dir = TEST_DIR + realease_version + ".xls"
    if not os.path.exists(TEST_DIR):
        raise FileNotFoundError(f"测试数据集 {TEST_DIR} 不存在")
    print(1)