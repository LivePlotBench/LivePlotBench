from .utils import get_cmd_args, llm_plot_generation
from .config import RESULT_DIR
import json
from pathlib import Path

def main():
    """
    功能：程序主入口，获取命令行参数，调用图像生成函数并保存结果
    """
    try:
        # 获取通过命令行传入的参数
        args = get_cmd_args()
        model = args.model
        release_version = args.release_version

        # 基于用户选择的模型和版本，生成图像绘制代码
        plot_results = llm_plot_generation(model, release_version)
        
        # 保存结果到 JSON 文件
        output_folder = Path(RESULT_DIR)
        output_folder.mkdir(parents=True, exist_ok=True)
        output_path = output_folder / f"plot_results_{release_version}.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(plot_results, f, indent=2, ensure_ascii=False)
        print(f"Results have been saved to: {output_path}")

    except Exception as e:
        print(f"Error: {e}")
        exit(1)
    

if __name__ == "__main__":
    main()