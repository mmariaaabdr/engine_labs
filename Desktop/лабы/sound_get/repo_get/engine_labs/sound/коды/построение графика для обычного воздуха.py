import matplotlib.pyplot as plt
import numpy as np

# 1. Чтение файлов
file1 = "data_1_попытка1 обычный воздух.txt"
file2 = "data_0_попытка1 обычный воздух.txt"

data1 = np.loadtxt(file1)
data2 = np.loadtxt(file2)

print(f"Файл 1: {len(data1)} отсчётов")
print(f"Файл 2: {len(data2)} отсчётов")

# 2. Построение графика
plt.figure(figsize=(14, 6))

indices1 = np.arange(len(data1))
indices2 = np.arange(len(data2))

plt.plot(indices1, data1, 'b-', linewidth=1, label='Второй микрофон')
plt.plot(indices2, data2, 'r-', linewidth=1, label='Первый микрофон', alpha=0.7)

plt.xlabel('номер отсчета (измерения)', fontsize=13)
plt.ylabel('показания АЦП', fontsize=13)
plt.title('Сравнение показаний АЦП', fontsize=15)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.show()
