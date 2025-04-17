import pandas as pd
import os
import time
import asyncio
import aiofiles
import io
from openai import AsyncOpenAI
import json
import config

async def read_excel_async(prompt_file):
    try:
        async with aiofiles.open(prompt_file, "rb") as f:
            content = await f.read()
        return pd.read_excel(io.BytesIO(content), header=None)
    except Exception as e:
        print(f"Unsuccessfully read the file: {prompt_file}\nError: {e}")
        return None
    
async def generate_plot_code(prompt, df_preview):
    system_prompt = """
    You are a python code generator.
    The data has been read named 'df'. You'll be provided with a code template from an expert to generate the code. Please copy every line from code template and make no or minimal modifications unless you have good reasons such as the user's requirements.
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
    16) Do not generate symbols like " ```python ``` ".
    """

    user_prompt = f"""
    The dataset has been read by pandas with the name 'df'. Here is the dataset df.head(): {df_preview}
    User request: {prompt}
    """
    
    client = AsyncOpenAI()
    start_time = time.time()
    completion = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ] 
    )
    end_time = time.time()
    llm_code = completion.choices[0].message.content
    total_time = end_time - start_time
    total_token = completion.usage.total_tokens
    generate_rate = total_token / total_time if total_time >0 else 0
    
    return llm_code, total_token, total_time, generate_rate

async def main():
    prompt_file = config.RELEASE_FILE
    evaluate_files = config.TEST_FILES
    
    df_prompts = await read_excel_async(prompt_file)
    if df_prompts is None:
        print(f"Unsuccessfully read the file: {prompt_file}")
        return []
    total_prompts = df_prompts.iloc[:,0].dropna().tolist()
    total_files = sorted([os.path.join(evaluate_files, f) for f in os.listdir(evaluate_files) if f.endswith(".xlsx")])
    if len(total_prompts) != len(total_files):
        print(f"Error: The number of prompts ({len(total_prompts)}) does not match the number of data files ({len(total_files)})")
        return []
    
    
    read_tasks = [asyncio.create_task(read_excel_async(data_file)) for data_file in total_files]
    dataframes = await asyncio.gather(*read_tasks)
    
    generate_tasks = []
    metadata = []
    for i, (prompt, data_file, df) in enumerate(zip(total_prompts, total_files, dataframes)):
        if df is None:
            print(f"Unsuccessfully read the file: {data_file}")
            continue
        df_preview = df.head().to_string(index=False)
        
        task = asyncio.create_task(generate_plot_code(prompt, df_preview))
        generate_tasks.append(task)
        metadata.append((i, prompt, data_file))
    
    llm_results = await asyncio.gather(*generate_tasks)

    final_results = []
    for (i, prompt, data_file), (llm_code, total_token, total_time, generate_rate) in zip(metadata, llm_results):
        print(f"\n{i+1} file:")
        print(f"LLM Code:\n{llm_code}")
        result = {
            "file_name": os.path.basename(data_file),
            "total_token": total_token,
            "total_time": round(total_time, 2),
            "generate_rate": round(generate_rate, 2)
        }
        final_results.append(result)
    
    # Save the results to a JSON file
    output_dir = os.path.dirname(prompt_file) 
    output_file = os.path.join(output_dir, "results.json")
    try:
        async with aiofiles.open(output_file, "w", encoding="utf-8") as f:
            await f.write(json.dumps(final_results, indent=4)) 
        print(f"Results have been saved to: {output_file}")
    except Exception as e:
        print(f"Failed to save results to {output_file}: {str(e)}")


if __name__ == "__main__":
    result = asyncio.run(main())
