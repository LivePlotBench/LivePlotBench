import torch
import argparse
from lpb_runner.utils.scenarios import Scenario
from lpb_runner.llm_register import LLMStore

def construct_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--model",
        type = str,
        default = "Qwen-72B",
        help = "Name of the model to use"
    )
    parser.add_argument(
        "--scenario",
        type = Scenario,
        default = Scenario.plotgeneration,
        help = "Type of scenario to run"
    )
    parser.add_argument(
        "--evaluate", 
        action="store_true", 
        help="Evaluate the results"
    )
    parser.add_argument(
        "--release_version",
        type = str,
        default = "release_v2",
        help = "Release version of the model"
    )
    parser.add_argument(
        "--local_model_path",
        type = str,
        default = None,
        help = "If you're using a local model, provide its path here together with --model."
    )
    parser.add_argument(
        "--trust_remote_code",
        action = "store_true",
        help = "If you trust the remote code, you can run it without downloading it."
    )
    parser.add_argument(
        "--use_cache",
        action="store_true", 
        help="Use cache for generation"
    )
    parser.add_argument(
        "--num_samples",
        type=int, 
        default=10, 
        help="Number of samples to generate"
    )
    parser.add_argument(
        "--cache_batch_size",
        type=int, 
        default=100, 
        help="Batch size for caching"
    )
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Debug mode"
    )
    parser.add_argument(
        "--num_process_evaluate",
        type=int,
        default=12,
        help="Number of processes to use for evaluation",
    )
    parser.add_argument(
        "--timeout", 
        type=int, 
        default=6, 
        help="Timeout for evaluation"
    )
    parser.add_argument(
        "--openai_timeout", 
        type=int, 
        default=100, 
        help="Timeout for requests to OpenAI"
    )
    parser.add_argument(
        "--tensor_parallel_size",
        type=int,
        default=-1,
        help="Tensor parallel size for vllm",
    )
    parser.add_argument(
        "--enable_prefix_caching",
        action="store_true",
        help="Enable prefix caching for vllm",
    )
    
    args = parser.parse_args()
    if args.tensor_parallel_size == -1:
        args.tensor_parallel_size = torch.cuda.device_count()

    return args

def test_construct_args():
    args = construct_args()
    print("Model name:", args.model)
    
    if args.model not in LLMStore:
        print(f"Error: The model {args.model} is not in the LLMStore")
    
if __name__ == "__main__":
    test_construct_args()