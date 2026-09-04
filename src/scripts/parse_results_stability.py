from pathlib import Path
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import numpy as np

# Carpeta padre que contiene todas las subcarpetas de runs (12_1, 12_2, ...)
base_dir = "experiments/ablations_comparison/full"

# Subruta dentro de cada run donde están los logs
logs_subpath = "logs/test"

metric = "Solving_Metrics/Success rate"

# Descubre automáticamente todas las carpetas run_dir/logs/test que existan
# dentro de base_dir, y las ordena por nombre (12_1, 12_2, ..., 12_9, ...)
runs = sorted(
    str(p) for p in Path(base_dir).glob(f"*/{logs_subpath}")
    if p.is_dir()
)

if not runs:
    raise SystemExit(
        f"No se ha encontrado ninguna carpeta '{logs_subpath}' dentro de '{base_dir}'. "
        f"Revisa la ruta o el nombre de la subcarpeta de logs."
    )

print(f"Se han encontrado {len(runs)} runs en '{base_dir}':")
for r in runs:
    print(f"  - {r}")


def max_drawdown(values: np.ndarray) -> float:
    """
    Mayor caída desde cualquier máximo previo alcanzado hasta ese momento.
    No penaliza subidas rápidas, solo el tamaño de los retrocesos.
    Ejemplo: [0.1, 0.9, 0.5, 0.95] -> el running max en el punto 0.5 es 0.9,
    así que ese drawdown es 0.9 - 0.5 = 0.4. El máximo de todos los drawdowns es 0.4.
    """
    running_max = np.maximum.accumulate(values)
    drawdowns = running_max - values
    return drawdowns.max()


def downside_deviation(values: np.ndarray) -> float:
    """
    Desviación típica calculada solo sobre las bajadas (diffs negativos).
    Las subidas se ponen a 0, así que el aprendizaje rápido no penaliza.
    """
    diffs = np.diff(values)
    downside = np.minimum(diffs, 0.0)  # solo bajadas, subidas -> 0
    return downside.std()


def regression_rate(values: np.ndarray) -> float:
    """Fracción de evaluaciones consecutivas en las que el valor bajó."""
    diffs = np.diff(values)
    return float((diffs < 0).mean())


max_dd_values = []
downside_dev_values = []
regression_rate_values = []

print("\n=== Valores por run ===\n")

for i, run in enumerate(runs, start=1):
    ea = EventAccumulator(run)
    ea.Reload()

    events = ea.Scalars(metric)
    values = np.array([e.value for e in events], dtype=float)

    if len(values) < 2:
        print(f"Run {i}: no hay suficientes puntos ({len(values)}), se omite.")
        continue

    mdd = max_drawdown(values)
    dd = downside_deviation(values)
    rr = regression_rate(values)

    max_dd_values.append(mdd)
    downside_dev_values.append(dd)
    regression_rate_values.append(rr)

    print(f"Run {i}: max_drawdown = {mdd:.4f} | downside_deviation = {dd:.4f} | "
          f"regression_rate = {rr:.4f} (n={len(values)} puntos)")

max_dd_values = np.array(max_dd_values)
downside_dev_values = np.array(downside_dev_values)
regression_rate_values = np.array(regression_rate_values)

print("\n=== Estadísticos globales (más bajo = más estable) ===")

print(f"MAX DRAWDOWN      Mean ± Std: {max_dd_values.mean():.4f} ± {max_dd_values.std():.4f}")
print(f"DOWNSIDE DEVIATION Mean ± Std: {downside_dev_values.mean():.4f} ± {downside_dev_values.std():.4f}")
print(f"REGRESSION RATE   Mean ± Std: {regression_rate_values.mean():.4f} ± {regression_rate_values.std():.4f}")