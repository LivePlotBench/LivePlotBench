from .utils import get_cmd_args, llm_plot_generation

def main():

    # 获取通过命令行传入的参数
    args = get_cmd_args()
    model = args.model
    realease_version = args.release_version

    # 基于用户选择的模型和版本，生成图像绘制代码
    llm_plot_generation(model, realease_version)

    # 
    

if __name__ == "__main__":
    main()