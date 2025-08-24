import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

Q_ref = 1835
u_ref = 3
H_ref = 60

def sigma_y(x): return 0.08 * x / (1 + 0.0001 * x) ** 0.5
def sigma_z(x): return 0.06 * x / (1 + 0.0015 * x) ** 0.5

def gaussian_plume(Q, u, H, X, Y, Z, sy_func, sz_func):
    sy = sy_func(X)
    sz = sz_func(X)
    term1 = Q / (2 * np.pi * sy * sz * u)
    term2 = np.exp(-Y**2 / (2 * sy**2))
    term3 = np.exp(-(Z - H)**2 / (2 * sz**2)) + np.exp(-(Z + H)**2 / (2 * sz**2))
    return term1 * term2 * term3

x = np.linspace(1, 51000, 800)
y = np.linspace(-5000, 5000, 400)
X, Y = np.meshgrid(x, y)
Z = np.full_like(X, 0.0)

def generate_range(ref, percent=10, num=100):
    delta = percent / 100 * ref
    return np.linspace(ref - delta, ref + delta, num)

def compute_single_sensitivity(param_list, param_name, Q=Q_ref, u=u_ref, H=H_ref):
    C_list = []
    for val in param_list:
        if param_name == 'Q':
            C = gaussian_plume(val, u, H, X, Y, Z, sigma_y, sigma_z)
        elif param_name == 'u':
            C = gaussian_plume(Q, val, H, X, Y, Z, sigma_y, sigma_z)
        elif param_name == 'H':
            C = gaussian_plume(Q, u, val, X, Y, Z, sigma_y, sigma_z)
        C_max = np.max(C)
        C_list.append(C_max)

    ref_val = {'Q': Q, 'u': u, 'H': H}[param_name]
    idx = np.argmin(np.abs(param_list - ref_val))
    C0 = C_list[idx]

    idx_minus = np.argmin(np.abs(param_list - (ref_val * 0.9)))
    idx_plus = np.argmin(np.abs(param_list - (ref_val * 1.1)))
    delta = ref_val * 0.1
    S_minus = (C_list[idx_minus] - C0) / (-delta) * (ref_val / C0)
    S_plus = (C_list[idx_plus] - C0) / (delta) * (ref_val / C0)

    return C_list, S_minus, S_plus

Q_list = generate_range(Q_ref)
u_list = generate_range(u_ref)
H_list = generate_range(H_ref)

C_Q, S_Q_minus, S_Q_plus = compute_single_sensitivity(Q_list, 'Q')
C_u, S_u_minus, S_u_plus = compute_single_sensitivity(u_list, 'u')
C_H, S_H_minus, S_H_plus = compute_single_sensitivity(H_list, 'H')

stability_classes = {
    'A': (lambda x: 0.22 * x / (1 + 0.0001 * x) ** 0.5, lambda x: 0.20 * x),
    'B': (lambda x: 0.16 * x / (1 + 0.0001 * x) ** 0.5, lambda x: 0.12 * x),
    'C': (lambda x: 0.11 * x / (1 + 0.0001 * x) ** 0.5, lambda x: 0.08 * x / (1 + 0.0002 * x) ** 0.5),
    'D': (lambda x: 0.08 * x / (1 + 0.0001 * x) ** 0.5, lambda x: 0.06 * x / (1 + 0.0015 * x) ** 0.5),
    'E': (lambda x: 0.06 * x / (1 + 0.0001 * x) ** 0.5, lambda x: 0.04 * x / (1 + 0.0015 * x) ** 0.5),
    'F': (lambda x: 0.04 * x / (1 + 0.0001 * x) ** 0.5, lambda x: 0.02 * x / (1 + 0.0015 * x) ** 0.5),
}

stability_order = list(stability_classes.keys())
ref_class = 'D'
ref_index = stability_order.index(ref_class)

C_stab_list = []
for key in stability_order:
    sy_func, sz_func = stability_classes[key]
    C = gaussian_plume(Q_ref, u_ref, H_ref, X, Y, Z, sy_func, sz_func)
    C_stab_list.append(np.max(C))

C0 = C_stab_list[ref_index]
S0 = ref_index + 1
S_stab_list = []

for i, C_val in enumerate(C_stab_list):
    if i == ref_index:
        S_stab_list.append(0.0)
        continue
    delta_C = C_val - C0
    delta_S = (i + 1) - S0
    S = delta_C / delta_S * (S0 / C0)
    S_stab_list.append(S)


df_param = pd.DataFrame({
    '参数': ['Q', 'u', 'H'],
    '-10%扰动': [S_Q_minus, S_u_minus, S_H_minus],
    '+10%扰动': [S_Q_plus, S_u_plus, S_H_plus],
})

df_stab = pd.DataFrame({
    '稳定度等级': stability_order,
    '地面最大浓度': C_stab_list,
    '相对灵敏度系数': S_stab_list
})

with pd.ExcelWriter('../data/gaussian_sensitivity_values.xlsx') as writer:
    df_param.to_excel(writer, index=False, sheet_name='Q_u_H参数灵敏度')
    df_stab.to_excel(writer, index=False, sheet_name='稳定度灵敏度')


percent = np.linspace(-10, 10, 100)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(percent, C_Q, label='排放强度 Q', color='royalblue')
ax1.plot(percent, C_u, label='风速 u', color='darkorange')
ax1.plot(percent, C_H, label='烟囱高度 H', color='forestgreen')
ax1.set_xlabel('扰动百分比 (%)')
ax1.set_ylabel('地面最大浓度 (ug/m$_3$)')
ax1.set_title('参数扰动 vs 地面最大浓度')
ax1.grid(True)
ax1.legend()

ax2.plot(stability_order, C_stab_list, marker='o', color='purple')
ax2.set_xlabel('稳定度等级（A-F）')
ax2.set_ylabel('地面最大浓度 (ug/m$_3$)')
ax2.set_title('稳定度等级 vs 地面最大浓度')
ax2.grid(True)

plt.tight_layout()
plt.savefig("../figure/plot11_param_vs_max_concentration.png", dpi=300, bbox_inches='tight')
plt.show()