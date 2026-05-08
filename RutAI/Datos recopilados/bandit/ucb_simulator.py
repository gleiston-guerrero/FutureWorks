"""
RutAI — Simulador UCB + Entropía
=================================
Replica EXACTAMENTE el algoritmo de app/services/ucb_service.py:
  - 3 brazos: fastest, shortest, recommended
  - Recompensa binaria: completada=1, cancelada=0
  - Exploración forzada cuando total_usos == 0
  - UCB score = avg_reward + sqrt(2 * ln(N) / n_i) + lambda * H(p_i)

Genera los datos para la Tabla 4 del artículo científico.

Correcciones v2:
  - reward_rate calculado en la MISMA traza de simulación (últimas 100 iter)
    en vez de re-simular con policy2/env2 independiente
  - requirements.txt y README generados automáticamente
  - Notebook .ipynb generado al final
"""

import numpy as np
import matplotlib.pyplot as plt
import json
import math
import random
import csv
import nbformat
from typing import Dict, Tuple
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────────────────────
SEED_BASE   = 42
N_SEEDS     = 100
HORIZON     = 500
TIPOS_RUTA  = ["fastest", "shortest", "recommended"]

OUTPUT_DIR = Path(__file__).parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

REWARD_PROBS = {
    "fastest":     0.40,
    "shortest":    0.50,
    "recommended": 0.65,
}
OPTIMAL_ARM  = "recommended"
OPTIMAL_PROB = REWARD_PROBS[OPTIMAL_ARM]

# ─────────────────────────────────────────────────────────────
# ENTORNO
# ─────────────────────────────────────────────────────────────

class BanditEnv:
    """Entorno de bandido con 3 brazos y recompensas Bernoulli."""
    def __init__(self, seed: int):
        self.rng = np.random.default_rng(seed)

    def pull(self, arm: str) -> int:
        return int(self.rng.random() < REWARD_PROBS[arm])


# ─────────────────────────────────────────────────────────────
# ALGORITMOS
# ─────────────────────────────────────────────────────────────

class UCBRutAI:
    """Replica EXACTA de UCBService (app/services/ucb_service.py)."""
    def __init__(self, seed: int, lambda_ent: float = 0.1):
        self.rng = random.Random(seed)
        self.lambda_ent = lambda_ent
        self.total_usos    = {t: 0 for t in TIPOS_RUTA}
        self.total_rewards = {t: 0 for t in TIPOS_RUTA}

    def select(self) -> str:
        total_plays = sum(self.total_usos.values())

        if total_plays < len(TIPOS_RUTA):
            usados     = {t for t in TIPOS_RUTA if self.total_usos[t] > 0}
            pendientes = [t for t in TIPOS_RUTA if t not in usados]
            if pendientes:
                return self.rng.choice(pendientes)

        for t in TIPOS_RUTA:
            if self.total_usos[t] == 0:
                return t

        best_arm, best_score = None, -float("inf")
        for t in TIPOS_RUTA:
            avg    = self.total_rewards[t] / self.total_usos[t]
            conf   = math.sqrt(2 * math.log(total_plays) / self.total_usos[t])
            p      = avg
            H      = 0.0 if p <= 0 or p >= 1 else -p * math.log2(p) - (1 - p) * math.log2(1 - p)
            score  = avg + conf + self.lambda_ent * H
            if score > best_score:
                best_score, best_arm = score, t
        return best_arm or "fastest"

    def update(self, arm: str, reward: int):
        self.total_usos[arm]    += 1
        self.total_rewards[arm] += reward


class RandomPolicy:
    def __init__(self, seed: int):
        self.rng = random.Random(seed)
    def select(self) -> str:
        return self.rng.choice(TIPOS_RUTA)
    def update(self, arm: str, reward: int):
        pass


class GreedyPolicy:
    def __init__(self, seed: int):
        self.rng = random.Random(seed)
        self.total_usos    = {t: 0 for t in TIPOS_RUTA}
        self.total_rewards = {t: 0 for t in TIPOS_RUTA}

    def select(self) -> str:
        for t in TIPOS_RUTA:
            if self.total_usos[t] == 0:
                return t
        return max(TIPOS_RUTA, key=lambda t: self.total_rewards[t] / self.total_usos[t])

    def update(self, arm: str, reward: int):
        self.total_usos[arm]    += 1
        self.total_rewards[arm] += reward


class EpsilonGreedy:
    def __init__(self, epsilon: float, seed: int):
        self.epsilon = epsilon
        self.rng     = random.Random(seed)
        self.total_usos    = {t: 0 for t in TIPOS_RUTA}
        self.total_rewards = {t: 0 for t in TIPOS_RUTA}

    def select(self) -> str:
        for t in TIPOS_RUTA:
            if self.total_usos[t] == 0:
                return t
        if self.rng.random() < self.epsilon:
            return self.rng.choice(TIPOS_RUTA)
        return max(TIPOS_RUTA, key=lambda t: self.total_rewards[t] / self.total_usos[t])

    def update(self, arm: str, reward: int):
        self.total_usos[arm]    += 1
        self.total_rewards[arm] += reward


class ThompsonSampling:
    def __init__(self, seed: int):
        self.rng   = np.random.default_rng(seed)
        self.alpha = {t: 1 for t in TIPOS_RUTA}
        self.beta  = {t: 1 for t in TIPOS_RUTA}

    def select(self) -> str:
        samples = {t: self.rng.beta(self.alpha[t], self.beta[t]) for t in TIPOS_RUTA}
        return max(samples, key=samples.get)

    def update(self, arm: str, reward: int):
        if reward:
            self.alpha[arm] += 1
        else:
            self.beta[arm]  += 1


class LinUCBDiag:
    """
    LinUCB diagonalizado (Li et al., 2010).
    Vector de contexto d=3: hora normalizada, tipo de día, distancia normalizada.
    Nota: contexto sintético generado de forma reproducible por semilla.
    """
    def __init__(self, alpha: float, seed: int, d: int = 3):
        self.alpha = alpha
        self.d     = d
        self.rng   = np.random.default_rng(seed)
        self.A = {t: np.eye(d)        for t in TIPOS_RUTA}
        self.b = {t: np.zeros((d, 1)) for t in TIPOS_RUTA}
        self._last_ctx = None

    def _context(self) -> np.ndarray:
        hora      = self.rng.uniform(0, 1)
        laboral   = float(self.rng.integers(0, 2))
        distancia = self.rng.uniform(0, 1)
        return np.array([[hora], [laboral], [distancia]])

    def select(self) -> str:
        ctx = self._context()
        self._last_ctx = ctx
        best_arm, best_score = None, -np.inf
        for t in TIPOS_RUTA:
            A_inv = np.linalg.inv(self.A[t])
            theta = A_inv @ self.b[t]
            p = float((theta.T @ ctx)[0, 0]) + self.alpha * float(np.sqrt((ctx.T @ A_inv @ ctx)[0, 0]))
            if p > best_score:
                best_score, best_arm = p, t
        return best_arm

    def update(self, arm: str, reward: int):
        ctx = self._last_ctx
        self.A[arm] += ctx @ ctx.T
        self.b[arm] += reward * ctx


# ─────────────────────────────────────────────────────────────
# FUNCIÓN DE SIMULACIÓN (CORREGIDA)
# ─────────────────────────────────────────────────────────────

def simulate_policy(policy_factory, n_seeds: int = N_SEEDS, horizon: int = HORIZON) -> Dict:
    """
    Ejecuta la política para n_seeds semillas.

    CORRECCIÓN v2: reward_rate se mide en las últimas 100 interacciones
    de la MISMA traza de simulación, no en una re-simulación independiente.
    Esto elimina el sesgo introducido al crear policy2/env2 con semillas
    distintas que no comparten el historial de aprendizaje.

    Devuelve:
      - regret_mean/std/ci_lower/ci_upper  por timestep
      - final_regret_mean/ci
      - reward_rate_mean/std (últimas 100 iter, misma traza)
    """
    all_regrets      = []
    all_reward_rates = []

    for s in range(n_seeds):
        seed   = SEED_BASE + s
        env    = BanditEnv(seed)
        policy = policy_factory(seed)

        cumulative_regret = 0.0
        regrets_run       = []
        rewards_last100   = []

        for t in range(horizon):
            arm    = policy.select()
            reward = env.pull(arm)

            instant_regret     = OPTIMAL_PROB - REWARD_PROBS[arm]
            cumulative_regret += instant_regret
            regrets_run.append(cumulative_regret)

            # Recoger recompensa de las últimas 100 iteraciones (misma traza)
            if t >= horizon - 100:
                rewards_last100.append(reward)

            policy.update(arm, reward)

        all_regrets.append(regrets_run)
        all_reward_rates.append(float(np.mean(rewards_last100)))

    arr = np.array(all_regrets)  # shape (n_seeds, horizon)

    # Bootstrap IC 95% sobre la curva completa
    rng_bs  = np.random.default_rng(0)
    n_boot  = 1000
    boot_idx   = rng_bs.choice(n_seeds, size=(n_boot, n_seeds), replace=True)
    boot_means = np.array([arr[boot_idx[i]].mean(axis=0) for i in range(n_boot)])

    ci_lower = np.percentile(boot_means, 2.5,  axis=0)
    ci_upper = np.percentile(boot_means, 97.5, axis=0)
    ci_half  = (ci_upper - ci_lower) / 2

    return {
        "regret_mean":        arr.mean(axis=0),
        "regret_std":         arr.std(axis=0),
        "regret_ci_lower":    ci_lower,
        "regret_ci_upper":    ci_upper,
        "regret_ci_half":     ci_half,
        "final_regret_mean":  float(arr[:, -1].mean()),
        "final_regret_ci":    float(ci_half[-1]),
        "reward_rate_mean":   float(np.mean(all_reward_rates)),
        "reward_rate_std":    float(np.std(all_reward_rates)),
    }


# ─────────────────────────────────────────────────────────────
# EJECUTAR
# ─────────────────────────────────────────────────────────────

print("=" * 60)
print("Simulador UCB RutAI v2")
print(f"Semillas: {N_SEEDS} | Horizonte: {HORIZON} pasos")
print(f"Reward_rate: últimas 100 iter de la misma traza (sin re-sim)")
print("=" * 60)

policies = {
    "Random":                 lambda s: RandomPolicy(s),
    "Greedy":                 lambda s: GreedyPolicy(s),
    "ε-greedy (ε=0.1)":      lambda s: EpsilonGreedy(0.1, s),
    "ε-greedy (ε=0.2)":      lambda s: EpsilonGreedy(0.2, s),
    "Thompson":               lambda s: ThompsonSampling(s),
    "LinUCB":                 lambda s: LinUCBDiag(alpha=1.0, seed=s),
    "UCB + Entropía (RutAI)": lambda s: UCBRutAI(s, lambda_ent=0.1),
}

results = {}
for name, factory in policies.items():
    print(f"  Simulando: {name}...", end=" ", flush=True)
    results[name] = simulate_policy(factory)
    r = results[name]
    print(f"Regret final = {r['final_regret_mean']:.2f} ± {r['final_regret_ci']:.2f}  |  "
          f"Tasa éxito = {r['reward_rate_mean']:.3f} ± {r['reward_rate_std']:.3f}")

print()

# ─────────────────────────────────────────────────────────────
# TABLA PAPER
# ─────────────────────────────────────────────────────────────

print("─" * 75)
print(f"{'Algoritmo':<25} {'Regret final (µ ± IC95%)':<32} {'Tasa éxito (µ ± σ)'}")
print("─" * 75)
for name, r in results.items():
    marker = " ← propuesto" if "RutAI" in name else ""
    print(f"{name:<25} {r['final_regret_mean']:>7.2f} ± {r['final_regret_ci']:.2f}"
          f"{'':>16} {r['reward_rate_mean']:.3f} ± {r['reward_rate_std']:.3f}{marker}")
print("─" * 75)

# ─────────────────────────────────────────────────────────────
# EXPORTAR JSON + CSV
# ─────────────────────────────────────────────────────────────

export = {}
for name, r in results.items():
    export[name] = {
        "final_regret_mean": round(r["final_regret_mean"], 4),
        "final_regret_ci95": round(r["final_regret_ci"],   4),
        "reward_rate_mean":  round(r["reward_rate_mean"],  4),
        "reward_rate_std":   round(r["reward_rate_std"],   4),
        "regret_at_t100":    round(float(r["regret_mean"][99]),  4),
        "regret_at_t250":    round(float(r["regret_mean"][249]), 4),
        "regret_at_t500":    round(float(r["regret_mean"][-1]),  4),
    }

json_path = OUTPUT_DIR / "ucb_results.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(export, f, indent=2, ensure_ascii=False)
print(f"\n✓ ucb_results.json → {json_path}")

csv_path = OUTPUT_DIR / "ucb_timesteps.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["timestep", "algorithm", "regret_mean", "ci_lower", "ci_upper"])
    for name, r in results.items():
        for i in range(HORIZON):
            writer.writerow([i + 1, name,
                             f"{r['regret_mean'][i]:.4f}",
                             f"{r['regret_ci_lower'][i]:.4f}",
                             f"{r['regret_ci_upper'][i]:.4f}"])
print(f"✓ ucb_timesteps.csv → {csv_path}")

metadata = {
    "experiment":  "UCB + Entropía vs baselines",
    "version":     "2",
    "horizon":     HORIZON,
    "n_seeds":     N_SEEDS,
    "seed_base":   SEED_BASE,
    "arms":        TIPOS_RUTA,
    "reward_probs": REWARD_PROBS,
    "optimal_arm": OPTIMAL_ARM,
    "algorithms":  list(policies.keys()),
    "ci_method":   "Bootstrap 95% (1000 iter) sobre curva completa",
    "reward_rate_method": "Últimas 100 iteraciones de la misma traza de simulación",
    "linucb_context": "Sintético: hora∈[0,1], laboral∈{0,1}, distancia∈[0,1] — reproducible por semilla",
}
meta_path = OUTPUT_DIR / "metadata.json"
with open(meta_path, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)
print(f"✓ metadata.json → {meta_path}")

# ─────────────────────────────────────────────────────────────
# FIGURAS
# ─────────────────────────────────────────────────────────────

colors = {
    "Random":                 "#e74c3c",
    "Greedy":                 "#e67e22",
    "ε-greedy (ε=0.1)":      "#f1c40f",
    "ε-greedy (ε=0.2)":      "#d4ac0d",
    "Thompson":               "#2ecc71",
    "LinUCB":                 "#3498db",
    "UCB + Entropía (RutAI)": "#8e44ad",
}
styles = {
    "Random": "-", "Greedy": "--",
    "ε-greedy (ε=0.1)": "-.", "ε-greedy (ε=0.2)": ":",
    "Thompson": "-", "LinUCB": "--", "UCB + Entropía (RutAI)": "-",
}
lw = {k: 1.5 for k in policies}
lw["UCB + Entropía (RutAI)"] = 2.8

t = np.arange(1, HORIZON + 1)

# Fig 1: Curvas de regret
fig, ax = plt.subplots(figsize=(9, 5.5))
for name, r in results.items():
    ax.plot(t, r["regret_mean"], color=colors[name], linestyle=styles[name],
            lw=lw[name], label=name, zorder=3 if "RutAI" in name else 2)
    ax.fill_between(t, r["regret_ci_lower"], r["regret_ci_upper"],
                    color=colors[name], alpha=0.12, zorder=1)
ax.set_xlabel("Interacciones (t)", fontsize=12)
ax.set_ylabel("Regret acumulado medio", fontsize=12)
ax.set_title(f"Comparación de algoritmos de bandido\n"
             f"(T={HORIZON}, {N_SEEDS} semillas, IC 95% bootstrap)", fontsize=13)
ax.legend(fontsize=9, loc="upper left", framealpha=0.9)
ax.grid(True, alpha=0.3)
ax.set_xlim(1, HORIZON)
ax.set_ylim(bottom=0)
plt.tight_layout()
fig1_path = OUTPUT_DIR / "ucb_regret_curves.png"
plt.savefig(str(fig1_path), dpi=150, bbox_inches="tight")
plt.close()
print(f"✓ ucb_regret_curves.png → {fig1_path}")

# Fig 2: Barras de regret final
names  = list(results.keys())
means  = [results[n]["final_regret_mean"] for n in names]
errors = [results[n]["final_regret_ci"]   for n in names]
bar_colors = [colors[n] for n in names]

fig, ax = plt.subplots(figsize=(9, 4.5))
bars = ax.bar(names, means, yerr=errors, color=bar_colors,
              capsize=5, alpha=0.85, edgecolor="white", linewidth=0.8)
for bar, name in zip(bars, names):
    if "RutAI" in name:
        bar.set_edgecolor("#4a148c")
        bar.set_linewidth(2.5)
ax.set_ylabel("Regret acumulado final (µ ± IC95%)", fontsize=11)
ax.set_title(f"Regret final tras T={HORIZON} interacciones\n"
             f"({N_SEEDS} semillas, bootstrap IC 95%)", fontsize=12)
ax.set_xticks(range(len(names)))
ax.set_xticklabels(names, rotation=18, ha="right", fontsize=9)
ax.grid(axis="y", alpha=0.3)
ax.set_ylim(bottom=0)
plt.tight_layout()
fig2_path = OUTPUT_DIR / "ucb_final_regret_bar.png"
plt.savefig(str(fig2_path), dpi=150, bbox_inches="tight")
plt.close()
print(f"✓ ucb_final_regret_bar.png → {fig2_path}")

# Fig 3: Frecuencia de selección del brazo óptimo
def simulate_optimal_freq(policy_factory, n_seeds=N_SEEDS, horizon=HORIZON):
    all_optimal = []
    for s in range(n_seeds):
        seed   = SEED_BASE + s
        env    = BanditEnv(seed)
        policy = policy_factory(seed)
        flags  = []
        for _ in range(horizon):
            arm = policy.select()
            r   = env.pull(arm)
            flags.append(int(arm == OPTIMAL_ARM))
            policy.update(arm, r)
        all_optimal.append(flags)
    arr = np.array(all_optimal)
    window   = 20
    smoothed = np.convolve(arr.mean(axis=0), np.ones(window) / window, mode="valid")
    return smoothed

print("\nCalculando frecuencia de brazo óptimo...")
fig, ax = plt.subplots(figsize=(9, 5))
for name, factory in policies.items():
    smooth = simulate_optimal_freq(factory)
    t2     = np.arange(len(smooth)) + 1
    ax.plot(t2, smooth, color=colors[name], linestyle=styles[name],
            lw=lw[name], label=name, zorder=3 if "RutAI" in name else 2)
ax.axhline(y=1/3, color="gray", linestyle=":", lw=1.2, label="Selección aleatoria (1/3)")
ax.set_xlabel("Interacciones (t)", fontsize=12)
ax.set_ylabel("P(brazo óptimo seleccionado)", fontsize=12)
ax.set_title(f"Convergencia al brazo óptimo (media móvil w=20)\n"
             f"Brazo óptimo = '{OPTIMAL_ARM}'  [P(r=1) = {OPTIMAL_PROB}]", fontsize=12)
ax.legend(fontsize=9, loc="lower right", framealpha=0.9)
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 1.05)
ax.set_xlim(1, HORIZON - 20)
plt.tight_layout()
fig3_path = OUTPUT_DIR / "ucb_optimal_arm_freq.png"
plt.savefig(str(fig3_path), dpi=150, bbox_inches="tight")
plt.close()
print(f"✓ ucb_optimal_arm_freq.png → {fig3_path}")

# ─────────────────────────────────────────────────────────────
# GENERAR JUPYTER NOTEBOOK (requerido por Zenodo)
# ─────────────────────────────────────────────────────────────

nb = nbformat.v4.new_notebook()
nb.metadata["kernelspec"] = {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3",
}

cells_text = [
    ("markdown", """# RutAI — Simulador UCB + Entropía\n\n**Artículo:** Comparación de algoritmos de bandido para recomendación de rutas  \n**Versión:** 2 (corrección reward_rate en misma traza)  \n**Semillas:** 100 | **Horizonte:** T = 500\n\nEste notebook es el artefacto reproducible para Zenodo. Ejecutar en orden."""),
    ("markdown", "## 1. Instalación de dependencias"),
    ("code", "# !pip install numpy matplotlib scipy nbformat\nimport subprocess, sys\nsubprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy', 'matplotlib', 'scipy', 'nbformat', '-q'])"),
    ("markdown", "## 2. Configuración"),
    ("code", f"""import numpy as np
import matplotlib.pyplot as plt
import json, math, random, csv
from pathlib import Path

SEED_BASE   = {SEED_BASE}
N_SEEDS     = {N_SEEDS}
HORIZON     = {HORIZON}
TIPOS_RUTA  = {TIPOS_RUTA}
REWARD_PROBS = {json.dumps(REWARD_PROBS)}
OPTIMAL_ARM  = "{OPTIMAL_ARM}"
OPTIMAL_PROB = REWARD_PROBS[OPTIMAL_ARM]
print("Config OK — brazos:", TIPOS_RUTA)
print("Probabilidades de recompensa:", REWARD_PROBS)"""),
    ("markdown", "## 3. Definición del entorno y algoritmos\nSe copia la lógica de `app/services/ucb_service.py`."),
    ("code", """class BanditEnv:
    def __init__(self, seed):
        self.rng = np.random.default_rng(seed)
    def pull(self, arm):
        return int(self.rng.random() < REWARD_PROBS[arm])

class UCBRutAI:
    def __init__(self, seed, lambda_ent=0.1):
        self.rng = random.Random(seed)
        self.lambda_ent = lambda_ent
        self.total_usos    = {t: 0 for t in TIPOS_RUTA}
        self.total_rewards = {t: 0 for t in TIPOS_RUTA}
    def select(self):
        total = sum(self.total_usos.values())
        if total < len(TIPOS_RUTA):
            pend = [t for t in TIPOS_RUTA if self.total_usos[t] == 0]
            if pend: return self.rng.choice(pend)
        for t in TIPOS_RUTA:
            if self.total_usos[t] == 0: return t
        best, bs = None, -float('inf')
        for t in TIPOS_RUTA:
            avg  = self.total_rewards[t] / self.total_usos[t]
            conf = math.sqrt(2 * math.log(total) / self.total_usos[t])
            p    = avg
            H    = 0.0 if p<=0 or p>=1 else -p*math.log2(p)-(1-p)*math.log2(1-p)
            s    = avg + conf + self.lambda_ent * H
            if s > bs: bs, best = s, t
        return best or 'fastest'
    def update(self, arm, reward):
        self.total_usos[arm]    += 1
        self.total_rewards[arm] += reward
print("Clases definidas OK")"""),
    ("markdown", "## 4. Simulación\n**CORRECCIÓN v2:** `reward_rate` se mide en las últimas 100 iteraciones de la **misma** traza, eliminando el sesgo de re-simulación."),
    ("code", """def simulate(policy_factory, n_seeds=N_SEEDS, horizon=HORIZON):
    all_regrets, all_rates = [], []
    for s in range(n_seeds):
        env    = BanditEnv(SEED_BASE + s)
        policy = policy_factory(SEED_BASE + s)
        cum, run, last100 = 0.0, [], []
        for t in range(horizon):
            arm = policy.select()
            r   = env.pull(arm)
            cum += OPTIMAL_PROB - REWARD_PROBS[arm]
            run.append(cum)
            if t >= horizon - 100: last100.append(r)
            policy.update(arm, r)
        all_regrets.append(run)
        all_rates.append(float(np.mean(last100)))
    arr   = np.array(all_regrets)
    rng_b = np.random.default_rng(0)
    bidx  = rng_b.choice(n_seeds, size=(1000, n_seeds), replace=True)
    bmean = np.array([arr[bidx[i]].mean(axis=0) for i in range(1000)])
    ci_l  = np.percentile(bmean, 2.5,  axis=0)
    ci_u  = np.percentile(bmean, 97.5, axis=0)
    return {
        'regret_mean': arr.mean(axis=0), 'ci_lower': ci_l, 'ci_upper': ci_u,
        'final_regret': float(arr[:,-1].mean()), 'final_ci': float((ci_u-ci_l)[-1]/2),
        'reward_rate': float(np.mean(all_rates)), 'reward_std': float(np.std(all_rates)),
    }
print("Función simulate() OK")"""),
    ("markdown", "## 5. Resultados — Tabla 4"),
    ("code", """import importlib, sys

# Definir baselines inline para el notebook
class RandomPolicy:
    def __init__(self, s): self.rng = random.Random(s)
    def select(self): return self.rng.choice(TIPOS_RUTA)
    def update(self, a, r): pass

class GreedyPolicy:
    def __init__(self, s):
        self.rng = random.Random(s)
        self.u = {t:0 for t in TIPOS_RUTA}
        self.rw = {t:0 for t in TIPOS_RUTA}
    def select(self):
        for t in TIPOS_RUTA:
            if self.u[t]==0: return t
        return max(TIPOS_RUTA, key=lambda t: self.rw[t]/self.u[t])
    def update(self, a, r): self.u[a]+=1; self.rw[a]+=r

class EG:
    def __init__(self, eps, s):
        self.eps=eps; self.rng=random.Random(s)
        self.u={t:0 for t in TIPOS_RUTA}; self.rw={t:0 for t in TIPOS_RUTA}
    def select(self):
        for t in TIPOS_RUTA:
            if self.u[t]==0: return t
        return self.rng.choice(TIPOS_RUTA) if self.rng.random()<self.eps else max(TIPOS_RUTA,key=lambda t:self.rw[t]/self.u[t])
    def update(self, a, r): self.u[a]+=1; self.rw[a]+=r

class TS:
    def __init__(self, s):
        self.rng=np.random.default_rng(s)
        self.alpha={t:1 for t in TIPOS_RUTA}; self.beta={t:1 for t in TIPOS_RUTA}
    def select(self):
        return max({t:self.rng.beta(self.alpha[t],self.beta[t]) for t in TIPOS_RUTA}, key=lambda t:0)
    def update(self, a, r):
        if r: self.alpha[a]+=1
        else: self.beta[a]+=1

policies_nb = {
    'Random':           lambda s: RandomPolicy(s),
    'Greedy':           lambda s: GreedyPolicy(s),
    'ε-greedy (0.1)':  lambda s: EG(0.1, s),
    'ε-greedy (0.2)':  lambda s: EG(0.2, s),
    'Thompson':        lambda s: TS(s),
    'UCB+Entropía':    lambda s: UCBRutAI(s),
}

results_nb = {}
for name, fac in policies_nb.items():
    print(f'Simulando {name}...', end=' ')
    results_nb[name] = simulate(fac)
    r = results_nb[name]
    print(f\"regret={r['final_regret']:.2f}±{r['final_ci']:.2f}  rate={r['reward_rate']:.3f}\")"""),
    ("markdown", "## 6. Visualización"),
    ("code", """fig, ax = plt.subplots(figsize=(9, 5))
t_arr = np.arange(1, HORIZON+1)
for name, r in results_nb.items():
    ax.plot(t_arr, r['regret_mean'], label=name, lw=2.5 if 'UCB' in name else 1.5)
    ax.fill_between(t_arr, r['ci_lower'], r['ci_upper'], alpha=0.1)
ax.set_xlabel('Interacciones (t)'); ax.set_ylabel('Regret acumulado')
ax.set_title(f'Regret acumulado — T={HORIZON}, {N_SEEDS} semillas, IC95% bootstrap')
ax.legend(fontsize=9); ax.grid(alpha=0.3)
plt.tight_layout(); plt.show()"""),
    ("markdown", "## 7. Cómo citar\n\n```\nAutor, A. (2025). RutAI UCB Simulation [Software]. Zenodo. https://doi.org/XXXX\n```\n\nSustituir `XXXX` por el DOI asignado en Zenodo tras la subida."),
]

for kind, source in cells_text:
    if kind == "markdown":
        nb.cells.append(nbformat.v4.new_markdown_cell(source))
    else:
        nb.cells.append(nbformat.v4.new_code_cell(source))

nb_path = OUTPUT_DIR / "ucb_simulation_reproducible.ipynb"
with open(nb_path, "w", encoding="utf-8") as f:
    nbformat.write(nb, f)
print(f"\n✓ Jupyter notebook → {nb_path}")

# ─────────────────────────────────────────────────────────────
# requirements.txt
# ─────────────────────────────────────────────────────────────
req_path = OUTPUT_DIR / "requirements.txt"
req_path.write_text("numpy>=1.26\nmatplotlib>=3.8\nscipy>=1.12\nnbformat>=5.9\n", encoding="utf-8")
print(f"✓ requirements.txt → {req_path}")

# ─────────────────────────────────────────────────────────────
# README
# ─────────────────────────────────────────────────────────────
readme_path = OUTPUT_DIR / "README_ucb.md"
readme_path.write_text(f"""# RutAI — UCB + Entropía Simulation

## Descripción
Simulación comparativa de algoritmos de bandido multi-brazo para recomendación
de tipos de ruta en la app RutAI. Replica `app/services/ucb_service.py`.

## Archivos
| Archivo | Descripción |
|---------|-------------|
| `ucb_simulation.py` | Script principal |
| `ucb_simulation_reproducible.ipynb` | Notebook Jupyter para Zenodo |
| `outputs/ucb_results.json` | Resultados numéricos (Tabla 4) |
| `outputs/ucb_timesteps.csv` | Regret por timestep |
| `outputs/ucb_regret_curves.png` | Figura: curvas de regret |
| `outputs/ucb_final_regret_bar.png` | Figura: regret final |
| `outputs/ucb_optimal_arm_freq.png` | Figura: convergencia |

## Reproducibilidad
```bash
pip install -r requirements.txt
python ucb_simulation.py
# o abrir el notebook:
jupyter notebook ucb_simulation_reproducible.ipynb
```

## Configuración
- **Brazos:** fastest (p=0.40), shortest (p=0.50), recommended (p=0.65)
- **Horizonte:** T = {HORIZON} interacciones
- **Semillas:** {N_SEEDS} (base={SEED_BASE})
- **IC:** Bootstrap 95% (1000 iteraciones) sobre curva completa
- **Reward rate:** últimas 100 iter de la misma traza (sin re-simulación)

## Mapeo de endpoints
El contexto de LinUCB usa variables sintéticas reproducibles por semilla:
hora_día ∈ [0,1], tipo_día ∈ {{0,1}}, distancia ∈ [0,1].

## Cómo citar
DOI Zenodo: _pendiente de asignación tras upload_
""", encoding="utf-8")
print(f"✓ README_ucb.md → {readme_path}")

print("\n✅ Simulación v2 completada.")