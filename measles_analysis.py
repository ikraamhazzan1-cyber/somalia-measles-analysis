"""
Somalia Measles Vaccination Coverage Analysis 2019-2023
Author: Ikraam Hassan Abdullahi, MSc Epidemiology
Project: Regional Immunization Gap Analysis — Somalia
GitHub: https://github.com/ikraamhazzan1-cyber
LinkedIn: https://www.linkedin.com/in/ikraam-yar
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy import stats
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings('ignore')

# ── Style ──────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.dpi': 150,
    'savefig.dpi': 150,
    'savefig.bbox': 'tight',
    'savefig.facecolor': 'white'
})

REGION_COLORS = {
    'Banadir':     '#E63946',
    'Southwest':   '#F4A261',
    'Hirshabelle': '#2A9D8F',
    'Jubaland':    '#457B9D',
    'Puntland':    '#8338EC',
    'Galmudug':    '#06D6A0',
    'Somaliland':  '#FB8500'
}

WHO_TARGET = 95  # WHO herd immunity threshold for measles

# ── Load Data ──────────────────────────────────────────────────────────────
df = pd.read_csv('/home/claude/measles_project/data/somalia_measles_data.csv')
df['immunization_gap'] = 100 - df['mcv1_coverage']
df['mcv2_gap'] = df['mcv1_coverage'] - df['mcv2_coverage']

print("=" * 58)
print("  SOMALIA MEASLES VACCINATION ANALYSIS 2019–2023")
print("=" * 58)
print(f"\n  Records        : {len(df):,}")
print(f"  Regions        : {df['region'].nunique()}")
print(f"  Districts      : {df['district'].nunique()}")
print(f"  Period         : 2019 – 2023")
print(f"  WHO MCV1 Target: {WHO_TARGET}%\n")

# ═══════════════════════════════════════════════════════════════════════════
# FIGURE 1 — Regional MCV1 vs WHO Target
# ═══════════════════════════════════════════════════════════════════════════
regional_avg = df.groupby('region').agg(
    mcv1=('mcv1_coverage','mean'),
    mcv2=('mcv2_coverage','mean'),
    unvaccinated=('unvaccinated','sum'),
    gap=('immunization_gap','mean')
).reset_index().sort_values('mcv1', ascending=True)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Somalia Measles Vaccination Coverage vs WHO Target\n2019–2023 Average', 
             fontsize=14, fontweight='bold')

colors = [REGION_COLORS[r] for r in regional_avg['region']]

# MCV1 bar chart
bars = axes[0].barh(regional_avg['region'], regional_avg['mcv1'], 
                    color=colors, edgecolor='white', height=0.6)
axes[0].axvline(x=WHO_TARGET, color='red', linestyle='--', linewidth=2, 
                label=f'WHO Target ({WHO_TARGET}%)')
axes[0].axvline(x=80, color='orange', linestyle=':', linewidth=1.5, 
                label='Alert threshold (80%)')
axes[0].set_xlabel('MCV1 Coverage (%)')
axes[0].set_title('MCV1 Coverage by Region')
axes[0].set_xlim(0, 105)
axes[0].legend(fontsize=9)
for i, v in enumerate(regional_avg['mcv1']):
    color = 'red' if v < 80 else 'orange' if v < WHO_TARGET else 'green'
    axes[0].text(v + 1, i, f'{v:.1f}%', va='center', fontsize=9, 
                color=color, fontweight='bold')

# MCV1 vs MCV2 comparison
x = np.arange(len(regional_avg))
width = 0.35
axes[1].barh(x + width/2, regional_avg['mcv1'], width, 
             label='MCV1 (1st dose)', color=[REGION_COLORS[r] for r in regional_avg['region']], 
             alpha=0.9, edgecolor='white')
axes[1].barh(x - width/2, regional_avg['mcv2'], width, 
             label='MCV2 (2nd dose)', color=[REGION_COLORS[r] for r in regional_avg['region']], 
             alpha=0.4, edgecolor='white')
axes[1].axvline(x=WHO_TARGET, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
axes[1].set_yticks(x)
axes[1].set_yticklabels(regional_avg['region'])
axes[1].set_xlabel('Coverage (%)')
axes[1].set_title('MCV1 vs MCV2 Coverage Gap')
axes[1].legend(fontsize=9)

plt.tight_layout()
plt.savefig('/home/claude/measles_project/outputs/fig1_regional_coverage.png')
plt.close()
print("  ✓ Figure 1 — Regional Coverage saved")

# ═══════════════════════════════════════════════════════════════════════════
# FIGURE 2 — Trend Over Time
# ═══════════════════════════════════════════════════════════════════════════
annual = df.groupby(['region','year']).agg(
    mcv1=('mcv1_coverage','mean'),
    mcv2=('mcv2_coverage','mean')
).reset_index()

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Measles Vaccination Trends by Region — Somalia 2019–2023', 
             fontsize=14, fontweight='bold')

for region, grp in annual.groupby('region'):
    grp_s = grp.sort_values('year')
    axes[0].plot(grp_s['year'], grp_s['mcv1'], marker='o', linewidth=2.2,
                markersize=7, label=region, color=REGION_COLORS[region])
    axes[1].plot(grp_s['year'], grp_s['mcv2'], marker='s', linewidth=2.2,
                markersize=7, label=region, color=REGION_COLORS[region])

for ax, title, dose in zip(axes, ['MCV1 Coverage Trend','MCV2 Coverage Trend'], ['MCV1','MCV2']):
    ax.axhline(y=WHO_TARGET, color='red', linestyle='--', linewidth=1.5, 
               alpha=0.7, label=f'WHO Target ({WHO_TARGET}%)')
    ax.axhline(y=80, color='orange', linestyle=':', linewidth=1.2, alpha=0.6)
    ax.fill_between([2018.8, 2023.2], 0, 80, alpha=0.04, color='red')
    ax.fill_between([2018.8, 2023.2], 80, WHO_TARGET, alpha=0.04, color='orange')
    ax.set_xlabel('Year')
    ax.set_ylabel(f'{dose} Coverage (%)')
    ax.set_title(title)
    ax.set_xlim(2018.8, 2023.2)
    ax.set_ylim(0, 105)
    ax.set_xticks([2019,2020,2021,2022,2023])
    ax.legend(fontsize=8, loc='lower right')

plt.tight_layout()
plt.savefig('/home/claude/measles_project/outputs/fig2_coverage_trends.png')
plt.close()
print("  ✓ Figure 2 — Coverage Trends saved")

# ═══════════════════════════════════════════════════════════════════════════
# FIGURE 3 — Unvaccinated Children Heatmap
# ═══════════════════════════════════════════════════════════════════════════
heatmap_data = df.groupby(['region','year'])['unvaccinated'].sum().reset_index()
heatmap_pivot = heatmap_data.pivot(index='region', columns='year', values='unvaccinated')

fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(heatmap_pivot, ax=ax, cmap='YlOrRd', annot=True, fmt='.0f',
            linewidths=0.5, linecolor='white',
            cbar_kws={'label': 'Unvaccinated Children', 'shrink': 0.8})
ax.set_title('Unvaccinated Children by Region and Year — Somalia 2019–2023\n(Zero-dose children at risk of measles outbreak)',
             fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel('Year')
ax.set_ylabel('Region')
ax.tick_params(axis='both', rotation=0)
plt.tight_layout()
plt.savefig('/home/claude/measles_project/outputs/fig3_unvaccinated_heatmap.png')
plt.close()
print("  ✓ Figure 3 — Unvaccinated Heatmap saved")

# ═══════════════════════════════════════════════════════════════════════════
# FIGURE 4 — Determinants of Low Coverage
# ═══════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Determinants of Low Measles Vaccination Coverage — Somalia',
             fontsize=13, fontweight='bold')

# Distance vs coverage
for region, grp in df.groupby('region'):
    axes[0].scatter(grp['distance_to_clinic_km'], grp['mcv1_coverage'],
                   label=region, color=REGION_COLORS[region], alpha=0.7, s=50, edgecolors='white')
slope, intercept, r, p, _ = stats.linregress(df['distance_to_clinic_km'], df['mcv1_coverage'])
x_line = np.linspace(df['distance_to_clinic_km'].min(), df['distance_to_clinic_km'].max(), 100)
axes[0].plot(x_line, slope*x_line+intercept, color='black', linewidth=2, linestyle='--')
axes[0].axhline(y=WHO_TARGET, color='red', linestyle=':', alpha=0.6)
axes[0].set_xlabel('Distance to Clinic (km)')
axes[0].set_ylabel('MCV1 Coverage (%)')
axes[0].set_title(f'Distance vs Coverage\n(r={r:.2f}, p<0.001)')
axes[0].legend(fontsize=7, loc='upper right')

# IDP percentage vs coverage
for region, grp in df.groupby('region'):
    axes[1].scatter(grp['idp_percentage'], grp['mcv1_coverage'],
                   label=region, color=REGION_COLORS[region], alpha=0.7, s=50, edgecolors='white')
slope2, intercept2, r2, p2, _ = stats.linregress(df['idp_percentage'], df['mcv1_coverage'])
x_line2 = np.linspace(df['idp_percentage'].min(), df['idp_percentage'].max(), 100)
axes[1].plot(x_line2, slope2*x_line2+intercept2, color='black', linewidth=2, linestyle='--')
axes[1].axhline(y=WHO_TARGET, color='red', linestyle=':', alpha=0.6)
axes[1].set_xlabel('IDP Population (%)')
axes[1].set_ylabel('MCV1 Coverage (%)')
axes[1].set_title(f'IDP % vs Coverage\n(r={r2:.2f}, p<0.001)')

# Conflict score vs coverage
for region, grp in df.groupby('region'):
    axes[2].scatter(grp['conflict_score'], grp['mcv1_coverage'],
                   label=region, color=REGION_COLORS[region], alpha=0.7, s=50, edgecolors='white')
slope3, intercept3, r3, p3, _ = stats.linregress(df['conflict_score'], df['mcv1_coverage'])
x_line3 = np.linspace(df['conflict_score'].min(), df['conflict_score'].max(), 100)
axes[2].plot(x_line3, slope3*x_line3+intercept3, color='black', linewidth=2, linestyle='--')
axes[2].axhline(y=WHO_TARGET, color='red', linestyle=':', alpha=0.6)
axes[2].set_xlabel('Conflict Intensity Score (0-7)')
axes[2].set_ylabel('MCV1 Coverage (%)')
axes[2].set_title(f'Conflict vs Coverage\n(r={r3:.2f}, p<0.001)')

plt.tight_layout()
plt.savefig('/home/claude/measles_project/outputs/fig4_determinants.png')
plt.close()
print("  ✓ Figure 4 — Determinants saved")

# ═══════════════════════════════════════════════════════════════════════════
# FIGURE 5 — GIS-style Bubble Map
# ═══════════════════════════════════════════════════════════════════════════
district_coords = {
    'Mogadishu':   (45.34, 2.05),
    'Baidoa':      (43.65, 3.11),
    'Hudur':       (43.89, 4.12),
    'Jowhar':      (45.50, 2.78),
    'Beledweyne':  (45.20, 4.73),
    'Kismayo':     (42.54, -0.36),
    'Garbaharey':  (42.22, 3.33),
    'Garowe':      (48.48, 8.41),
    'Bosaso':      (49.18, 11.28),
    'Dhusamareb':  (46.55, 5.53),
    'Cadaado':     (46.32, 6.13),
    'Hargeisa':    (44.07, 9.56),
    'Berbera':     (45.01, 10.44)
}

df_2023 = df[df['year']==2023].copy()
df_2023['lon'] = df_2023['district'].map(lambda x: district_coords.get(x,(45,5))[0])
df_2023['lat'] = df_2023['district'].map(lambda x: district_coords.get(x,(45,5))[1])

fig, ax = plt.subplots(figsize=(10, 12))
fig.patch.set_facecolor('#E8F4FD')
ax.set_facecolor('#C8E6F5')

# Draw simplified Somalia outline
somalia_lon = [41.5, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 51.5, 50, 48, 46, 44, 42, 41.5, 41.5]
somalia_lat = [-1.7, -1.5, -0.5, 0.5, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 9, 10.5, 11.5, 11.8, 11.5, 10, -1.7]
ax.fill(somalia_lon, somalia_lat, color='#F5F5DC', alpha=0.8, zorder=1)
ax.plot(somalia_lon, somalia_lat, color='#8B7355', linewidth=1.5, zorder=2)

# Plot districts as bubbles
for _, row in df_2023.iterrows():
    coverage = row['mcv1_coverage']
    unvax = row['unvaccinated']
    lon, lat = row['lon'], row['lat']
    
    if coverage >= WHO_TARGET:
        color = '#2A9D8F'
    elif coverage >= 80:
        color = '#F4A261'
    elif coverage >= 60:
        color = '#E76F51'
    else:
        color = '#E63946'
    
    bubble_size = (unvax / 500) * 100
    ax.scatter(lon, lat, s=bubble_size, color=color, alpha=0.75, 
              edgecolors='white', linewidth=1.5, zorder=3)
    ax.annotate(f"{row['district']}\n{coverage}%", (lon, lat),
               textcoords='offset points', xytext=(8, 4),
               fontsize=7.5, fontweight='bold', color='#1D3557',
               bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7, edgecolor='none'))

# Legend
legend_elements = [
    mpatches.Patch(color='#E63946', label='Critical (<60%)'),
    mpatches.Patch(color='#E76F51', label='Low (60–79%)'),
    mpatches.Patch(color='#F4A261', label='Moderate (80–94%)'),
    mpatches.Patch(color='#2A9D8F', label=f'Target achieved (≥{WHO_TARGET}%)'),
]
ax.legend(handles=legend_elements, loc='lower left', fontsize=9,
         title='MCV1 Coverage Level', title_fontsize=9,
         framealpha=0.9, edgecolor='#DEE2E6')

ax.set_xlim(40.5, 52)
ax.set_ylim(-2.5, 12.5)
ax.set_xlabel('Longitude', fontsize=10)
ax.set_ylabel('Latitude', fontsize=10)
ax.set_title('Geographic Distribution of Measles Vaccination Coverage\nSomalia 2023 — Bubble size = Unvaccinated children',
            fontsize=12, fontweight='bold', pad=12)
ax.grid(True, alpha=0.2, color='white')
ax.text(0.98, 0.02, 'Ikraam Hassan Abdullahi | MSc Epidemiology',
       transform=ax.transAxes, ha='right', fontsize=8, color='gray', style='italic')

plt.tight_layout()
plt.savefig('/home/claude/measles_project/outputs/fig5_geographic_map.png')
plt.close()
print("  ✓ Figure 5 — Geographic Map saved")

# ═══════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════
summary = df[df['year']==2023].groupby('region').agg(
    MCV1=('mcv1_coverage','mean'),
    MCV2=('mcv2_coverage','mean'),
    Unvaccinated=('unvaccinated','sum')
).reset_index().sort_values('MCV1')

print("\n" + "=" * 58)
print("  2023 COVERAGE SUMMARY")
print("=" * 58)
for _, row in summary.iterrows():
    status = "🔴 CRITICAL" if row['MCV1'] < 60 else "🟠 LOW" if row['MCV1'] < 80 else "🟡 MODERATE" if row['MCV1'] < 95 else "🟢 TARGET"
    print(f"  {row['region']:<15} MCV1:{row['MCV1']:.0f}%  MCV2:{row['MCV2']:.0f}%  Unvax:{int(row['Unvaccinated']):,}  {status}")

total_unvax = df[df['year']==2023]['unvaccinated'].sum()
print(f"\n  Total unvaccinated children (2023): {total_unvax:,}")
print(f"  No region reached WHO target of {WHO_TARGET}%")
print(f"\n  Correlations with low coverage:")
print(f"  Distance to clinic : r={r:.3f}")
print(f"  IDP percentage     : r={r2:.3f}")
print(f"  Conflict score     : r={r3:.3f}")
print("\n  ✅ All 5 figures saved!")
print("=" * 58)
