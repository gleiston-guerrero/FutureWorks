# -*- coding: utf-8 -*-
"""Figura 4: prevalencia de cada proveedor por punto de observacion.
Datos: campana de 15 pasadas del 16 de agosto de 2026, n=121 sitios."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
plt.rcParams.update({"font.family":"serif","font.size":8,"axes.linewidth":.6})
N=121
# familia: (EC, US, GB, DE, CH)  — verificado contra los JSON, mayoria de 3 pasadas
datos=[("Google",69,68,64,63,58),("Meta",25,25,15,16,11),("Microsoft",14,14,0,0,0),
       ("LinkedIn",13,13,3,4,2),("TikTok",12,12,9,7,8),("Hotjar",8,8,6,6,3),
       ("TapAd",4,4,0,0,0),("Baidu",4,4,2,2,2),("Adobe",2,2,2,2,2)]
etiq=["Ecuador","United States","United Kingdom","Germany","Switzerland"]
OCRE="#B8860B"; NAVY="#1F3864"
col=[OCRE,OCRE,NAVY,NAVY,NAVY]; hatch=["","//","","//","xx"]
fig,ax=plt.subplots(figsize=(7.0,3.3))
y=np.arange(len(datos)); h=0.16
for k in range(5):
    v=[100*d[k+1]/N for d in datos]
    ax.barh(y+(2-k)*h, v, height=h, color=col[k], edgecolor="white",
            linewidth=.4, hatch=hatch[k], label=etiq[k])
ax.set_yticks(y); ax.set_yticklabels([d[0] for d in datos])
ax.invert_yaxis(); ax.set_xlabel("Sites setting at least one cookie before consent (%)")
ax.set_xlim(0,62); ax.grid(axis="x",linewidth=.4,alpha=.35); ax.set_axisbelow(True)
for s in ("top","right"): ax.spines[s].set_visible(False)
ax.legend(loc="lower right",frameon=False,fontsize=7,ncol=1)
fig.tight_layout(); fig.savefig("fig_vantage.pdf"); print("fig_vantage.pdf generada")
