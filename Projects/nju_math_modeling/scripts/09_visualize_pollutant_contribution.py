import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

lst = []

# 依次读取每个季度的 Sheet
for i in range(1, 5):
    df = pd.read_excel("../data/fuzzy_contrib_rank_stats.xlsx", sheet_name=f"Q{i}", index_col=0)
    array = df.to_numpy()  # 转为 numpy 数组
    lst.append(array)

rank_weights = np.array([1.0, 0.8, 0.6, 0.2, 0.15, 0.1])

pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'O3', 'CO']
quarters = ['第一季度', '第二季度', '第三季度', '第四季度']

weighted_contrib_matrix = np.zeros((6, 4))
for i, quarter_matrix in enumerate(lst):

    weighted_contrib_matrix[:, i] = quarter_matrix @ rank_weights

row_sums = weighted_contrib_matrix.sum(axis=1)

weights = row_sums / row_sums.sum()

print(weights)

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(
    weighted_contrib_matrix,
    annot=True,
    fmt=".1f",
    cmap='YlGnBu',
    xticklabels=quarters,
    yticklabels=pollutants,
    ax=ax
)

ax.set_title("四个季度污染物加权总贡献热力图", fontsize=16, weight='bold')
ax.set_xlabel("季度", fontsize=12)
ax.set_ylabel("污染物", fontsize=12)

plt.tight_layout()
plt.savefig("../figure/plot09_weighted_contribution_heatmap.png", dpi=300, bbox_inches='tight')
plt.show()