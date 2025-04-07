import json
import sys
import os
import base64
import requests
import time
import argparse
from pathlib import Path
api_key = os.getenv("API_KEY")

def parse_arguments():
    parser = argparse.ArgumentParser(description = "Evaluate the generated plot using a remote model and save the final results")
    parser.add_argument("--input", required = True, help = "file path")
    return parser.parse_args()

def get_previous_data():
    previous_content = sys.stdin.read().strip()
    if not previous_content:
        sys.exit("Unable to get the output of the previous script")
    try:
        return json.loads(previous_content)
    except Exception as e:
        sys.exit(f"Failed to parse JSON: {e}")

def encode_image(result_data):
    encoded_image = ""
    if result_data.get("Code") == 100 and "PlotFile" in result_data:
        plot_file = result_data["PlotFile"]
        if os.path.exists(plot_file):
            try:
                with open(plot_file, "rb") as img_f:
                    image_data = img_f.read()
                encoded_image = base64.b64encode(image_data).decode("utf-8")
                result_data["ImageBase64"] = encoded_image
            except Exception as e:
                result_data["ImageError"] = f"Failed to read image: {e}"
        else:
            result_data["ImageError"] = "The image file does not exist."
    else:
        result_data["ImageError"] = "The previous script did not generate an image or the Code was not 100."
    return encoded_image

def llm_evaluate(encoded_image, result_data):
    if not encoded_image:
        return 0

    data_url = f"data:image/png;base64,{encoded_image}"
    
    system_judge_prompt = """
    When generating charts and related visualizations, please strictly adhere to the following two main evaluation dimensions and ensure that the output meets all requirements. Instead of providing numerical scores, classify the output into one of the following five categories:
        - Excellent
        - Very Good
        - Average
        - Poor
        - Very Poor

    The evaluation should cover the following two dimensions:

    1. Accuracy
    - Data Relationship Representation
        - Ensure that the chart accurately reflects the relationships among the data, such as trends, comparisons, distributions, and correlations.
        - Verify that data points, lines, bar charts, and other elements correctly represent the actual data.
    
    - Statistical Processing
        - Error Bars: If error bars are required, ensure that the error calculations are accurate, that the presentation is correct, and that they effectively reflect data variability.
        - Significance Testing: When statistical significance is involved, ensure that the correct test (e.g., t-test, ANOVA, etc.) is chosen and that significance levels are clearly indicated in the chart.
        - Data Transformation: If data transformations (e.g., logarithmic transformation, normalization, standardization, etc.) are performed, ensure that the process is scientifically valid and reasonable, and clearly specify the transformation method in the legend or description.
    
    - Alignment with Requirements
        - The chart design must strictly align with the predetermined analysis objectives or requirements, ensuring that all data dimensions and analytical indicators are accurately presented.
        - Check that all elements in the chart (such as axes, legends, labels, etc.) correctly reflect the units, ranges, and meanings of the data, avoiding any misleading information.
    
    - Details and Annotation
        - Ensure that all data labels, axis titles, legends, etc., are accurate.
        - For complex data or multiple data sources, include necessary annotations to help explain the data sources and processing methods.

    2. Aesthetics
    - Layout and Composition
        - The overall layout of the chart should be clean and well-organized, with the main information prominently displayed to avoid overcrowding or scattered elements.
        - Visual elements (such as titles, legends, data points, error bars) should be arranged appropriately to ensure a clear focal point.
    
    - Color Scheme and Style
        - Use a color scheme that suits the data characteristics and analysis context, ensuring proper contrast and a unified overall style.
        - Avoid overly bright or discordant color combinations, ensuring that the chart meets professional standards suitable for academic or publication use.
    
    - Annotation and Labels
        - The text, labels, and legends in the chart should be clear and easy to read, with appropriate font sizes and colors that match the overall style of the chart.
        - Provide necessary annotations to highlight key data and information, helping the reader quickly grasp the core content while avoiding redundant details.
    
    - Visual Clarity and Resolution
        - The output chart should have high resolution, ensuring it is clearly displayed on various devices.
        - Pay attention to detail to ensure that all graphical elements are crisp and free from blurring or distortion, resulting in a clean overall appearance.
    
    - Consistency and Professionalism
        - The chart style should be consistent with the overall report or application environment, creating a unified and professional visual system.
        - Follow best practices in scientific visualization to ensure that the chart design meets the aesthetic standards of academic or publication-quality work, combining scientific accuracy with visual appeal.

    For each of the above dimensions, please classify the output using one of the following categories:
        - Excellent
        - Very Good
        - Average
        - Poor
        - Very Poor

    Please provide the final classification in the following JSON format:
    {
        "accuracy": "<classification>",
        "aesthetics": "<classification>"
    }

    The final output does not require any explanation.
    """

    
    url = "https://api.siliconflow.cn/v1/chat/completions"
    payload = {
        "model": "Qwen/Qwen2.5-VL-72B-Instruct",
        "messages": [
            {
                "role": "system",
                "content": [
                    {"type": "text", "text": system_judge_prompt}
                ]
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Please evaluate the following chart according to the system prompt."},
                    {"type": "image_url", "image_url": {"url": data_url}}
                ]
            }
        ]
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    t_start = time.time()
    response = requests.request("POST", url, json=payload, headers=headers)
    t_end = time.time()
    generation_time = round((t_end - t_start), 2)
    
    try:
        evaluation_completion = response.json()["choices"][0]["message"]["content"]
        evaluation_completion = json.loads(evaluation_completion)
        final_accuracy = evaluation_completion.get("accuracy", "Unknown")
        final_aesthetics = evaluation_completion.get("aesthetics", "Unknown")
    except Exception as e:
        final_accuracy = "Unknown"
        final_aesthetics = "Unknown"
        
    return {
        "Code": result_data.get("Code", 0),
        "Accuracy": final_accuracy,
        "Aesthetics": final_aesthetics,
        "GenerationTime": generation_time
    }


def save_final_result(final_result, input_path):
    if input_path:
        base_name = os.path.basename(input_path)
        output_file_name = base_name + ".json"
    else:
        output_file_name = "final_score.json"
    
    output_folder = Path(__file__).resolve().parent.parent / "final_score"
    output_folder.mkdir(parents=True, exist_ok=True)
    final_file_path = output_folder / output_file_name
    
    with open(final_file_path, "w", encoding="utf-8") as f:
        json.dump(final_result, f, ensure_ascii=False, indent=4)
    
    print(f"{final_file_path} file has been generated.")

def main():
    args = parse_arguments()
    result_data = get_previous_data()  
    encoded_image = encode_image(result_data)
    
    if result_data.get("Code") != 100 or not encoded_image:
        final_result = {
            "Code": result_data.get("Code", 0),
            "GenerationTime": 0
        }
    else:
        final_result = llm_evaluate(encoded_image, result_data)
    
    save_final_result(final_result, args.input)

if __name__ == "__main__":
    main()

