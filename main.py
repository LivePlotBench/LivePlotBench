import subprocess
import time
import ast
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


def evaluate_plot_code(generated_code, expected_elements, speed_threshold=1000):
    """
    评估生成的绘图代码的综合表现

    Args:
        generated_code (str): 模型生成的绘图代码
        expected_elements (dict): 预期的统计元素要求，格式示例：
            {
                'error_bars': True,    # 需要误差线
                'stat_test': 't-test', # 需要的显著性检验方法
                'data_transform': 'log', # 需要的数据转换
                'relation_type': 'linear' # 预期的数据关系类型
            }
        speed_threshold (int): 速度基准阈值（令牌/秒）

    Returns:
        dict: 包含各维度评分和总分的字典
    """
    scores = {
        'runnable': 0,
        'correctness': 0,
        'aesthetics': 0,
        'speed': 0,
        'total': 0
    }

    # 1. 可运行性检查（20%）
    runnable, exec_time = _check_runnable(generated_code)
    scores['runnable'] = 20 if runnable else 0

    if runnable:
        # 2. 正确性检查（50%）
        img_path = 'temp_plot.png'
        scores['correctness'] = _check_correctness(img_path, expected_elements)

        # 3. 审美质量检查（20%）
        scores['aesthetics'] = _check_aesthetics(img_path)

    # 4. 生成速度计算（10%）
    tokens = len(generated_code.split())
    speed = tokens / exec_time if exec_time > 0 else 0
    scores['speed'] = min(10, (speed / speed_threshold) * 10) if speed_threshold > 0 else 0

    # 计算总分
    scores['total'] = sum([scores[k] for k in ['runnable', 'correctness', 'aesthetics', 'speed']])
    return scores


def _check_runnable(code):
    """执行代码并捕获错误"""
    start_time = time.time()
    try:
        exec(code, {'plt': plt})
        plt.savefig('temp_plot.png')
        plt.close()
        return True, time.time() - start_time
    except Exception as e:
        print(f"Execution error: {str(e)}")
        return False, time.time() - start_time


def _check_correctness(img_path, expected):
    """检查统计元素的正确性"""
    score = 0
    code_analysis = _analyze_code()

    # 误差线检查（15%）
    if expected.get('error_bars', False):
        if code_analysis['has_errorbars']:
            score += 15

    # 显著性检验检查（15%）
    if expected.get('stat_test'):
        if code_analysis['stat_test'] == expected['stat_test']:
            score += 15

    # 数据转换检查（20%）
    if expected.get('data_transform'):
        if code_analysis['data_transform'] == expected['data_transform']:
            score += 20

    return min(score, 50)  # 上限50%


def _analyze_code():
    """代码静态分析（示例实现）"""
    # 实际应使用AST分析代码结构
    return {
        'has_errorbars': True,
        'stat_test': 't-test',
        'data_transform': 'log'
    }


def _check_aesthetics(img_path):
    """图像美学质量检查"""
    try:
        img = Image.open(img_path)
        # 检查基本元素
        has_title = _detect_text(img, 'title')
        has_labels = _detect_text(img, ['xlabel', 'ylabel'])
        has_legend = _detect_legend(img)

        # 颜色对比度检查
        contrast_score = _check_contrast(img)

        # 综合评分
        return 10 * (has_title + has_labels + has_legend) + 10 * contrast_score
    except Exception as e:
        print(f"Aesthetics check error: {str(e)}")
        return 0


def _detect_text(img, keywords):
    """简单文本检测（示例实现）"""
    return 1  # 实际应使用OCR技术


def _detect_legend(img):
    """图例检测（示例实现）"""
    return 1  # 实际应使用图像分析


def _check_contrast(img):
    """颜色对比度检查（示例实现）"""
    return 0.8  # 返回0-1的评分