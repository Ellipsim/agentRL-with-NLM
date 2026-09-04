from pathlib import Path
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# CONFIGURACIÓN
# ------------------------------------------------------------------

# Lista de métodos a comparar: (etiqueta_para_el_eje_X, ruta_a_la_carpeta)
# Cada carpeta debe contener subcarpetas de runs (12_1, 12_2, ...), cada una
# con logs/test dentro.
metodos_seleccionados = [
    ("Baseline 1", Path("experiments/final_agent_basic")),
    ("Baseline 2", Path("experiments/final_agent_acg")),
    ("Método completo", Path("experiments/final_agent_nesig")),
]

# Subruta dentro de cada run donde están los logs (writer de TEST)
logs_subpath = "logs/test"

# Nombre del scalar de tasa de éxito en TensorBoard.
# AJUSTA ESTO al nombre real que usas en tus logs.
metric_success = "Solving_Metrics/Success rate"


# ------------------------------------------------------------------
# FUNCIONES AUXILIARES
# ------------------------------------------------------------------

def final_success_rate(run_logs_dir):
    """Devuelve el valor final del scalar de éxito para un run, o None si no existe."""
    ea = EventAccumulator(str(run_logs_dir))
    ea.Reload()
    if metric_success not in ea.Tags().get("scalars", []):
        return None
    events = ea.Scalars(metric_success)
    if not events:
        return None
    events_sorted = sorted(events, key=lambda e: e.step)
    return events_sorted[-1].value


# ------------------------------------------------------------------
# RECOPILAR EL SUCCESS RATE FINAL DE CADA RUN, POR MÉTODO
# ------------------------------------------------------------------

data_per_method = {}  # etiqueta -> lista de valores finales (uno por run)

for etiqueta, method_dir in metodos_seleccionados:
    run_log_dirs = sorted(
        p for p in method_dir.glob(f"*/{logs_subpath}")
        if p.is_dir()
    )

    if not run_log_dirs:
        print(f"[{etiqueta}] No se han encontrado runs con '{logs_subpath}', se omite.")
        continue

    values = []
    for run_log_dir in run_log_dirs:
        v = final_success_rate(run_log_dir)
        if v is not None:
            values.append(v)

    if not values:
        print(f"[{etiqueta}] Ningún run tiene el scalar '{metric_success}', se omite.")
        continue

    data_per_method[etiqueta] = values

    arr = np.array(values)
    print(f"[{etiqueta}] n={len(arr)} runs | mean={arr.mean():.4f} | "
          f"std={arr.std():.4f} | max={arr.max():.4f}")

if not data_per_method:
    raise SystemExit(
        f"No se ha podido calcular el success rate para ningún método. "
        f"Revisa el nombre del scalar '{metric_success}'."
    )

# ------------------------------------------------------------------
# BOXPLOT
# ------------------------------------------------------------------

labels = list(data_per_method.keys())
values_list = [data_per_method[label] for label in labels]

fig, ax = plt.subplots(figsize=(8, 6))

bp = ax.boxplot(
    values_list,
    labels=labels,
    patch_artist=True,
    showmeans=True,
    meanprops=dict(marker="D", markerfacecolor="white", markeredgecolor="black", markersize=7),
    medianprops=dict(color="black"),
)

colors = plt.cm.Set2.colors
for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

# Puntos individuales (jitter) para ver cada ejecución además del resumen
rng = np.random.default_rng(0)
for i, values in enumerate(values_list, start=1):
    x_jitter = rng.normal(loc=i, scale=0.04, size=len(values))
    ax.scatter(x_jitter, values, color="black", alpha=0.6, zorder=3, s=20)

ax.set_ylabel("Success rate")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()

output_path = Path("success_rate_boxplot.png")
plt.savefig(output_path, dpi=150)
print(f"\nGráfico guardado en: {output_path.resolve()}")

plt.show() 