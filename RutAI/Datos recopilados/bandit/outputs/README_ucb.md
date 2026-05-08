# RutAI — UCB + Entropía Simulation

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
- **Horizonte:** T = 500 interacciones
- **Semillas:** 100 (base=42)
- **IC:** Bootstrap 95% (1000 iteraciones) sobre curva completa
- **Reward rate:** últimas 100 iter de la misma traza (sin re-simulación)

## Mapeo de endpoints
El contexto de LinUCB usa variables sintéticas reproducibles por semilla:
hora_día ∈ [0,1], tipo_día ∈ {0,1}, distancia ∈ [0,1].

## Cómo citar
DOI Zenodo: _pendiente de asignación tras upload_
