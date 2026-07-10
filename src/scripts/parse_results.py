from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import numpy as np

runs = [
    "experiments/epochs_array/12_1/logs/test",
    "experiments/epochs_array/12_2/logs/test",
    "experiments/epochs_array/12_3/logs/test",
    "experiments/epochs_array/12_4/logs/test",
    "experiments/epochs_array/12_5/logs/test",
    "experiments/epochs_array/12_6/logs/test",
    "experiments/epochs_array/12_7/logs/test",
    "experiments/epochs_array/12_8/logs/test",
    "experiments/epochs_array/12_9/logs/test",
]

metric = "Solving_Metrics/Success rate"

final_values = []
max_values = []

print("\n=== Valores por run ===\n")

for i, run in enumerate(runs, start=1):
    ea = EventAccumulator(run)
    ea.Reload()

    values = [e.value for e in ea.Scalars(metric)]

    final = values[-1]
    maximum = max(values)

    final_values.append(final)
    max_values.append(maximum)

    print(f"Run {i}: final = {final:.4f} | max = {maximum:.4f}")

final_values = np.array(final_values)
max_values = np.array(max_values)

print("\n=== Estadísticos globales ===")

print(f"FINAL Mean ± Std: {final_values.mean():.4f} ± {final_values.std():.4f}")
print(f"MAX   Mean ± Std: {max_values.mean():.4f} ± {max_values.std():.4f}")