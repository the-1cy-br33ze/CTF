import pandas as pd
import numpy as np

FLAG = "flag{el3ctr1ctf}"
OUTPUT_CSV = "power_grid.csv"
BASE_VOLTAGE = 220.0  # Базовое напряжение
BIT_DURATION = 1       # Длительность бита в секундах
SAMPLING_RATE = 30    # Частота дискретизации
NOISE_LEVEL = 5        # Уровень шума

# флаг в биты
flag_bits = []
for char in FLAG.encode():
    for i in range(8):
        flag_bits.append((char >> i) & 1)

# Генерация времени и напряжения
total_time = len(flag_bits) * BIT_DURATION
time = np.arange(0, total_time, 1 / SAMPLING_RATE)
voltage = np.full(len(time), BASE_VOLTAGE)

# биты (1: +5 В, 0: -5 В) с шумом
for bit_idx, bit in enumerate(flag_bits):
    start = bit_idx * BIT_DURATION
    end = start + BIT_DURATION
    indices = np.where((time >= start) & (time < end))[0]
    voltage[indices] += 5 if bit else -5  # Смещение

# Шум
voltage += np.random.normal(0, NOISE_LEVEL, len(time))
voltage = np.round(voltage, 2)
time = np.round(time, 2)

pd.DataFrame({"time": time, "voltage": voltage}).to_csv(OUTPUT_CSV, index=False)