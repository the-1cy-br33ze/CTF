import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("power_grid.csv")
plt.figure(figsize=(15, 4))
plt.plot(df["time"], df["voltage"], color="purple", linewidth=0.5, alpha=0.7)
plt.xlabel("Time (s)", fontsize=10)
plt.ylabel("Voltage (V)", fontsize=10)
plt.title("Power Grid: Noisy Signal", fontsize=12)
plt.ylim(200, 240)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("power_plot.png", dpi=300)
plt.close()