import json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
BENCH="#1F3B73"; ECU="#9E3D00"; GREY="#3A3A3A"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":8.5,"axes.labelsize":8.5,
 "xtick.labelsize":8,"ytick.labelsize":8,"legend.fontsize":7.6,"axes.edgecolor":GREY,
 "axes.linewidth":0.9,"pdf.fonttype":42,"savefig.bbox":"tight","savefig.pad_inches":0.03})
d=json.load(open('/home/claude/datos3/vendors.json')); N=d['N']
filas=sorted(d['filas'], key=lambda t:-t[1]['EC'])
filas=[f for f in filas if f[1]['EC']>=4]
ETQ={"EC":("Ecuador",ECU,"//"),"US":("United States",ECU,"\\\\"),
     "EU":("European Union",BENCH,"xx"),"GB":("United Kingdom",BENCH,"..")}
ORD=["EC","US","EU","GB"]
fig,ax=plt.subplots(figsize=(5.15,4.5))
h=0.19
for k,(et,c) in enumerate(filas):
    for j,v in enumerate(ORD):
        lab,col,hat=ETQ[v]
        y=-k+(1.5-j)*h
        ax.barh(y,100*c[v]/N,height=h,color="white",edgecolor=col,hatch=hat,lw=1.0,zorder=2)
ax.set_yticks([-k for k in range(len(filas))])
ax.set_yticklabels([f[0] for f in filas])
ax.set_xlabel(f"Percentage of the {N} sites where the vendor set cookies\nbefore any consent interaction")
ax.set_xlim(0,68)
ax.spines[["top","right","left"]].set_visible(False)
ax.tick_params(axis="y",length=0)
ax.grid(axis="x",color="#CCCCCC",lw=0.6,zorder=0); ax.set_axisbelow(True)
leg=[Patch(facecolor="white",edgecolor=ETQ[v][1],hatch=ETQ[v][2],label=ETQ[v][0]) for v in ORD]
ax.legend(handles=leg,loc="lower center",bbox_to_anchor=(0.45,-0.30),ncol=2,frameon=False)
fig.savefig("fig_vantage.pdf")
print("fig_vantage.pdf")
