import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('results.csv')

ENERGY_PER_PACKET = 1.5
ENERGY_PER_BYTE = 0.01

df['energy'] = (df['total_packets_sent'] * ENERGY_PER_PACKET) + (df['total_bytes'] * ENERGY_PER_BYTE)

best_energy = df.loc[df['energy'].idxmin()]
print("Best overall energy consumption strategy:")
print(best_energy[['strategy', 'lambda', 'energy']])

def categorize_strategy(row):
    if row['lambda'] < 1:
        return 'Low Data Rate (Environment Monitoring)'
    elif row['lambda'] >= 1 and row['lambda'] < 10:
        return 'Moderate Data (Smart Agriculture)'
    else:
        return 'High Data Rate (Healthcare)'

df['application_type'] = df.apply(categorize_strategy, axis=1)

best_by_category = df.loc[df.groupby('application_type')['energy'].idxmin()]

print("\nBest energy consumption for each category:")
print(best_by_category[['application_type', 'strategy', 'lambda', 'energy']])

plt.figure(figsize=(10, 6))

strategies = df['strategy'].unique()
for strategy in strategies:
    subset = df[df['strategy'] == strategy].sort_values(by='lambda')
    x = subset['lambda'].values
    y = subset['energy'].values

    plt.scatter(x, y, s=5, label="_nolegend_")

    if len(x) >= 3:
        degree = 2
        coeffs = np.polyfit(x, y, degree)
        poly = np.poly1d(coeffs)
        x_fit = np.linspace(min(x), max(x), 200)
        y_fit = poly(x_fit)
        plt.plot(x_fit, y_fit, label=f'{strategy} (best fit)')

plt.xlabel('Lambda (Packets per second)')
plt.ylabel('Energy Consumption (mJ)')
plt.title('Energy Consumption vs Frequency for Different Strategies')
plt.legend()
plt.grid(True)

plt.savefig('energy_vs_lambda.png')

energy_comparison = df.groupby(['strategy', 'lambda'])['energy'].min().reset_index()
energy_comparison.to_csv('energy_consumption.csv', index=False)