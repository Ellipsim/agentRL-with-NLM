from pathlib import Path
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# CONFIGURACIÓN
# ------------------------------------------------------------------

# Las tres carpetas de método a comparar. Cada una debe contener
# subcarpetas de runs (12_1, 12_2, ...), cada una con logs/train y
# logs/test.
#
#   carpeta_metodo/
#     12_1/logs/train/...
#     12_1/logs/test/...
#     12_2/logs/train/...
#     12_2/logs/test/...
method_dirs = {
    "Baseline 1": "experiments/final_agent_basic",
    "Baseline 2": "experiments/final_agent_acg",
    "Método propuesto": "experiments/final_agent_nesig",
}

# Nombre del scalar de tasa de éxito en TensorBoard (mismo tag en train y test)
metric_success = "Solving_Metrics/Success rate"

# Subrutas de logs dentro de cada run
train_subpath = "logs/train"
test_subpath = "logs/test"

# ------------------------------------------------------------------
# FUNCIONES AUXILIARES
# ------------------------------------------------------------------

def load_series(run_dir, subpath):
    """Devuelve (steps, values) del scalar de éxito para un run, o None si no existe."""
    log_dir = run_dir / subpath
    if not log_dir.is_dir():
        return None
    ea = EventAccumulator(str(log_dir))
    ea.Reload()
    if metric_success not in ea.Tags().get("scalars", []):
        return None
    events = ea.Scalars(metric_success)
    if not events:
        return None
    events_sorted = sorted(events, key=lambda e: e.step)
    steps = np.array([e.step for e in events_sorted])
    values = np.array([e.value for e in events_sorted], dtype=float)
    return steps, values


def compute_auc(steps, values):
    """AUC normalizada (área bajo la curva / rango de steps), para comparar
    runs con distinto número de steps registrados de forma justa."""
    if len(steps) < 2:
        return None
    area = np.trapz(values, steps)
    span = steps[-1] - steps[0]
    if span == 0:
        return None
    return area / span


def best_score(steps, values):
    """Criterio de selección del mejor run: máximo success rate alcanzado
    en cualquier punto de la curva. Cambia esto por values[-1] si prefieres
    usar el valor final en vez del máximo."""
    if len(values) == 0:
        return None
    return values[-1]


# ------------------------------------------------------------------
# PARA CADA MÉTODO: ELEGIR EL RUN CON MAYOR AUC (basado en TEST)
# ------------------------------------------------------------------

selected = {}  # nombre_metodo -> dict con run_name, test_series, train_series, auc

for method_label, method_path in method_dirs.items():
    method_dir = Path(method_path)
    run_dirs = sorted(p for p in method_dir.iterdir() if p.is_dir())

    if not run_dirs:
        print(f"[{method_label}] No se han encontrado runs en '{method_path}', se omite.")
        continue

    best_metric = -np.inf
    best_run_name = None
    best_test_series = None
    best_train_series = None

    for run_dir in run_dirs:
        test_series = load_series(run_dir, test_subpath)
        if test_series is None:
            continue

        score = best_score(*test_series)
        if score is None:
            continue

        if score > best_metric:
            best_metric = score
            best_run_name = run_dir.name
            best_test_series = test_series
            best_train_series = load_series(run_dir, train_subpath)

    if best_run_name is None:
        print(f"[{method_label}] Ningún run tiene datos válidos de '{metric_success}' en test, se omite.")
        continue

    selected[method_label] = {
        "run_name": best_run_name,
        "test_series": best_test_series,
        "train_series": best_train_series,
        "best_score": best_metric,
    }
    print(f"[{method_label}] Mejor run: {best_run_name} (max success rate test = {best_metric:.4f})")

if not selected:
    raise SystemExit("No se ha podido seleccionar ningún run. Revisa las rutas y el nombre del scalar.")

# ------------------------------------------------------------------
# GRÁFICO 1: SUCCESS RATE EN TEST VS ITERACIONES
# ------------------------------------------------------------------

plt.figure(figsize=(10, 6))
for method_label, info in selected.items():
    steps, values = info["test_series"]
    plt.plot(steps, values, label=f"{method_label}", linewidth=2)

plt.xlabel("Iteración")
plt.ylabel("Success rate (test)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

test_output_path = Path("success_rate_test_best_auc.png")
plt.savefig(test_output_path, dpi=150)
print(f"\nGráfico de test guardado en: {test_output_path.resolve()}")

# ------------------------------------------------------------------
# GRÁFICO 2: SUCCESS RATE EN TRAIN VS ITERACIONES
# ------------------------------------------------------------------

plt.figure(figsize=(10, 6))
for method_label, info in selected.items():
    train_series = info["train_series"]
    if train_series is None:
        print(f"[{method_label}] Aviso: no hay datos de train para el run seleccionado, se omite en el gráfico de train.")
        continue
    steps, values = train_series
    plt.plot(steps, values, label=f"{method_label}", linewidth=2)

plt.xlabel("Iteración")
plt.ylabel("Success rate (train)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

train_output_path = Path("success_rate_train_best_auc.png")
plt.savefig(train_output_path, dpi=150)
print(f"Gráfico de train guardado en: {train_output_path.resolve()}")

plt.show()