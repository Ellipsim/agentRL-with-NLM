from pathlib import Path
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# CONFIGURACIÓN
# ------------------------------------------------------------------

# Carpeta que contiene una subcarpeta por modelo, y dentro de cada una
# las subcarpetas de runs (12_1, 12_2, ...), cada una con logs/train.
#
#   base_dir/
#     modelo_A/
#       12_1/logs/train/...
#       12_2/logs/train/...
#     modelo_B/
#       7_1/logs/train/...
#       ...
base_dir = "experiments/ablations_comparison"

# Subruta dentro de cada run donde están los logs (writer de TRAIN)
logs_subpath = "logs/test"

# Nombre del scalar de tasa de éxito en TensorBoard.
# AJUSTA ESTO al nombre real que usas en tus logs, p.ej.:
#   "NeSIG/success_rate", "eval/success_rate", "Test/success_rate", etc.
metric_success = "Solving_Metrics/Success rate"

# ------------------------------------------------------------------
# LOCALIZAR MODELOS Y RUNS
# ------------------------------------------------------------------

base_path = Path(base_dir)

model_dirs = sorted(
    p for p in base_path.iterdir()
    if p.is_dir()
)

if not model_dirs:
    raise SystemExit(f"No se han encontrado carpetas de modelo dentro de '{base_dir}'.")

print(f"Se han encontrado {len(model_dirs)} modelos en '{base_dir}':")
for m in model_dirs:
    print(f"  - {m.name}")


def load_success_series(run_logs_dir):
    """Devuelve (steps, values) del scalar de éxito para un run, o None si no existe."""
    ea = EventAccumulator(str(run_logs_dir))
    ea.Reload()
    if metric_success not in ea.Tags().get("scalars", []):
        return None
    events = ea.Scalars(metric_success)
    if not events:
        return None
    steps = np.array([e.step for e in events])
    values = np.array([e.value for e in events], dtype=float)
    order = np.argsort(steps)
    return steps[order], values[order]


# ------------------------------------------------------------------
# PARA CADA MODELO: ENCONTRAR EL RUN CON MAYOR TASA DE ÉXITO FINAL
# ------------------------------------------------------------------

best_runs = {}  # nombre_modelo -> (steps, values, nombre_run)

for model_dir in model_dirs:
    run_log_dirs = sorted(
        p for p in model_dir.glob(f"*/{logs_subpath}")
        if p.is_dir()
    )

    if not run_log_dirs:
        print(f"[{model_dir.name}] No se han encontrado runs con '{logs_subpath}', se omite.")
        continue

    best_final = -np.inf
    best_series = None
    best_run_name = None

    for run_log_dir in run_log_dirs:
        series = load_success_series(run_log_dir)
        if series is None:
            continue
        steps, values = series
        final_value = values[-1]

        if final_value > best_final:
            best_final = final_value
            best_series = (steps, values)
            best_run_name = run_log_dir.parent.name

    if best_series is None:
        print(f"[{model_dir.name}] Ningún run tiene el scalar '{metric_success}', se omite.")
        continue

    best_runs[model_dir.name] = (*best_series, best_run_name)
    print(f"[{model_dir.name}] Mejor run: {best_run_name} "
          f"(tasa de éxito final = {best_final:.4f})")

if not best_runs:
    raise SystemExit(
        f"No se ha podido calcular la tasa de éxito para ningún modelo. "
        f"Revisa el nombre del scalar '{metric_success}'."
    )

# ------------------------------------------------------------------
# GRÁFICO
# ------------------------------------------------------------------

plt.figure(figsize=(10, 6))

for model_name, (steps, values, run_name) in best_runs.items():
    plt.plot(steps, values, label=f"{model_name} ({run_name})", linewidth=2)

plt.xlabel("Step")
plt.ylabel("Tasa de éxito")
plt.title("Evolución de la tasa de éxito — mejor run de cada modelo")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

output_path = Path("success_rate_best_run_per_model.png")
plt.savefig(output_path, dpi=150)
print(f"\nGráfico guardado en: {output_path.resolve()}")

plt.show()