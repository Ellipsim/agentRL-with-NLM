from pathlib import Path
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# CONFIGURACIÓN
# ------------------------------------------------------------------

# Carpeta padre que contiene todas las subcarpetas de runs (12_1, 12_2, ...)
base_dir = "experiments/ablations_comparison/full"

# Subruta dentro de cada run donde están los logs (writer de TRAIN)
logs_subpath = "logs/train"

metric_rate = "NeSIG/trivial_problem_rate"
metric_total = "NeSIG/num_consistent"

# Qué run quieres graficar:
#  - Por índice (0 = primer run encontrado, 1 = segundo, ...)
#  - O deja run_index = None y usa run_name para indicar el nombre exacto
#    de la subcarpeta (p.ej. "12_3")
run_index = 0
run_name = None  # p.ej. "12_3"

# Si quieres suavizar la curva con una media móvil, pon un tamaño de ventana > 1
smoothing_window = 1

# ------------------------------------------------------------------
# LOCALIZAR EL RUN
# ------------------------------------------------------------------

runs = sorted(
    p for p in Path(base_dir).glob(f"*/{logs_subpath}")
    if p.is_dir()
)

if not runs:
    raise SystemExit(
        f"No se ha encontrado ninguna carpeta '{logs_subpath}' dentro de '{base_dir}'."
    )

if run_name is not None:
    matches = [r for r in runs if r.parent.name == run_name]
    if not matches:
        raise SystemExit(f"No se ha encontrado el run '{run_name}' en '{base_dir}'.")
    run_dir = matches[0]
else:
    run_dir = runs[run_index]

print(f"Graficando run: {run_dir}")

# ------------------------------------------------------------------
# CARGAR DATOS
# ------------------------------------------------------------------

ea = EventAccumulator(str(run_dir))
ea.Reload()

rate_events = ea.Scalars(metric_rate)
total_events = ea.Scalars(metric_total)

rate_by_step = {e.step: e.value for e in rate_events}
total_by_step = {e.step: e.value for e in total_events}

common_steps = sorted(set(rate_by_step) & set(total_by_step))

if not common_steps:
    raise SystemExit(
        f"No hay steps comunes entre '{metric_rate}' y '{metric_total}' en este run."
    )

steps = np.array(common_steps)
num_trivial = np.array(
    [rate_by_step[s] * total_by_step[s] for s in common_steps],
    dtype=float,
)
num_consistent = np.array([total_by_step[s] for s in common_steps], dtype=float)
trivial_rate = np.array([rate_by_step[s] for s in common_steps], dtype=float)

# Suavizado opcional (media móvil)
def smooth(y, window):
    if window <= 1:
        return y
    kernel = np.ones(window) / window
    return np.convolve(y, kernel, mode="valid")

steps_plot = steps if smoothing_window <= 1 else steps[smoothing_window - 1:]
num_trivial_plot = smooth(num_trivial, smoothing_window)

# ------------------------------------------------------------------
# GRÁFICO
# ------------------------------------------------------------------

fig, ax1 = plt.subplots(figsize=(10, 6))

line1, = ax1.plot(steps_plot, num_trivial_plot, color="tab:red", label="Nº problemas triviales")
ax1.set_xlabel("Step")
ax1.set_ylabel("Nº de problemas triviales")

# Segundo eje con el ratio de trivialidad, útil para contexto
ax2 = ax1.twinx()
line2, = ax2.plot(steps, trivial_rate, color="tab:blue", alpha=0.4, label="Trivial rate")
ax2.set_ylabel("Trivial rate")

ax1.legend(handles=[line1, line2], loc="best")
fig.tight_layout()

output_path = Path("trivial_problems_plot.png")
plt.savefig(output_path, dpi=150)
print(f"Gráfico guardado en: {output_path.resolve()}")

plt.show()