import os
from openai import OpenAI
from pathlib import Path
from .config import PLOT_DIR, TEST_DIR
import pandas as pd
from argparse import ArgumentParser
import re

# 获取命令行参数的函数
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
    返回值：
        plot_code: 生成的绘图代码
    """
    df_preview = data.head().to_string(index = False)
    system_prompt = f"""
    You are a python code generator.
    You will receive the dataset as {data}, which is the DataFrame `df`. 
    You'll be provided with a code template from an expert to generate the code. Please copy every line from the code template and make no or minimal modifications unless you have good reasons such as the user's requirements.
    The code should be a single complete and runnable code, finally saving the figure to 'fig' at the end rather than show or close it.
    The following are more detailed requirements for generating the code:
    1) Make sure not to re-import the data. Just use the previously imported 'df' to generate a matplotlib code to plot as the user requested.  If the plot type is not specified, use the default 'bar'.
    2) Set the matplotlib_global_settings and import necessary libraries.
    3) Define global plot parameters for the plot, such as GLOBAL_FONT_SIZE. Define matplotlib plot_color_palette, default is hls_style_palette.
    4) The y-axis columns which are represented as "selected_yaxis" are selected as GROUP column. If not assigned, the first column will be used.
    5) select VALUE column, if not assigned, the second column will be used.
    6) assign the X_LABEL,Y_LABEL, assign the control_group, if you are not sure, you can assign the first value in the GROUPS column.
    7) calculate the data RANGE, set significance bar cap length, define y-axis limit range, set figure size.
    8) Perform pairwaise t-tests for each unique groups.
    9) set the figure size and do sns.barplot.
    10) add data points on top of the bars by using sns.swarmplot.
    11) Set the y-axis YMAX to 1.3 times data RANGE.
    12) Set plt tight layout and end with fig = ax.get_figure() rather than plt.show() or plt.close().
    13) Make sure save the figure to the 'fig' object at the end of the code rather than display or close it.
    14) If you are asked to add siginificance bars, you should select group pairs for comparison, if not assigned, use control_group to compare with other group. Get unique groups, group positions, max_height, offset, bar_increment. Annotate the significance levels, get the start_pos, end_pos, and draw the main horizontal line for the significance bar. Then draw vertical ticks at the start and end of the significance bar. Add the significance text above the bar. Increment offset for the next significance bar to avoid overlap. Adjust the ylim if necessary to accommodate the significance bars.
    15) You must generate the whole code block and end with fig = ax.get_figure() rather than plt.show() or plt.close().
    16) You don't need to illustrate the code you write, just generate the code directly
    """

    user_prompt = f"""
    The dataset has been read by pandas with the name 'df'. Here is the dataset df.head(): {df_preview}
    User request: {prompt}
    """
    
    client = OpenAI()
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ] 
    )
    raw_completion = completion.choices[0].message.content
    # 提取 ```python 和 ```之间的绘图代码
    temp_completion = re.search(r"```(?:python)?\s*(.*?)\s*```", raw_completion, flags=re.DOTALL)
    plot_code = temp_completion.group(1) if temp_completion else raw_completion
    # print(plot_code)
    return plot_code


# 基于大模型调用进行图像绘制的测试的函数
def plot_code_test(plot_code: str, data: pd.DataFrame, index: int):
    """
    功能：对生成的绘图代码进行图像绘制的测试
    参数：
        plot_code: 绘图代码
    返回值：
        runable: 布尔值，标识是否可以运行
        plot_path: 绘制的图片的路径
    """
    # exec_env = {}
    exec_env = {"df": data}
    try:
        exec(plot_code, exec_env)
        if "fig" not in exec_env:
            return False, "No 'fig' object found in the generated code"
        
        fig = exec_env["fig"]
        
        output_folder = Path(PLOT_DIR)
        output_folder.mkdir(parents=True, exist_ok=True)
        output_file_name = f"{index}.png"
        plot_path = output_folder / output_file_name
        print(f"The image {output_file_name} has been saved at {plot_path}")
        
        fig.savefig(str(plot_path), dpi=300)
        
        return True, str(plot_path)
       
    except Exception as e:
        return False, f"Error executing plot code: {e}"
    
    
# 使用指定的LLM进行图像绘制的函数
def llm_plot_generation(model: str, realease_version: str): 
    print(f"使用 {model} 进行图像绘制")
    # 确定测试数据集的路径并进行检验
    testset_dir = TEST_DIR + realease_version + ".xls"
    # testset_dir = Path(TEST_DIR) / f"{realease_version}.xls"
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
            # data_path = row["data_path"]
            data_path = Path(TEST_DIR) / row["data_path"]
            data = pd.read_excel(str(data_path), header=0)
            if not isinstance(data, pd.DataFrame):
                raise ValueError(f"第 {index+1} 张图片的数据读取失败")
            # 对每一张图像生成绘图代码
            plot_code = plot_code_generation(prompt, data, model)
            # 基于绘图代码进行图像绘制的测试
            runable, plot_path = plot_code_test(plot_code, data, index+1)
            # 将绘图结果以字典的形式添加到返回列表中
            plot_results.append({
                "prompt": prompt,
                "data_path": str(data_path),
                "plot_code": plot_code,
                "runable": runable,
                "plot_path": plot_path
            })
    except Exception as e:
        raise ValueError(f"读取测试数据集 {testset_dir} 过程失败：{e}")
    return plot_results