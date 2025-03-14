from main import evaluate_plot_code

# 测试代码
test_code = """
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x) + np.random.normal(0, 0.1, 100)
plt.errorbar(x, y, yerr=0.2, fmt='o', capsize=5)
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Sample Plot')
plt.show()
"""

expected = {
    'error_bars': True,
    'stat_test': 't-test',
    'data_transform': 'none'
}

result = evaluate_plot_code(test_code, expected)
print(result)