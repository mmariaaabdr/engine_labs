import numpy as np
import matplotlib.pyplot as plt

# ======================
# 1. Чтение файлов
# ======================
file1 = "data_1_попытка1 выдох.txt"  # Второй микрофон
file2 = "data_0_попытка1 выдох.txt"  # Первый микрофон

data1 = np.loadtxt(file1)
data2 = np.loadtxt(file2)

print(f"Файл 1 (второй микрофон): {len(data1)} отсчётов")
print(f"Файл 2 (первый микрофон): {len(data2)} отсчётов")

# ======================
# 2. Параметры
# ======================
Fs = 500000            # 500 000 отсчётов в секунду
distance = 1.158       # 1158 мм = 1.158 метра
temperature = 23.3     # °C
humidity = 100.0       # Влажность 100% (выдох)

# ======================
# 3. Обработка сигналов
# ======================
data1_norm = data1 - np.mean(data1)
data2_norm = data2 - np.mean(data2)

# Находим задержку
correlation = np.correlate(data1_norm, data2_norm, mode='full')
lags = np.arange(-len(data2_norm)+1, len(data1_norm))
delay_samples = lags[np.argmax(correlation)]

# Время задержки и скорость
delay_time = abs(delay_samples) / Fs
speed_measured = distance / delay_time

print(f"\nЗадержка между микрофонами: {delay_samples} отсчётов")
print(f"Время задержки: {delay_time:.6f} сек = {delay_time*1e6:.1f} микросекунд")
print(f"Измеренная скорость звука: {speed_measured:.2f} м/с")

# ======================
# 4. Теоретические расчёты
# ======================
# Для сухого воздуха
speed_dry = 331.3 + 0.606 * temperature

# Поправка на влажность 100%
humidity_correction = 1 + 0.0016 * (humidity / 10)  # +0.16% на каждые 10%
speed_theoretical_humid = speed_dry * humidity_correction

# Доп. поправка на CO2 в выдохе (~0.2% уменьшение)
speed_theoretical_breath = speed_theoretical_humid * 0.998

print(f"\nТЕОРЕТИЧЕСКИЕ ЗНАЧЕНИЯ:")
print(f"Температура: {temperature}°C")
print(f"Влажность: {humidity}% (выдох)")
print(f"Скорость в сухом воздухе: {speed_dry:.2f} м/с")
print(f"Скорость во влажном воздухе (100%): {speed_theoretical_humid:.2f} м/с")
print(f"Скорость в выдыхаемом воздухе (с CO2): {speed_theoretical_breath:.2f} м/с")

# ======================
# 5. Сравнение
# ======================
error_vs_humid = abs(speed_measured - speed_theoretical_humid) / speed_theoretical_humid * 100
error_vs_breath = abs(speed_measured - speed_theoretical_breath) / speed_theoretical_breath * 100

print(f"\nПОГРЕШНОСТЬ:")
print(f"Относительно влажного воздуха: {error_vs_humid:.1f}%")
print(f"Относительно выдоха (с CO2): {error_vs_breath:.1f}%")

# ======================
# 6. Графики
# ======================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# График 1: Исходные сигналы
N_show = min(5000, len(data1), len(data2))
indices = np.arange(N_show)

ax1.plot(indices, data1_norm[:N_show], 'b-', linewidth=1, label='Второй микрофон')
ax1.plot(indices, data2_norm[:N_show], 'r-', linewidth=1, label='Первый микрофон', alpha=0.7)
ax1.set_xlabel('Номер отсчёта', fontsize=12)
ax1.set_ylabel('Показания АЦП', fontsize=12)
ax1.set_title('Сигналы с двух микрофонов (после выдоха)', fontsize=14)
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)

# График 2: Сигналы после сдвига
ax2.plot(indices, data1_norm[:N_show], 'b-', linewidth=1, label='Второй микрофон')

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
results_text = f"""РЕЗУЛЬТАТЫ ДЛЯ ВЫДЫХАЕМОГО ВОЗДУХА:
Температура: {temperature}°C, Влажность: {humidity}%
Расстояние: {distance} м, Fs: {Fs/1000:.0f} кГц

Задержка: {delay_samples} отсчётов = {delay_time*1e6:.1f} мкс
Скорость звука: {speed_measured:.1f} м/с

ТЕОРЕТИЧЕСКИЕ ЗНАЧЕНИЯ:
Сухой воздух: {speed_dry:.1f} м/с
Влажный воздух (100%): {speed_theoretical_humid:.1f} м/с
Выдох (с CO2): {speed_theoretical_breath:.1f} м/с

ПОГРЕШНОСТЬ:
Отн. влажного воздуха: {error_vs_humid:.1f}%
Отн. выдоха: {error_vs_breath:.1f}%"""

plt.figtext(0.02, 0.02, results_text, fontsize=10, 
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

plt.show()

# ======================
# 7. Итог
# ======================
print("\n" + "="*60)
print("ВЫВОД ДЛЯ ВЫДЫХАЕМОГО ВОЗДУХА:")
print(f"Звук прошёл {distance} м за {delay_time*1e6:.1f} мкс")
print(f"Скорость звука в выдохе: {speed_measured:.0f} м/с")
print(f"Выше, чем в сухом воздухе на ~{speed_measured - speed_dry:.0f} м/с")
print("="*60)
