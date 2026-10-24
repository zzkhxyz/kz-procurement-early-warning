import sys, pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.stats import beta
D, OUT = sys.argv[1], sys.argv[2]
plt.rcParams.update({'font.family':'serif','font.serif':['Liberation Serif','DejaVu Serif'],'mathtext.fontset':'stix',
 'font.size':8,'axes.labelsize':8,'xtick.labelsize':7.5,'ytick.labelsize':7.5,'legend.fontsize':7.5,
 'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':0.6,
 'xtick.major.width':0.6,'ytick.major.width':0.6,'axes.edgecolor':'#555','xtick.color':'#333','ytick.color':'#333'})
C={'graph':'#2a78d6','tabular':'#eb6834','red_flag':'#1baf7a'}
LAB={'graph':'Graph-enriched IF','tabular':'Tabular IF','red_flag':'Red-flag baseline'}
MK={'graph':'o','tabular':'s','red_flag':'^'}
grid=dict(color='#e3e3e3',lw=0.5)

# Fig 1: recovery@K with exact 95% CIs (co-bidding; rotation identical)
s=pd.read_csv(f'{D}/synthetic_recovery.csv'); s=s[s.pattern=='co_bidding']
fig,ax=plt.subplots(figsize=(3.45,2.25))
xs={0.01:0,0.05:1,0.10:2}; off={'red_flag':-0.18,'tabular':0,'graph':0.18}
ax.yaxis.grid(True,**grid); ax.set_axisbelow(True)
for i,K in enumerate([0.01,0.05,0.10]):
    ax.hlines(K,i-0.32,i+0.32,colors='#888',linestyles=(0,(3,2)),lw=0.8,zorder=1)
for m in ['red_flag','tabular','graph']:
    d=s[s.model==m].sort_values('K'); x=np.array([xs[round(k,2)] for k in d.K])+off[m]
    p=d.recovered.to_numpy(); n=d.n_planted.to_numpy(); y=p/n
    lo=np.where(p==0,0,beta.ppf(.025,p,n-p+1)); hi=np.where(p==n,1,beta.ppf(.975,p+1,n-p))
    ax.errorbar(x,y,yerr=[y-lo,hi-y],fmt=MK[m],ms=4.5,color=C[m],mec='white',mew=0.6,elinewidth=1,capsize=2,label=LAB[m],zorder=3)
ax.set_xticks([0,1,2],['1','5','10']); ax.set_xlim(-0.5,2.5)
ax.set_xlabel('Review capacity $K$ (% of 22,349 test lots)'); ax.set_ylabel('Recovery@$K$ (0–1)')
ax.set_ylim(-0.02,1.05)
h,l=ax.get_legend_handles_labels()
from matplotlib.lines import Line2D
h.append(Line2D([],[],color='#888',ls=(0,(3,2)),lw=0.8)); l.append('Random ranking ($=K$)')
ax.legend(h,l,loc='center right',bbox_to_anchor=(1.0,0.55),frameon=False,handletextpad=0.4,borderaxespad=0.2)
fig.tight_layout(pad=0.3); fig.savefig(f'{OUT}/fig_recovery.pdf'); fig.savefig(f'{OUT}/fig_recovery.png',dpi=200)

# Fig 2: 45 seed-pair Jaccard values per model and K
j=pd.read_csv(f'{D}/seed_jaccard_45pairs.csv')
fig,ax=plt.subplots(figsize=(3.45,2.25)); rng=np.random.default_rng(0)
ax.yaxis.grid(True,**grid); ax.set_axisbelow(True)
off={'tabular':-0.18,'graph':0.18}
for m in ['tabular','graph']:
    for i,K in enumerate([0.01,0.05,0.10]):
        v=j[(j.model==m)&(np.isclose(j.K,K))].jaccard.to_numpy()
        x=i+off[m]+rng.uniform(-0.06,0.06,len(v))
        ax.scatter(x,v,s=7,color=C[m],alpha=0.55,lw=0,marker=MK[m],zorder=2,label=LAB[m] if i==0 else None)
        ax.hlines(v.mean(),i+off[m]-0.12,i+off[m]+0.12,colors='#222',lw=1.2,zorder=3)
ax.axhline(0.7,color='#888',ls=(0,(3,2)),lw=0.8,zorder=1)
ax.text(-0.45,0.685,'$J_K=0.7$ (A2 criterion)',ha='left',va='top',fontsize=7,color='#444')
ax.set_xticks([0,1,2],['1','5','10']); ax.set_xlim(-0.5,2.5); ax.set_ylim(0,1)
ax.set_xlabel('Review capacity $K$ (% of test lots)'); ax.set_ylabel('Top-$K$ Jaccard, seed pairs (0–1)')
h,l=ax.get_legend_handles_labels()
h.append(Line2D([],[],color='#222',lw=1.2)); l.append('Mean of 45 pairs')
ax.legend(h,l,loc='upper left',frameon=False,markerscale=1.6,handletextpad=0.3,borderaxespad=0.2)
fig.tight_layout(pad=0.3); fig.savefig(f'{OUT}/fig_seed_stability.pdf'); fig.savefig(f'{OUT}/fig_seed_stability.png',dpi=200)
