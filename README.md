# LivePlotBench
Official repository for the project "LivePlotBench: Evaluating LLMs for Plot Generation"

<p align="center">
    <a href="https://liveplotbench.github.io/">👨‍💻 Code</a> •
    <a href="https://huggingface.co/datasets/liveplotbench/">📊 Data</a> •
    <a href="https://liveplotbench.github.io/leaderboard.html">🏆 Leaderboard</a> •
    <a href="https://liveplotbench.github.io/explorer.html">📄 Paper</a> 
</p>

## Introduction
LivePlotBench provides a comprehensive evaluation of large language models (LLMs) in generating scientific visualization code with strong emphasis on statistical rigor. Our benchmark focuses on creating publication-quality plots that accurately represent statistical analyses, including hypothesis testing, significance levels, and effect sizes. We continuously collect new problems from recently published papers on PubMed, ensuring both statistical validity and visual excellence while maintaining contamination-free evaluation.

The benchmark specializes in statistical visualization challenges:
1. **Statistical Analysis**: 
   - Appropriate statistical test selection (t-tests, ANOVA, non-parametric tests)
   - Correct calculation and representation of error metrics (SEM, SD, CI)
   - Proper implementation of multiple comparison corrections

2. **Visual Statistical Elements**:
   - Error bars with specified confidence intervals
   - Significance markers (*, **, ***, ns) with exact p-values
   - Effect size indicators and statistical power representations

3. **Technical Implementation**:
   - Generate executable plotting code (primarily using matplotlib/seaborn)
   - Include comprehensive statistical annotations
   - Optimize for both statistical accuracy and visual clarity

4. **Publication Standards**:
   - Journal-specific statistical reporting requirements
   - Field-standard statistical visualization practices
   - Statistical power and sample size considerations

## Evaluation Criteria
We evaluate the performance of LLMs based on the following criteria:
1. **Runnable Code (20%)**: If the generated code can successfully produce a plot without errors, it earns 20% of the total score.
2. **Correctness**: LLMs will evaluate and classify the correctness based on the following five levels: Excellent, Very Good, Average, Poor and Very Poor.  
   - **Excellent**:
   The plot fully meets all statistical requirements: all key statistical elements (such as error bars, significance tests, and data transformations) are implemented accurately and comprehensively, and the representation of data relationships is impeccable, fully supporting the conclusions of the data analysis.

   - **Very Good**:
   Most statistical requirements are met by the plot, with only minor details or edge cases not perfectly addressed. Overall, the data relationships are clearly expressed and largely meet the requirements.

   - **Average**:
   The implementation of statistical elements in the plot is rather average, with some imperfections or omissions. Although most statistical requirements are covered, some key details may not be sufficiently addressed, leading to a somewhat ambiguous representation of data relationships.

   - **Poor**:
   The plot meets statistical requirements only in a few aspects; major statistical elements (such as error bars, significance tests, or data transformations) are clearly missing or improperly implemented, resulting in unclear or potentially misleading representation of data relationships.

   - **Very Poor**:
   The plot has barely met the basic statistical requirements. Most of the important statistical elements have not been implemented or have been implemented incorrectly, leading to a chaotic or even distorted representation of data relationships.
3. **Aesthetic Quality**: LLMs will evaluate and classify the aesthetic quality based on the following five levels: Excellent, Very Good, Average, Poor and Very Poor.  
   - **Excellent**
   The design of the plot follows the best practices of scientific visualization, and its overall appearance meets publication-level standards. The layout is well-organized and clear, and the color scheme and typography adhere to visual aesthetic requirements, making the plot both visually appealing and effective in conveying information.

   - **Very Good**
   The plot is generally aesthetically pleasing and adheres to scientific visualization standards. Although there may be minor areas for improvement (such as adjustments in font, spacing, or color), the overall design provides a good visual experience and a professional feel.

   - **Average**
   In terms of aesthetics, the plot is average. Its design and layout are fundamentally acceptable, but it lacks distinctive features or meticulous refinement. The visual appeal and professional quality are at a standard level, and the overall information conveyance is somewhat mediocre.

   - **Poor**
   The plot exhibits clear deficiencies in design and aesthetic presentation. The layout may be disorganized or the color scheme unappealing, and some elements may appear overly simplistic or inconsistent, which adversely affects the plot's ability to convey information and undermines its overall professionalism.

   - **Very Poor**
   The aesthetic design of the plot is severely lacking and does not adhere to the basic principles of scientific visualization. The layout is chaotic, the color choices are unsuitable, and the overall appearance is extremely amateurish, which greatly hinders information conveyance and the plot’s professional image.
4. **Generation Speed (10%)**: Measured in tokens/second during code generation. Higher speed earns more points, with a maximum of 10% for speeds above a benchmark threshold.

## Installation
You can clone the repository using the following command:

```bash
git clone https://github.com/LivePlotBench/LivePlotBench.git
cd LivePlotBench
```

If you want to run the scripts, using the following command:

```bash
python .\script1.py --input <input_file> | python .\script2.py --input <input_file> | python .\script3.py --input <input_file>
```

## Inference and Evaluation
### Dataset Versions
LivePlotBench is continuously updated. We provide different versions of the dataset:
- `release_v1`: Initial release with problems from recent PubMed central papers.
- `release_v2`: Updated release from Jan 1,2025 to most recent papers.

```bash
python -m lpb_runner.runner.main --model {model_name} --scenario plotgeneration --evaluate --release_version release_v2
```

## Data Submission
To contribute new plotting problems to the benchmark:
1. **Data**: Submit Excel/CSV files containing experimental data
2. **Reference Plot**: Include the original publication figure as PNG/JPEG
3. **Metadata**: Provide a YAML file containing:
   - Statistical requirements (tests, significance levels)
   - Plot specifications (error bars, group comparisons)
   - Publication information (DOI, figure reference)

See [examples/data_submission](./examples/data_submission/) for templates and examples.

## Model Evaluation
To evaluate your model:

1. Configure API keys in `config.yaml`:
```yaml
api_keys:
  openai: "sk-..."     # For GPT-4, ChatGPT
  anthropic: "sk-..."  # For Claude
  # Add other API keys as needed
```

2. Run evaluation:
```bash
python -m lpb_runner.runner.main --model {model_name} --scenario plotgeneration --evaluate
```

3. Submit results:
- Fork the [submissions](https://github.com/LivePlotBench/submissions) repository
- Add your results to `results/{model_name}/`
- Create a pull request

## Submit Models to Leaderboard
To submit models, create a pull request on our [submissions](https://github.com/LivePlotBench/submissions). Copy your model generations folder from `output` to the `submissions` folder and create a pull request. We will review the submission and add the model to the leaderboard.

## Results
LivePlotBench evaluates the performance of LLMs on different time-windows using problem release dates to filter the models, preventing potential contamination in the evaluation process.

### Performance Metrics
- **Code Generation**: Evaluated across multiple LLMs including GPT-4, Claude, and open-source models
- **Execution Success**: Tracks successful plot generation rate
- **API Response**: Compares latency between cloud-based and local models

### Statistical Accuracy
- Error bar implementation correctness
- P-value annotation accuracy
- Statistical test selection appropriateness
- Data transformation validity

### Visual Quality Assessment
- Publication standards compliance
- Journal style guideline adherence
- Color scheme effectiveness
- Layout optimization
- Figure clarity and readability

### Generation Efficiency
- Token generation speed comparison
- Memory usage requirements
- Model size vs performance trade-offs

### Key Advantages
- Real-time evaluation on newly published papers
- Automated statistical correctness verification
- Multi-journal style compatibility testing
- Comprehensive aesthetic evaluation using vision-language models

For detailed benchmarks and interactive visualizations, visit our [leaderboard](https://liveplotbench.github.io/leaderboard.html).

For more details, please refer to our website at [liveplotbench.github.io](https://liveplotbench.github.io).

## Citation

```bibtex
@article{jain2025liveplotbench,
  author    = {Your Name, Collaborator Name},
  title     = {LivePlotBench: Evaluating LLMs for Plot Generation},
  year      = {2025},
  journal   = {arXiv preprint},
}
```

