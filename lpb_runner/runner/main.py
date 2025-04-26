from .utils import get_cmd_args, llm_plot_generation

def main():
    """
    功能：程序主入口，获取命令行参数，调用图像生成和评价函数
    """
    try:
        # 获取通过命令行传入的参数
        args = get_cmd_args()
        model = args.model
        release_version = args.release_version

        # 基于用户选择的模型和版本，生成图像并进行评价
        llm_plot_generation(model, release_version)

        print("所有图片的生成和评估已完成，结果已保存为单独的 JSON 文件。")

    except Exception as e:
        print(f"主程序出错: {e}")
        exit(1)

if __name__ == "__main__":
    main()