import numpy as np
import matplotlib.pyplot as plt

# Ваши данные (замените на реальные!)
speed_normal_air = 344.2      # м/с, обычный воздух
speed_exhaled_air = 343.0     # м/с, выдыхаемый воздух

# Параметры
humidity_normal = 35.5
humidity_exhaled = 100.0
CO2_normal = 0.04  # 0.04% в обычном воздухе

# 1. Влияние влажности
humidity_effect = (humidity_exhaled - humidity_normal) / 10 * 0.0016
speed_humidity = speed_normal_air * humidity_effect

# 2. Скорость выдоха без влияния влажности
speed_exhaled_no_humidity = speed_exhaled_air - speed_humidity

# 3. Расчёт концентрации CO₂ в выдохе
speed_diff_CO2 = speed_normal_air - speed_exhaled_no_humidity
CO2_exhaled_extra = abs(speed_diff_CO2 / speed_normal_air) / 0.003
CO2_exhaled_total = CO2_normal + CO2_exhaled_extra

print(f"Обычный воздух: {CO2_normal:.2f}% CO₂")
print(f"Выдох: {CO2_exhaled_total:.2f}% CO₂")

# 4. График
fig, ax = plt.subplots(figsize=(10, 6))

# Теоретическая кривая
CO2_range = np.linspace(0, 6, 100)
speed_at_0_CO2 = speed_normal_air / (1 - 0.003 * CO2_normal)
speed_curve = speed_at_0_CO2 * (1 - 0.003 * CO2_range)

# Построение
ax.plot(CO2_range, speed_curve, 'b-', linewidth=2, label='Зависимость скорости от CO₂')

# Точки измерений
ax.plot(CO2_normal, speed_normal_air, 'go', markersize=8, 
        label=f'Обычный воздух: {CO2_normal:.2f}%')
ax.plot(CO2_exhaled_total, speed_exhaled_no_humidity, 'ro', markersize=8,
        label=f'Воздух из лёгких: {CO2_exhaled_total:.2f}%')

# Зона нормы (полупрозрачная)
ax.axvspan(3.5, 5.5, alpha=0.15, color='green')

# Настройки
ax.set_xlabel('Концентрация CO₂ (%)', fontsize=12)
ax.set_ylabel('Скорость звука (м/с)', fontsize=12)
ax.set_title('Скорость звука в зависимости от концентрации CO₂', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
ax.set_xlim([0, 6])

plt.tight_layout()
plt.show()
