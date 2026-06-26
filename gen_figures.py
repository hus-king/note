import matplotlib.pyplot as plt
import numpy as np
import os

# --- Style: clean textbook look ---
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 12,
    'axes.titlesize': 13,
    'axes.labelsize': 12,
    'figure.dpi': 150,
    'savefig.dpi': 150,
    'savefig.bbox': 'tight',
})

out = '/Users/hesiqi/Desktop/note/images'

# ============================================================
# 1. Unit ramp signal  R(t)  &  R(t-t0)
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.5))

t = np.linspace(-1, 6, 700)
R = np.maximum(t, 0)
t0 = 2
R_shift = np.maximum(t - t0, 0)

ax1.plot(t, R, 'b', linewidth=1.8)
ax1.set_title(r'$R(t)$')
ax1.set_xlabel('$t$'); ax1.set_ylabel(r'$R(t)$')
ax1.set_xlim(-1, 6); ax1.set_ylim(-0.5, 6.5)
ax1.axhline(0, color='gray', linewidth=0.5)
ax1.axvline(0, color='gray', linewidth=0.5)
ax1.grid(True, alpha=0.3)

ax2.plot(t, R_shift, 'b', linewidth=1.8)
ax2.set_title(r'$R(t - t_0),\ t_0 = 2$')
ax2.set_xlabel('$t$'); ax2.set_ylabel(r'$R(t-t_0)$')
ax2.set_xlim(-1, 8); ax2.set_ylim(-0.5, 6.5)
ax2.axhline(0, color='gray', linewidth=0.5)
ax2.axvline(t0, color='red', linestyle='--', linewidth=0.8, label=r'$t=t_0$')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_ramp.png'))
plt.close(fig)

# ============================================================
# 2. Unit step signal  u(t)  &  u(t-t0)
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.5))

t = np.linspace(-3, 6, 900)
u = np.heaviside(t, 1)     # u(0)=1 convention
t0 = 2
u_shift = np.heaviside(t - t0, 1)

for ax, data, title, jump_x in [
    (ax1, u, r'$u(t)$', 0),
    (ax2, u_shift, r'$u(t - t_0),\ t_0 = 2$', t0),
]:
    ax.plot(t, data, 'b', linewidth=1.8)
    ax.set_title(title)
    ax.set_xlabel('$t$'); ax.set_ylabel('')
    ax.set_xlim(-3, 6); ax.set_ylim(-0.2, 1.3)
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.grid(True, alpha=0.3)
    # mark jump point at the correct x
    ax.plot([jump_x, jump_x], [0, 1], 'b', linewidth=1.8)
ax2.axvline(t0, color='red', linestyle='--', linewidth=0.8)

fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_step.png'))
plt.close(fig)

# ============================================================
# 3. Rectangular pulse (gate)  G(t) & G1(t)
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.5))

t = np.linspace(-1, 5, 900)
tau = 2
G = np.heaviside(t, 1) - np.heaviside(t - tau, 1)

t0 = 1
t = np.linspace(-1, 6, 900)
G1 = np.heaviside(t - t0, 1) - np.heaviside(t - t0 - tau, 1)

ax1.plot(t, G, 'b', linewidth=1.8)
ax1.set_title(r'$G(t) = u(t) - u(t-\tau),\ \tau=2$')
ax1.set_xlabel('$t$'); ax1.set_ylabel('')
ax1.set_xlim(-1, 5); ax1.set_ylim(-0.2, 1.3)
ax1.axhline(0, color='gray', linewidth=0.5)
ax1.grid(True, alpha=0.3)

ax2.plot(t, G1, 'b', linewidth=1.8)
ax2.set_title(r'$G_1(t) = u(t-t_0) - u(t-t_0-\tau)$')
ax2.set_xlabel('$t$'); ax2.set_ylabel('')
ax2.set_xlim(-1, 6); ax2.set_ylim(-0.2, 1.3)
ax2.axhline(0, color='gray', linewidth=0.5)
ax2.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_gate.png'))
plt.close(fig)

# ============================================================
# 4. Piecewise signal  g(t)
# ============================================================
fig, ax = plt.subplots(figsize=(9, 4))

t = np.linspace(-0.5, 4, 1000)
g = np.where((t >= 0) & (t < 1), t,
     np.where((t >= 1) & (t < 2), 1,
     np.where((t >= 2) & (t <= 3), 3 - t, 0)))

ax.plot(t, g, 'b', linewidth=1.8)
ax.set_title(r'$g(t) = t[u(t)-u(t-1)] + [u(t-1)-u(t-2)] + (3-t)[u(t-2)-u(t-3)]$', fontsize=11)
ax.set_xlabel('$t$'); ax.set_ylabel('$g(t)$')
ax.set_xlim(-0.5, 4); ax.set_ylim(-0.2, 1.5)
ax.axhline(0, color='gray', linewidth=0.5)
ax.axvline(0, color='gray', linewidth=0.5)
ax.grid(True, alpha=0.3)

# Mark key points
for x in [0, 1, 2, 3]:
    ax.axvline(x, color='red', linestyle='--', linewidth=0.6, alpha=0.5)

fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_piecewise.png'))
plt.close(fig)

# ============================================================
# 5. Unit impulse  δ(t)  (arrow representation)
# ============================================================
fig, ax = plt.subplots(figsize=(5, 4))

ax.annotate('', xy=(0, 1), xytext=(0, 0),
            arrowprops=dict(arrowstyle='->', color='b', lw=2.5))
ax.annotate('1', xy=(0.15, 0.85), fontsize=13, color='b')
# baseline
ax.axhline(0, color='gray', linewidth=0.5)
ax.axvline(0, color='gray', linewidth=0.5)

# Add small text for the definition
ax.text(2, 0.6, r'$\int_{-\infty}^{\infty}\delta(t)dt=1$', fontsize=12)
ax.text(2, 0.3, r'$\delta(t)=0\ (t\neq 0)$', fontsize=12)

ax.set_title(r'Unit impulse  $\delta(t)$', fontsize=13)
ax.set_xlim(-3, 5); ax.set_ylim(-0.2, 1.5)
ax.set_xlabel('$t$')
ax.grid(True, alpha=0.2)
ax.set_yticklabels([])   # hide y ticks — arrow height is not the value

fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_impulse.png'))
plt.close(fig)

# ============================================================
# 6. Impulse as limit of narrowing rectangular pulses
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))

t = np.linspace(-2.5, 2.5, 1000)
taus = [1.0, 0.5, 0.25]

for ax, tau in zip(axes, taus):
    rect = (np.heaviside(t + tau/2, 1) - np.heaviside(t - tau/2, 1)) / tau
    ax.plot(t, rect, 'b', linewidth=1.5)
    ax.fill_between(t, rect, alpha=0.15, color='b')
    ax.set_title(r'$\tau = {}$'.format(tau), fontsize=12)
    ax.set_xlabel('$t$')
    ax.set_xlim(-2, 2); ax.set_ylim(-0.1, 2.5)
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.grid(True, alpha=0.3)
    ax.text(1.2, 2.1, f'area = 1', fontsize=10, color='gray')

axes[0].set_ylabel(r'$\frac{1}{\tau}$')
fig.suptitle(r'$\delta(t) = \lim_{\tau \to 0} \frac{1}{\tau}[u(t+\tau/2) - u(t-\tau/2)]$', fontsize=13)
fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_impulse_limit.png'))
plt.close(fig)

# ============================================================
# 7. Impulse doublet  δ'(t)
# ============================================================
fig, ax = plt.subplots(figsize=(5.5, 4))

# The doublet is conceptual — draw a schematic
# Up-arrow at 0-
ax.annotate('', xy=(0, 1.3), xytext=(0, 0.05),
            arrowprops=dict(arrowstyle='->', color='b', lw=2.5))
ax.text(0.12, 0.7, r'$+\infty$', fontsize=11, color='b')
# Down-arrow at 0+ (we offset slightly for visual separation)
ax.annotate('', xy=(0, -1.3), xytext=(0, -0.05),
            arrowprops=dict(arrowstyle='->', color='b', lw=2.5))
ax.text(0.12, -0.9, r'$-\infty$', fontsize=11, color='b')

# label the two lobes
ax.text(-0.6, 0.5, r"$t \to 0^-$", fontsize=10, color='gray')
ax.text(0.3, -0.6, r"$t \to 0^+$", fontsize=10, color='gray')

ax.axhline(0, color='gray', linewidth=0.5)
ax.axvline(0, color='gray', linewidth=0.5)
ax.set_title(r"Impulse doublet  $\delta'(t) = \frac{d}{dt}\delta(t)$", fontsize=13)
ax.set_xlim(-3, 3); ax.set_ylim(-2, 2)
ax.set_xlabel('$t$')
ax.grid(True, alpha=0.2)
ax.set_yticklabels([])

fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_impulse_doublet.png'))
plt.close(fig)

print("All 7 figures saved to images/")

# ============================================================
# 8. Signal decomposition — approximation by rectangular pulses
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

# --- Generate a sample signal ---
t = np.linspace(0, 3, 1000)
f = 0.5 + 0.8 * np.sin(1.8 * t) * np.exp(-0.3 * t)

# --- Left: coarse approximation with Δt = 1.0 ---
ax = axes[0]
dt_coarse = 1.0
t_k = np.arange(0, 3, dt_coarse)
ax.plot(t, f, 'k', linewidth=1.2, label=r'$f(t)$ (original)')
for tk in t_k:
    fk = 0.5 + 0.8 * np.sin(1.8 * tk) * np.exp(-0.3 * tk)
    rect_t = np.linspace(tk, tk + dt_coarse, 100)
    ax.fill_between(rect_t, 0, fk, alpha=0.35, color='blue', edgecolor='blue', linewidth=0.5)
ax.set_title(r'Coarse approximation  ($\Delta t = 1.0$)', fontsize=12)
ax.set_xlabel('$t$'); ax.set_ylabel('$f(t)$')
ax.set_xlim(-0.1, 3.1); ax.set_ylim(-0.1, 1.3)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.axhline(0, color='gray', linewidth=0.5)

# --- Right: finer approximation with Δt = 0.5 ---
ax = axes[1]
dt_fine = 0.5
t_k = np.arange(0, 3, dt_fine)
ax.plot(t, f, 'k', linewidth=1.2, label=r'$f(t)$ (original)')
for tk in t_k:
    fk = 0.5 + 0.8 * np.sin(1.8 * tk) * np.exp(-0.3 * tk)
    rect_t = np.linspace(tk, tk + dt_fine, 50)
    ax.fill_between(rect_t, 0, fk, alpha=0.35, color='blue', edgecolor='blue', linewidth=0.5)
ax.set_title(r'Finer approximation  ($\Delta t = 0.5$)', fontsize=12)
ax.set_xlabel('$t$')
ax.set_xlim(-0.1, 3.1); ax.set_ylim(-0.1, 1.3)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.axhline(0, color='gray', linewidth=0.5)

fig.suptitle(r'Signal decomposition: $f(t) \approx \sum_k f(k\Delta t)\, g_{\Delta t}(t-k\Delta t)$',
             fontsize=13)
fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_decomp.png'))
plt.close(fig)

print("Figure 8 (signal decomposition) saved.")

# ============================================================
# 9. Convolution example 2: f1(t)=u(t)-u(t-3), f2(t)=e^{-t}u(t)
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

tau = np.linspace(-2, 6, 1000)
f1 = np.heaviside(tau, 1) - np.heaviside(tau - 3, 1)

cases = [
    (-1.0, r'$t = -1 < 0$', 'no overlap'),
    (1.5, r'$t = 1.5\ (0 < t < 3)$', 'partial overlap'),
    (4.0, r'$t = 4 > 3$', 'full overlap'),
]

for ax, (t_val, title, desc) in zip(axes, cases):
    # f2(t - tau) = e^{-(t-tau)} u(t-tau)
    f2_shifted = np.exp(-(t_val - tau)) * np.heaviside(t_val - tau, 1)

    ax.plot(tau, f1, 'b', linewidth=1.8, label=r'$f_1(\tau)$')
    ax.plot(tau, f2_shifted, 'r', linewidth=1.8, label=r'$f_2(t-\tau)$')

    # Highlight overlapping region
    overlap_start = max(0, t_val) if t_val > 0 else 0
    overlap_end = min(3, t_val) if t_val > 0 else 0
    if overlap_start < overlap_end:
        tau_ov = np.linspace(overlap_start, overlap_end, 200)
        ax.fill_between(tau_ov, 0,
                        np.minimum(np.ones_like(tau_ov), np.exp(-(t_val - tau_ov))),
                        alpha=0.25, color='purple')
        ax.text((overlap_start + overlap_end)/2, 0.25, 'overlap',
                ha='center', fontsize=10, color='purple')

    ax.set_title(title + f'  ({desc})', fontsize=11)
    ax.set_xlabel(r'$\tau$')
    ax.set_xlim(-2, 6); ax.set_ylim(-0.05, 1.15)
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5, linestyle='--', alpha=0.4)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

fig.suptitle(r'Ex2: $f_1(\tau)=u(\tau)-u(\tau-3),\  f_2(t-\tau)=e^{-(t-\tau)}u(t-\tau)$',
             fontsize=12)
fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_conv_ex2.png'))
plt.close(fig)

print("Figure 9 (convolution example 2) saved.")

# ============================================================
# 10. Convolution example 1: f(t)=u(t), h(t)=e^{-t}u(t)
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

tau = np.linspace(-2, 5, 1000)
f1 = np.heaviside(tau, 1)  # u(tau)

cases = [
    (-1.0, r'$t = -1 < 0$', 'no overlap'),
    (2.0, r'$t = 2 > 0$', 'partial overlap'),
]

for ax, (t_val, title, desc) in zip(axes, cases):
    # h(t - tau) = e^{-(t-tau)} u(t-tau)
    h_shifted = np.exp(-(t_val - tau)) * np.heaviside(t_val - tau, 1)

    ax.plot(tau, f1, 'b', linewidth=1.8, label=r'$f(\tau)=u(\tau)$')
    ax.plot(tau, h_shifted, 'r', linewidth=1.8, label=r'$h(t-\tau)=e^{-(t-\tau)}u(t-\tau)$')

    # Highlight overlapping region
    if t_val > 0:
        tau_ov = np.linspace(0, t_val, 200)
        ax.fill_between(tau_ov, 0,
                        np.minimum(np.ones_like(tau_ov), np.exp(-(t_val - tau_ov))),
                        alpha=0.25, color='purple')
        ax.text(t_val / 2, 0.3, 'overlap', ha='center', fontsize=10, color='purple')

    ax.set_title(title + f'  ({desc})', fontsize=11)
    ax.set_xlabel(r'$\tau$')
    ax.set_xlim(-2, 5); ax.set_ylim(-0.05, 1.15)
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5, linestyle='--', alpha=0.4)
    ax.legend(fontsize=8.5)
    ax.grid(True, alpha=0.3)

fig.suptitle(r'Ex1: $f(\tau)=u(\tau),\  h(t-\tau)=e^{-(t-\tau)}u(t-\tau)$', fontsize=12)
fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_conv_ex1.png'))
plt.close(fig)

print("Figure 10 (convolution example 1) saved.")
