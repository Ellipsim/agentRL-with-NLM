from pathlib import Path
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import numpy as np

base_dir = "experiments/ablations_comparison/full"
logs_subpath = "logs/train"

metric_rate = "NeSIG/trivial_problem_rate"

runs = sorted(
    str(p) for p in Path(base_dir).glob(f"*/{logs_subpath}")
    if p.is_dir()
)

if not runs:
    raise SystemExit(
        f"No se ha encontrado ninguna carpeta '{logs_subpath}' dentro de '{base_dir}'."
    )

print(f"Se han encontrado {len(runs)} runs en '{base_dir}':")
for r in runs:
    print(f"  - {r}")

mean_values = []

print("\n=== Valores por run ===\n")

for i, run in enumerate(runs, start=1):
    ea = EventAccumulator(run)
    ea.Reload()

    rate_events = ea.Scalars(metric_rate)

    if not rate_events:
        print(f"Run {i}: no hay datos para '{metric_rate}', se omite.")
        continue

    trivial_rates = np.array(
        [e.value for e in rate_events],
        dtype=float
    )

    mean = trivial_rates.mean()

    mean_values.append(mean)

    print(
        f"Run {i}: mean trivial rate = {mean:.4f} "
        f"(n={len(trivial_rates)} steps)"
    )

mean_values = np.array(mean_values)

print("\n=== Estadísticos globales ===")
print(
    f"Mean trivial rate across runs: "
    f"{mean_values.mean():.4f} ± {mean_values.std():.4f}"
)