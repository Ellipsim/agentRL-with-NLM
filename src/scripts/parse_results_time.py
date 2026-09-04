from pathlib import Path
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import numpy as np

# ------------------------------------------------------------------
# CONFIGURACIÓN
# ------------------------------------------------------------------

# Carpeta de UN solo método, que contiene las subcarpetas de runs
# (12_1, 12_2, ...), cada una con logs/train.
#
#   base_dir/
#     12_1/logs/train/...
#     12_2/logs/train/...
base_dir = "experiments/final_agent_nesig"

# Subruta dentro de cada run donde están los logs (writer de TRAIN)
logs_subpath = "logs/train"

# Tag de un scalar que se loguee de forma continua durante todo el
# entrenamiento. Se usa solo para leer los timestamps (wall_time) del
# primer y último evento, no su valor.
# AJUSTA ESTO a un tag que exista en tus logs de train.
metric_for_timing = "Agent_PPO/advantage_std_raw"

# ------------------------------------------------------------------
# FUNCIONES AUXILIARES
# ------------------------------------------------------------------

def training_duration_hours(run_logs_dir):
    """Duración del entrenamiento (en horas) = último wall_time - primer wall_time."""
    ea = EventAccumulator(str(run_logs_dir))
    ea.Reload()
    if metric_for_timing not in ea.Tags().get("scalars", []):
        return None
    events = ea.Scalars(metric_for_timing)
    if len(events) < 2:
        return None
    wall_times = sorted(e.wall_time for e in events)
    duration_seconds = wall_times[-1] - wall_times[0]
    return duration_seconds / 3600.0


# ------------------------------------------------------------------
# LOCALIZAR RUNS Y CALCULAR DURACIONES
# ------------------------------------------------------------------

base_path = Path(base_dir)

run_log_dirs = sorted(
    p for p in base_path.glob(f"*/{logs_subpath}")
    if p.is_dir()
)

if not run_log_dirs:
    raise SystemExit(
        f"No se ha encontrado ninguna carpeta '{logs_subpath}' dentro de '{base_dir}'."
    )

print(f"Se han encontrado {len(run_log_dirs)} runs en '{base_dir}':\n")

durations = []
for run_log_dir in run_log_dirs:
    run_name = run_log_dir.parent.name
    d = training_duration_hours(run_log_dir)
    if d is None:
        print(f"  {run_name}: no se pudo calcular (falta el tag '{metric_for_timing}' "
              f"o solo hay un evento)")
        continue
    durations.append(d)
    print(f"  {run_name}: {d:.2f} h ({d * 60:.1f} min)")

if not durations:
    raise SystemExit(
        f"No se ha podido calcular la duración de ningún run. "
        f"Revisa el tag '{metric_for_timing}'."
    )

arr = np.array(durations)

print("\n=== Estadísticos ===")
print(f"n runs        : {len(arr)}")
print(f"Media         : {arr.mean():.2f} h ({arr.mean() * 60:.1f} min)")
print(f"Std           : {arr.std():.2f} h ({arr.std() * 60:.1f} min)")
print(f"Min           : {arr.min():.2f} h")
print(f"Max           : {arr.max():.2f} h")
print(f"Total (suma)  : {arr.sum():.2f} h")