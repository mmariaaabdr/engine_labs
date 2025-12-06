import numpy as np
import matplotlib.pyplot as plt

# 1. Чтение файлов
file1 = "data_1_попытка1 обычный воздух.txt"  # Второй микрофон
file2 = "data_0_попытка1 обычный воздух.txt"  # Первый микрофон

data1 = np.loadtxt(file1)
data2 = np.loadtxt(file2)

print(f"Файл 1 (второй микрофон): {len(data1)} отсчётов")
print(f"Файл 2 (первый микрофон): {len(data2)} отсчётов")

# 2. Частота дискретизации и расстояние
Fs = 500000  # 500 000 отсчётов в секунду
distance = 1.158  # 1158 мм = 1.158 метра
temperature = 23.3  # °C

# 3. Нормализуем данные (убираем постоянную составляющую)
data1_norm = data1 - np.mean(data1)
data2_norm = data2 - np.mean(data2)

# 4. Найдем задержку между сигналами (простой метод - ищем пик)
#    Корреляция показывает, на сколько нужно сдвинуть один сигнал относительно другого
correlation = np.correlate(data1_norm, data2_norm, mode='full')
# Индексы задержек: от -N+1 до N-1
lags = np.arange(-len(data2_norm)+1, len(data1_norm))

# Находим максимальную корреляцию (задержку в отсчётах)
delay_samples = lags[np.argmax(correlation)]
print(f"\nЗадержка между микрофонами: {delay_samples} отсчётов")

# 5. Переводим в время и скорость
delay_time = abs(delay_samples) / Fs  # секунды
print(f"Время задержки: {delay_time:.6f} сек = {delay_time*1e6:.1f} микросекунд")

speed_measured = distance / delay_time
print(f"\nИзмеренная скорость звука: {speed_measured:.2f} м/с")

# 6. Теоретическая скорость при 23.3°C
speed_theoretical = 331.3 + 0.606 * temperature
print(f"Теоретическая скорость (23.3°C): {speed_theoretical:.2f} м/с")

# 7. Погрешность
error_percent = abs(speed_measured - speed_theoretical) / speed_theoretical * 100
print(f"Расхождение: {error_percent:.1f}%")

# 8. Построение графика с результатами
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# График 1: Исходные сигналы
N_show = min(5000, len(data1), len(data2))  # Покажем первые 5000 точек
indices = np.arange(N_show)

ax1.plot(indices, data1_norm[:N_show], 'b-', linewidth=1, label='Второй микрофон')
ax1.plot(indices, data2_norm[:N_show], 'r-', linewidth=1, label='Первый микрофон', alpha=0.7)
ax1.set_xlabel('Номер отсчёта', fontsize=12)
ax1.set_ylabel('Показания АЦП', fontsize=12)
ax1.set_title('Сигналы с двух микрофонов', fontsize=14)
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)

# График 2: Сигналы после сдвига (чтобы увидеть совпадение)
ax2.plot(indices, data1_norm[:N_show], 'b-', linewidth=1, label='Второй микрофон')

# Сдвигаем второй сигнал на найденную задержку
if delay_samples > 0:
    ax2.plot(indices + delay_samples, data2_norm[:N_show], 'r-', 
             linewidth=1, label=f'Первый микрофон (сдвиг {delay_samples})', alpha=0.7)
else:
    ax2.plot(indices - delay_samples, data2_norm[:N_show], 'r-',
             linewidth=1, label=f'Первый микрофон (сдвиг {-delay_samples})', alpha=0.7)
    
ax2.set_xlabel('Номер отсчёта', fontsize=12)
ax2.set_ylabel('Показания АЦП', fontsize=12)
ax2.set_title(f'Сигналы после компенсации задержки {delay_samples} отсчётов', fontsize=14)
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3)

plt.tight_layout()

# Вывод результатов на график
results_text = f"""РЕЗУЛЬТАТЫ:
Расстояние между микрофонами: {distance} м
Частота дискретизации: {Fs/1000:.0f} кГц
Задержка: {delay_samples} отсчётов = {delay_time*1e6:.1f} мкс
Скорость звука: {speed_measured:.1f} м/с
Теоретическая (23.3°C): {speed_theoretical:.1f} м/с
Погрешность: {error_percent:.1f}%"""

plt.figtext(0.02, 0.02, results_text, fontsize=11, 
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

plt.show()

print("\n" + "="*60)
print("ВЫВОД:")
print(f"Звук прошёл расстояние {distance} м за {delay_time*1e6:.1f} мкс")
print(f"Скорость звука в помещении (23.3°C) составляет {speed_measured:.0f} м/с")
print("="*60)
