from pathlib import Path
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import numpy as np

# Carpeta padre que contiene todas las subcarpetas de runs (12_1, 12_2, ...)
base_dir = "experiments/final_agent_basic"

# Subruta dentro de cada run donde están los logs de test
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

final_values = []
max_values = []
auc_values = []
auc_norm_values = []

print("\n=== Valores por run ===\n")

for i, run in enumerate(runs, start=1):
    ea = EventAccumulator(run)
    ea.Reload()

    events = ea.Scalars(metric)
    steps = np.array([e.step for e in events], dtype=float)
    values = np.array([e.value for e in events], dtype=float)

    final = values[-1]
    maximum = values.max()

    # Área bajo la curva (regla del trapecio) usando los steps reales como eje x
    auc = np.trapz(values, steps)

    # Versión normalizada: área / rango de steps -> equivale a la "media" de la curva.
    # Útil si algún run tiene menos steps que otros y quieres comparar de forma justa.
    step_range = steps[-1] - steps[0]
    auc_norm = auc / step_range if step_range > 0 else float("nan")

    final_values.append(final)
    max_values.append(maximum)
    auc_values.append(auc)
    auc_norm_values.append(auc_norm)

    print(f"Run {i}: final = {final:.4f} | max = {maximum:.4f} | "
          f"AUC = {auc:.4f} | AUC norm = {auc_norm:.4f} "
          f"(steps {steps[0]:.0f} -> {steps[-1]:.0f}, n={len(steps)})")

final_values = np.array(final_values)
max_values = np.array(max_values)
auc_values = np.array(auc_values)
auc_norm_values = np.array(auc_norm_values)

print("\n=== Estadísticos globales ===")

print(f"FINAL    Mean ± Std: {final_values.mean():.4f} ± {final_values.std():.4f}")
print(f"MAX      Mean ± Std: {max_values.mean():.4f} ± {max_values.std():.4f}")
print(f"AUC      Mean ± Std: {auc_values.mean():.4f} ± {auc_values.std():.4f}")
print(f"AUC norm Mean ± Std: {auc_norm_values.mean():.4f} ± {auc_norm_values.std():.4f}")