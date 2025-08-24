import numpy as np
import matplotlib.pyplot as plt


Q_ref = 1835
u_ref = 3
H_ref = 60


def sigma_y(x): return 0.08 * x / (1 + 0.0001 * x) ** 0.5
def sigma_z(x): return 0.06 * x / (1 + 0.0015 * x) ** 0.5


def gaussian_line(Q, u, H, x_vals, sy_func, sz_func):
    sy = sy_func(x_vals)
    sz = sz_func(x_vals)
    term1 = Q / (2 * np.pi * sy * sz * u)
    term2 = 1.0  # y = 0
    term3 = np.exp(-(0 - H)**2 / (2 * sz**2)) + np.exp(-(0 + H)**2 / (2 * sz**2))
    return term1 * term2 * term3

x_vals = np.linspace(100, 51000, 800)
perturb = 0.1

def get_stab_sigma(class_name):
    stability_sigma = {
        'A': (lambda x: 0.22 * x / (1 + 0.0001 * x)**0.5, lambda x: 0.20 * x),
        'B': (lambda x: 0.16 * x / (1 + 0.0001 * x)**0.5, lambda x: 0.12 * x),
        'C': (lambda x: 0.11 * x / (1 + 0.0001 * x)**0.5, lambda x: 0.08 * x / (1 + 0.0002 * x)**0.5),
        'D': (lambda x: 0.08 * x / (1 + 0.0001 * x)**0.5, lambda x: 0.06 * x / (1 + 0.0015 * x)**0.5),
        'E': (lambda x: 0.06 * x / (1 + 0.0001 * x)**0.5, lambda x: 0.04 * x / (1 + 0.0015 * x)**0.5),
        'F': (lambda x: 0.04 * x / (1 + 0.0001 * x)**0.5, lambda x: 0.02 * x / (1 + 0.0015 * x)**0.5),
    }
    return stability_sigma[class_name]

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes = axes.flatten()
colors = ['darkblue', 'black', 'darkorange']

#Q
C_Qp = gaussian_line(Q_ref * (1 + perturb), u_ref, H_ref, x_vals, sigma_y, sigma_z)
C_Q0 = gaussian_line(Q_ref, u_ref, H_ref, x_vals, sigma_y, sigma_z)
C_Qm = gaussian_line(Q_ref * (1 - perturb), u_ref, H_ref, x_vals, sigma_y, sigma_z)

axes[0].plot(x_vals, C_Qp, color=colors[0], label='+10% Q')
axes[0].plot(x_vals, C_Q0, color=colors[1], linestyle='--', label='基准 Q')
axes[0].plot(x_vals, C_Qm, color=colors[2], label='-10% Q')
axes[0].set_title('排放强度 Q 扰动影响')
axes[0].set_xlabel('下风向距离 x (m)')
axes[0].set_ylabel('浓度 (ug/m$^3$)')
axes[0].grid(True)
axes[0].legend()

#u
C_up = gaussian_line(Q_ref, u_ref * (1 + perturb), H_ref, x_vals, sigma_y, sigma_z)
C_um = gaussian_line(Q_ref, u_ref * (1 - perturb), H_ref, x_vals, sigma_y, sigma_z)

axes[1].plot(x_vals, C_up, color=colors[0], label='+10% u')
axes[1].plot(x_vals, C_Q0, color=colors[1], linestyle='--', label='基准 u')
axes[1].plot(x_vals, C_um, color=colors[2], label='-10% u')
axes[1].set_title('风速 u 扰动影响')
axes[1].set_xlabel('下风向距离 x (m)')
axes[1].set_ylabel('浓度 (ug/m$^3$)')
axes[1].grid(True)
axes[1].legend()

#H
C_Hp = gaussian_line(Q_ref, u_ref, H_ref * (1 + perturb), x_vals, sigma_y, sigma_z)
C_Hm = gaussian_line(Q_ref, u_ref, H_ref * (1 - perturb), x_vals, sigma_y, sigma_z)

axes[2].plot(x_vals, C_Hp, color=colors[0], label='+10% H')
axes[2].plot(x_vals, C_Q0, color=colors[1], linestyle='--', label='基准 H')
axes[2].plot(x_vals, C_Hm, color=colors[2], label='-10% H')
axes[2].set_title('烟囱高度 H 扰动影响')
axes[2].set_xlabel('下风向距离 x (m)')
axes[2].set_ylabel('浓度 (ug/m$^3$)')
axes[2].grid(True)
axes[2].legend()


sigC, sigD, sigE = get_stab_sigma('C'), get_stab_sigma('D'), get_stab_sigma('E')
C_C = gaussian_line(Q_ref, u_ref, H_ref, x_vals, *sigC)
C_D = gaussian_line(Q_ref, u_ref, H_ref, x_vals, *sigD)
C_E = gaussian_line(Q_ref, u_ref, H_ref, x_vals, *sigE)

axes[3].plot(x_vals, C_C, color=colors[0], label='稳定度 C')
axes[3].plot(x_vals, C_D, color=colors[1], linestyle='--', label='稳定度 D（基准）')
axes[3].plot(x_vals, C_E, color=colors[2], label='稳定度 E')
axes[3].set_title('稳定度扰动影响')
axes[3].set_xlabel('下风向距离 x (m)')
axes[3].set_ylabel('浓度 (ug/m$^3$)')
axes[3].grid(True)
axes[3].legend()

plt.suptitle('y=0, z=0 时各参数扰动对污染物浓度分布的影响', fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("../figure/plot12_y0_z0_param_sensitivity.png", dpi=300, bbox_inches='tight')
plt.show()
