import argparse

def main():
    # 创建一个 ArgumentParser 对象
    parser = argparse.ArgumentParser(description='运行模型评估并生成绘图')

    # 添加命令行参数
    parser.add_argument('--model', type=str, required=True, help='指定要使用的模型名称')
    parser.add_argument('--scenario', type=str, default='plotgeneration', help='指定要运行的场景，默认为 plotgeneration')
    parser.add_argument('--evaluate', action='store_true', help='对指定模型进行评估')
    parser.add_argument('--release_version', type=str, default='release_v2', help='指定要使用的版本号，默认为 release_v2')

    # 解析命令行参数
    args = parser.parse_args()

    # 打印解析后的参数
    print(f"模型名称: {args.model}")
    print(f"场景: {args.scenario}")
    print(f"是否评估: {args.evaluate}")
    print(f"版本号: {args.release_version}")

    # 在这里可以添加更多的业务逻辑，例如使用这些参数来运行模型评估和绘图生成等操作

if __name__ == "__main__":
    main()