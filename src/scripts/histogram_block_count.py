"""
Analiza la distribución del tamaño (número de bloques) de un conjunto de
problemas de Blocksworld en formato PDDL.

USO:
    python analizar_distribucion_bloques.py /ruta/a/carpeta_problemas

Qué hace:
    1. Recorre todos los archivos .pddl de la carpeta (y subcarpetas) indicada.
    2. Para cada archivo, extrae el número de bloques a partir de la sección
       (:objects ...).
    3. Calcula la distribución de tamaños (conteo por número exacto de
       bloques y agrupado por rangos).
    4. Imprime un resumen en consola, guarda un CSV con el detalle por
       problema y otro CSV con la tabla de distribución agrupada, y genera
       el código LaTeX de la tabla lista para pegar en la tesis.

NOTA sobre el parseo:
    Se asume el formato estándar de PDDL para Blocksworld, donde la sección
    (:objects b1 b2 b3 - block) enumera los bloques. Si tu generador usa un
    formato distinto (por ejemplo, objetos con nombres tipo "block1", o el
    dominio define varios tipos de objeto), ajusta la función
    `contar_bloques_de_archivo` marcada más abajo.
"""

import argparse
import csv
import re
import sys
from pathlib import Path
from collections import Counter

import matplotlib.pyplot as plt


def leer_seccion_objects(texto_pddl: str) -> str:
    """Extrae el contenido bruto de la sección (:objects ...) de un problema PDDL."""
    match = re.search(r":objects(.*?)\)\s*(?:\(:init|\(:goal)", texto_pddl, re.DOTALL | re.IGNORECASE)
    if not match:
        # fallback: buscar hasta el siguiente paréntesis de cierre de nivel superior
        match = re.search(r":objects(.*?)\n\s*\)", texto_pddl, re.DOTALL | re.IGNORECASE)
    if not match:
        return ""
    return match.group(1)


def contar_bloques_de_archivo(path: Path) -> int:
    """
    Devuelve el número de bloques definidos en un archivo de problema PDDL.

    Ajusta esta función si tu formato de objetos es distinto. Por defecto:
    - Busca la sección (:objects ...)
    - Cuenta los tokens que preceden a "- block" (o "- BLOCK"), que es la
      forma típica en la que PDDL tipa los objetos.
    - Si no hay tipado explícito (todos los objetos son de un único tipo
      implícito), cuenta simplemente todos los tokens no vacíos de la
      sección de objetos.
    """
    texto = path.read_text(encoding="utf-8", errors="ignore")
    seccion = leer_seccion_objects(texto)

    if not seccion:
        return 0

    # Caso 1: objetos tipados explícitamente, p. ej. "b1 b2 b3 - block"
    bloques_tipados = re.findall(r"([\w\-]+(?:\s+[\w\-]+)*)\s*-\s*block\b", seccion, re.IGNORECASE)
    if bloques_tipados:
        total = 0
        for grupo in bloques_tipados:
            total += len(grupo.split())
        return total

    # Caso 2: sin tipado explícito -> contar todos los tokens
    tokens = [t for t in seccion.split() if t not in ("-", "")]
    return len(tokens)


def clasificar_rango(n: int, tamano_bin: int = 5, maximo: int = 30) -> str:
    """Agrupa un tamaño de problema en un rango tipo '2-5', '6-10', etc."""
    if n <= 1:
        return "0-1"
    inicio = ((n - 2) // tamano_bin) * tamano_bin + 2
    fin = min(inicio + tamano_bin - 1, maximo)
    if n > maximo:
        return f">{maximo}"
    return f"{inicio}-{fin}"


def generar_grafico(tamanos: list, contador_rangos: dict, salida: Path, clave_orden) -> Path:
    """
    Genera dos subgráficos:
      1) Histograma con el conteo exacto de problemas por número de bloques.
      2) Barras con la distribución agrupada por rangos.
    Guarda el resultado como PNG.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # --- Histograma por tamaño exacto ---
    minimo, maximo = min(tamanos), max(tamanos)
    bins = range(minimo, maximo + 2)  # +2 para incluir el último valor entero
    ax1.hist(tamanos, bins=bins, align="left", edgecolor="black", color="#4C72B0", alpha=0.85)
    ax1.set_xlabel("Número de bloques")
    ax1.set_ylabel("Número de problemas")
    ax1.set_title("Distribución exacta por número de bloques")
    ax1.grid(axis="y", alpha=0.3)

    # --- Barras por rango agrupado ---
    rangos_ordenados = sorted(contador_rangos.keys(), key=clave_orden)
    valores = [contador_rangos[r] for r in rangos_ordenados]
    ax2.bar(rangos_ordenados, valores, color="#DD8452", edgecolor="black", alpha=0.85)
    ax2.set_xlabel("Rango de bloques")
    ax2.set_ylabel("Número de problemas")
    ax2.set_title("Distribución agrupada por rango")
    ax2.grid(axis="y", alpha=0.3)
    ax2.tick_params(axis="x", rotation=45)

    fig.suptitle("Distribución del tamaño de los problemas del conjunto de prueba")
    fig.tight_layout()

    grafico_path = salida / "distribucion_tamano_problemas.png"
    fig.savefig(grafico_path, dpi=150)
    plt.close(fig)
    return grafico_path


def main():
    parser = argparse.ArgumentParser(description="Distribución del tamaño de problemas Blocksworld (PDDL).")
    parser.add_argument("carpeta", type=str, help="Carpeta con los archivos .pddl de los problemas")
    parser.add_argument("--patron", type=str, default="*.pddl", help="Patrón de archivo a buscar (default: *.pddl)")
    parser.add_argument("--bin", type=int, default=5, help="Tamaño del rango para agrupar (default: 5)")
    parser.add_argument("--max", type=int, default=30, help="Tamaño máximo esperado de bloques (default: 30)")
    parser.add_argument("--salida", type=str, default=".", help="Carpeta donde guardar los CSV de salida")
    parser.add_argument("--sin-grafico", action="store_true", help="No generar el gráfico de la distribución")
    args = parser.parse_args()

    carpeta = Path(args.carpeta)
    if not carpeta.is_dir():
        print(f"ERROR: '{carpeta}' no es una carpeta válida.", file=sys.stderr)
        sys.exit(1)

    archivos = sorted(carpeta.rglob(args.patron))
    if not archivos:
        print(f"ERROR: no se han encontrado archivos que coincidan con '{args.patron}' en '{carpeta}'.", file=sys.stderr)
        sys.exit(1)

    detalle = []  # (nombre_archivo, num_bloques)
    for archivo in archivos:
        n = contar_bloques_de_archivo(archivo)
        if n == 0:
            print(f"[AVISO] No se pudo determinar el número de bloques en: {archivo}", file=sys.stderr)
            continue
        detalle.append((archivo.name, n))

    if not detalle:
        print("ERROR: no se ha podido extraer el número de bloques de ningún archivo. "
              "Revisa el formato de tus problemas PDDL y ajusta 'contar_bloques_de_archivo'.", file=sys.stderr)
        sys.exit(1)

    tamanos = [n for _, n in detalle]
    contador_exacto = Counter(tamanos)
    contador_rangos = Counter(clasificar_rango(n, args.bin, args.max) for n in tamanos)

    total = len(tamanos)

    # --- Resumen en consola ---
    print(f"\nTotal de problemas analizados: {total}")
    print(f"Tamaño mínimo: {min(tamanos)} bloques")
    print(f"Tamaño máximo: {max(tamanos)} bloques")
    print(f"Tamaño medio:  {sum(tamanos) / total:.2f} bloques\n")

    print("Distribución por rango de tamaño:")
    def clave_orden(r):
        return int(r.split("-")[0].replace(">", "999"))
    for rango in sorted(contador_rangos.keys(), key=clave_orden):
        n = contador_rangos[rango]
        pct = 100 * n / total
        print(f"  {rango:>8} bloques: {n:>4} problemas ({pct:5.1f}%)")

    # --- Guardar CSV con detalle por problema ---
    salida = Path(args.salida)
    salida.mkdir(parents=True, exist_ok=True)

    detalle_csv = salida / "detalle_tamano_problemas.csv"
    with open(detalle_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["archivo", "num_bloques"])
        writer.writerows(detalle)

    # --- Guardar CSV con la distribución agrupada ---
    distribucion_csv = salida / "distribucion_tamano_problemas.csv"
    with open(distribucion_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rango_bloques", "num_problemas", "porcentaje"])
        for rango in sorted(contador_rangos.keys(), key=clave_orden):
            n = contador_rangos[rango]
            writer.writerow([rango, n, f"{100 * n / total:.1f}"])

    # --- Generar tabla LaTeX ---
    latex_lines = []
    latex_lines.append(r"\begin{table}[ht]")
    latex_lines.append(r"    \centering")
    latex_lines.append(r"    \begin{tabular}{|c|c|c|}")
    latex_lines.append(r"        \hline")
    latex_lines.append(r"        \textbf{Número de bloques} & \textbf{Nº de problemas} & \textbf{Porcentaje} \\")
    latex_lines.append(r"        \hline")
    for rango in sorted(contador_rangos.keys(), key=clave_orden):
        n = contador_rangos[rango]
        pct = 100 * n / total
        latex_lines.append(f"        {rango} & {n} & {pct:.1f}\\% \\\\")
    latex_lines.append(r"        \hline")
    latex_lines.append(r"    \end{tabular}")
    latex_lines.append(r"    \caption[Distribución del tamaño de los problemas del conjunto de prueba.]{Distribución del número de bloques en el conjunto de prueba utilizado para la evaluación.}")
    latex_lines.append(r"    \label{tab:distribucion_tamano_problemas}")
    latex_lines.append(r"\end{table}")

    latex_path = salida / "tabla_distribucion_tamano.tex"
    latex_path.write_text("\n".join(latex_lines), encoding="utf-8")

    # --- Generar gráfico ---
    grafico_path = None
    if not args.sin_grafico:
        grafico_path = generar_grafico(tamanos, contador_rangos, salida, clave_orden)

    print(f"\nArchivos generados en '{salida.resolve()}':")
    print(f"  - {detalle_csv.name}       (número de bloques por cada archivo)")
    print(f"  - {distribucion_csv.name}  (distribución agrupada por rango)")
    print(f"  - {latex_path.name}        (tabla LaTeX lista para pegar en la tesis)")
    if grafico_path:
        print(f"  - {grafico_path.name}       (gráfico de la distribución)")


if __name__ == "__main__":
    main()