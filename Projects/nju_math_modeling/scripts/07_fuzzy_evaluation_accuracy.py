import numpy as np
import pandas as pd


types = ['PM2.5','PM10','SO2','NO2','O3','CO']
ranks=['I','II','III','IV']
rank_values=[
    [15, 35, 75, 120],
    [40, 70, 150, 200],
    [20, 60, 100, 140],
    [20, 40, 60, 80],
    [100, 160, 220, 280],
    [2, 4, 6, 8]
]

weight_lst=[
    [0.21500626, 0.17690561, 0.10938722, 0.21912507, 0.1866901, 0.09288574],
    [0.16284845 ,0.26812348,0.11321468, 0.19955507 ,0.17221305 ,0.08404527],
    [0.17185946, 0.1267788 , 0.09809252, 0.23151886 ,0.23496299 ,0.13678738],
    [0.22758504,0.17693654 ,0.08497872 ,0.18687918, 0.23357161 ,0.09004892]
]


def compute_membership(xi, s):
    rij = np.zeros(4)
    if xi <= s[0]:
        for k in range(0,4):
            rij[k] = 0.4-k*0.1
    elif xi >= s[-1]:
        rij[-1] = 1
    else:
        for j in range(4):
            if j == 0:
                if s[j] < xi <= s[j+1]:
                    rij[j] = (s[j+1] - xi) / (s[j+1] - s[j])
            elif j == 3:
                if s[j-1] < xi <= s[j]:
                    rij[j] = (xi - s[j-1]) / (s[j] - s[j-1])
            else:
                if s[j-1] < xi <= s[j]:
                    rij[j] = (xi - s[j-1]) / (s[j] - s[j-1])
                elif s[j] < xi <= s[j+1]:
                    rij[j] = (s[j+1] - xi) / (s[j+1] - s[j])
    return rij

def evaluate_levels(data, weights):
    n_samples = data.shape[0]
    levels = []

    contrib_rank_counts = np.zeros((6, 6), dtype=int)

    for i in range(n_samples):

        R = np.array([
            compute_membership(data[i, j], rank_values[j])
            for j in range(6)
        ])

        B = weights @ R

        level = ranks[np.argmax(B)]
        levels.append(level)

        contrib_vector = weights * R[:, np.argmax(B)]

        top4_indices = np.argsort(-contrib_vector)[:6]

        for rank, idx in enumerate(top4_indices):
            contrib_rank_counts[idx, rank] += 1

    return levels, contrib_rank_counts

def aqi_level(aqi_values):
    aqi_values = np.array(aqi_values)
    levels = np.full_like(aqi_values, 'IV', dtype=object)
    levels[aqi_values <= 150] = 'III'
    levels[aqi_values <= 100] = 'II'
    levels[aqi_values <= 50] = 'I'
    return levels


def compare_lists(list1, list2):
    if len(list1) != len(list2):
        raise ValueError("两个列表长度不一致")

    list1 = np.array(list1)
    list2 = np.array(list2)

    matches = list1 == list2
    accuracy = np.mean(matches)

    return accuracy, matches.sum(), len(list1)


def relaxed_accuracy(pred, true, tolerance=1):
    rank_map = {'I': 1, 'II': 2, 'III': 3, 'IV': 4}
    pred_vals = np.array([rank_map[x] for x in pred])
    true_vals = np.array([rank_map[x] for x in true])

    diff = np.abs(pred_vals - true_vals)
    within_tol = diff <= tolerance

    relaxed_acc = np.mean(within_tol)
    return relaxed_acc

lst=[]
for i in range(1,5):
    weights=weight_lst[i-1]
    df = pd.read_excel(f"../data/data_Q{i}.xlsx")

    pollutant_columns = ['PM2.5_24h', 'PM10_24h', 'SO2', 'NO2', 'O3', 'CO', 'AQI']
    pollutant_data = df[pollutant_columns]

    sample = pollutant_data.dropna().to_numpy()

    l1,counts = evaluate_levels(sample[:, 0:6],weights)
    lst.append(counts)
    l2 = aqi_level(sample[:, 6])

    a1, c, t = compare_lists(l1, l2)
    a2=relaxed_accuracy(l1,l2)
    print(f"--------------第{i}季度数学模型预测结果以及各污染物作为最大贡献指标的次数和占比----------")
    print(f'准确率：{a1:.3f}',f'等级插值容忍准确率：{a2:.3f}', f'\n样本总数：{t}', f'相同个数：{c}')
    for k in range(0,6):
        print(f"-----第{k + 1}程度贡献-----")
        total = sum(counts[:,k])
        proportions = [c / total for c in counts[:,k]]
        for t, c, p in zip(types, counts[:,k], proportions):
            print(f"{t}: 次数 = {c}, 占比 = {p:.3f}")
    print("\n")


    compare = {
        '预测值': l1,
        '真实值': l2
    }

    df1 = pd.DataFrame(compare)
    df1.to_excel(f'result_Q{i}.xlsx', index=False)

with pd.ExcelWriter("../data/fuzzy_contrib_rank_stats.xlsx") as writer:
    for i, counts in enumerate(lst):
        df_counts = pd.DataFrame(
            counts,
            index=types,
            columns=[f"第{j+1}程度贡献" for j in range(6)]
        )
        df_counts.to_excel(writer, sheet_name=f"Q{i+1}")



