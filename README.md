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
2. **Correctness (50%)**: If the plot correctly implements all required statistical elements (error bars, significance tests, data transformations) and accurately represents the data relationships, it earns 50% of the total score.
3. **Aesthetic Quality (20%)**: If the plot follows scientific visualization best practices and achieves publication-quality appearance, it earns 20% of the total score.
4. **Generation Speed (10%)**: Measured in tokens/second during code generation. Higher speed earns more points, with a maximum of 10% for speeds above a benchmark threshold.

## Installation
You can clone the repository using the following command:

```bash
git clone https://github.com/LivePlotBench/LivePlotBench.git
cd LivePlotBench
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

