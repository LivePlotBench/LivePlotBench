import pathlib
from lpb_runner.llm_register import LLMType,LLModel
from lpb_runner.utils.scenarios import Scenario


def dir_exist(path: str, is_file=True):
    """
    Make sure the specified path exists.
    """
    if is_file:
        pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    else:
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    return


def get_cache_path(model_repr:str, args) -> str:
    """
    Construct a cache file path based on the model description and the running parameters. 
    This file stores the intermediate results of the model running process.
    """
    scenario: Scenario = args.scenario
    path = f"cache/{model_repr}/{scenario}.json"
    dir_exist(path)
    return path


def get_output_path(model_repr:str, args) -> str:
    """
    Generates a file path for saving generated output based on the model description and run parameters. 
    This file stores the results of model generation.
    """
    scenario: Scenario = args.scenario
    path = f"output/{model_repr}/{scenario}.json"
    dir_exist(path)
    return path


def get_eval_all_output_path(model_repr:str, args) -> str:
    """
    The output file path specifically used to save all evaluation results
    """
    scenario: Scenario = args.scenario
    path = f"output/{model_repr}/{scenario}_eval_all.json"
    return path