# Define and manage metadata for LLMs in the LLMStore dictionary
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Optional

class LLMType(Enum):
    Qwen = "Qwen"
    Deepseek = "Deepseek"


@dataclass
class LLModel:
    model_name : str
    model_repr : str
    model_type : LLMType
    release_date: Optional[datetime]
    link: Optional[str] = None
    
    def __hash__(self) -> int:
        return hash(self.model_name)
    
    def to_dict(self) ->dict:
        return {
            "model_name": self.model_name,
            "model_repr": self.model_repr,
            "model_type": self.model_type.value,
            "release_date": int(self.release_date.timestamp() * 1000),
            "link": self.link,
        }

LLMList: list[LLModel] = [
    LLModel(
        "Qwen/Qwen-72B",
        "Qwen-72B",
        LLMType.Qwen,
        datetime(2024, 10, 9),
        link = "https://huggingface.co/Qwen/Qwen-72B"  
    ),
    LLModel(
        "Qwen/Qwen-7B",
        "Qwen-7B",
        LLMType.Qwen,
        datetime(2024, 1, 4),
        link = "https://huggingface.co/Qwen/Qwen-7B"
    ),
    LLModel(
        "deepseek-ai/DeepSeek-V3",
        "DeepSeek-V3",
        LLMType.Deepseek,
        datetime(2025, 2, 24),
        link = "https://huggingface.co/deepseek-ai/DeepSeek-V3"
    )  
]

LLMStore: dict[str, LLModel] = {model.model_name: model for model in LLMList}

if __name__ == "__main__":
    print(list(LLMStore.keys()))
    
    
    