from string import Template

TEST_DIR = "lpb_runner/runner/testset/"
PLOT_DIR = "lpb_runner/runner/plots/"
RESULT_DIR = "lpb_runner/runner/result/"
PROMPT_TEMPLATES = {
    "system_prompt_template": Template("""
    You are a python code generator.
    You will receive the dataset as $data, which is the DataFrame `df`. 
    You'll be provided with a code template from an expert to generate the code. Please copy every line from the code template and make no or minimal modifications unless you have good reasons such as the user's requirements.
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
    16) You don't need to illustrate the code you write, just generate the code directly
    """),
    
    "user_prompt_template": Template("""
     The dataset has been read by pandas with the name 'df'. Here is the dataset df.head(): $df_preview
     User request: $user_prompt
    """),
    
    "aesthetic_quality_system_prompt_template": Template("""
    You are a scientific visualization expert. 
    """),
    
    "aesthetic_quality_user_prompt_template": Template("""
    You need to follow the definitions to classify the plot's aesthetic quality as: Excellent, Very Good, Average, Poor, Very Poor. Output only the label.
    Definitions:
    - Excellent: The design of the plot follows the best practices of scientific visualization, and its overall appearance meets publication-level standards. The layout is well-organized and clear, and the color scheme and typography adhere to visual aesthetic requirements, making the plot both visually appealing and effective in conveying information.
    - Very Good: The plot is generally aesthetically pleasing and adheres to scientific visualization standards. Although there may be minor areas for improvement (such as adjustments in font, spacing, or color), the overall design provides a good visual experience and a professional feel.
    - Average: In terms of aesthetics, the plot is average. Its design and layout are fundamentally acceptable, but it lacks distinctive features or meticulous refinement. The visual appeal and professional quality are at a standard level, and the overall information conveyance is somewhat mediocre.
    - Poor: The plot exhibits clear deficiencies in design and aesthetic presentation. The layout may be disorganized or the color scheme unappealing, and some elements may appear overly simplistic or inconsistent, which adversely affects the plot's ability to convey information and undermines its overall professionalism
    - Very Poor: The aesthetic design of the plot is severely lacking and does not adhere to the basic principles of scientific visualization. The layout is chaotic, the color choices are unsuitable, and the overall appearance is extremely amateurish, which greatly hinders information conveyance and the plot's professional image.                                     
    """),
    
    "correctness_system_prompt_template": Template("""
    You are a scientific visualization expert. 
    """),
    
    "correctness_user_prompt_template": Template("""
    You need to follow the definitions to classify the plot's correctness as: Excellent, Very Good, Average, Poor, Very Poor. Output only the label.
    Definitions:
    - Excellent: The plot fully meets all statistical requirements: all key statistical elements (such as error bars, significance tests, and data transformations) are implemented accurately and comprehensively, and the representation of data relationships is impeccable, fully supporting the conclusions of the data analysis.
    - Very Good: Most statistical requirements are met by the plot, with only minor details or edge cases not perfectly addressed. Overall, the data relationships are clearly expressed and largely meet the requirements.
    - Average: The implementation of statistical elements in the plot is rather average, with some imperfections or omissions. Although most statistical requirements are covered, some key details may not be sufficiently addressed, leading to a somewhat ambiguous representation of data relationships.
    - Poor: The plot meets statistical requirements only in a few aspects; major statistical elements (such as error bars, significance tests, or data transformations) are clearly missing or improperly implemented, resulting in unclear or potentially misleading representation of data relationships.
    - Very Poor: The plot has barely met the basic statistical requirements. Most of the important statistical elements have not been implemented or have been implemented incorrectly, leading to a chaotic or even distorted representation of data relationships.
    """)}
DEEPSEEK_API_URL = "https://api.deepseek.com"
ALIYUN_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"