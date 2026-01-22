import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

def plot_sweeps_from_file(filepath, ax=None):
    data = []
    current_sweep = None

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith('"Sweep'):
                current_sweep = line.replace('"', '')
                continue

            # Nos quedamos SOLO con Function 2
            if current_sweep and "Function 2" not in current_sweep:
                continue

            if line.startswith('"X') or line.startswith('"Vac'):
                continue

            if "," in line and current_sweep:
                try:
                    x, y = map(float, line.split(","))
                    data.append((x, y))
                except ValueError:
                    pass

    if not data:
        raise ValueError("No se encontraron datos de Sweep - Function 2")

    x = [p[0]
         * 1.15
         for p in data]
    y = [p[1]
         + 0.15
         for p in data]

    # Si no me pasan axis, me fabrico uno
    created_fig = False
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))
        created_fig = True

    ax.plot(x, y, linestyle="-")
    ax.set_xscale("log")
    ax.grid(True, which="both")
    ax.set_xlabel("Frecuencia (Hz)")
    ax.set_ylabel("Amplitud (dBr)")
    ax.set_title("Sweep - Function 2")

    if created_fig:
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    BASE_DIR = "./MedisionesFinales/MEDICIONES_PATRON/PASA BAJOS 20K/PB-20K-M.csv"
    plot_sweeps_from_file(BASE_DIR)

