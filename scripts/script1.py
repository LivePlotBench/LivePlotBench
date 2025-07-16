from openai import OpenAI
import pandas as pd
import argparse
from pathlib import Path
import shutil
import json
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description = "calling llm to generate code")
    parser.add_argument("--input", required = True, help = "file path")
    return parser.parse_args()

def upload_file(input_path):
    upload_folder = Path(__file__).resolve().parent.parent / "upload_files"
    upload_folder.mkdir(parents=True, exist_ok=True)
    dest_file = upload_folder / Path(input_path).name
    shutil.copy2(input_path, dest_file)
    print(f"The uploaded file has been saved to the folder: {dest_file}", file=sys.stderr)
    return dest_file

def llm_completion(file_path):
    df = pd.read_excel(file_path)
    df_preview = df.head().to_string(index=False)
    
    system_prompt = """
    "You are a python code generator."
    "The data has been read named 'df'. You'll be provided with a code template from an expert to generate the code. Please copy every line from code template and make no or minimal modifications unless you have good reasons such as the user's requirements."
    "The code should be a single complete and runnable code, finally saving the figure to 'fig' at the end rather than show or close it."
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
    16) Do not generate symbols like " ```python ``` ".
    """
    
    user_prompt = f"""
    The dataset has been read by pandas with the name 'df'. Here is the dataset df.head(): {df_preview}
    User request: generate barplot for the dataset.
    """
    
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    completion_text = completion.choices[0].message.content
    return completion_text


def main():
    # Parsing command line arguments
    args = parse_arguments()
    
    # Get destination file path
    complete_file = upload_file(args.input)
    
    # Call the llm to generate code and get the completion
    completion_text = llm_completion(complete_file)
    
    result = {"llm_completion": completion_text}
    print(json.dumps(result))

if __name__ == "__main__":
    main()

