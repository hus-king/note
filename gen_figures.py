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

out = '/Users/hesiqi/Desktop/note/note/images'

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

# ============================================================
# 11. Triangular pulse wave for Fourier series example
# ============================================================
fig, ax = plt.subplots(figsize=(10, 4))

T = 4
t = np.linspace(-6, 6, 2000)

# Define periodic triangular wave: period T=4
# f(t) = t+2 for -2 < t < 0, f(t) = -t+2 for 0 < t < 2, repeat
def triangle_wave(t, T=4):
    t_mod = t % T          # map into [0, T)
    t_centered = t_mod - T/2  # map into [-2, 2)
    return np.where(t_centered <= 0, t_centered + 2, -t_centered + 2)

f = triangle_wave(t)

# Plot
ax.plot(t, f, 'b', linewidth=1.8)
ax.set_title(r'Periodic Triangular Pulse Wave  ($T=4$)', fontsize=13)
ax.set_xlabel('$t$')
ax.set_ylabel('$f(t)$')
ax.set_xlim(-6, 6)
ax.set_ylim(-0.2, 2.5)
ax.axhline(0, color='gray', linewidth=0.5)
ax.axvline(0, color='gray', linewidth=0.5)
ax.grid(True, alpha=0.3)

# Mark period
ax.annotate('', xy=(0, 2.3), xytext=(4, 2.3),
            arrowprops=dict(arrowstyle='<->', color='red', lw=1.5))
ax.text(2, 2.4, r'$T=4$', ha='center', fontsize=12, color='red')

# Mark key points
for x in [-4, -2, 0, 2, 4]:
    ax.axvline(x, color='gray', linestyle='--', linewidth=0.5, alpha=0.4)

fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_triangle_wave.png'))
plt.close(fig)

print("Figure 11 (triangular wave) saved.")

# ============================================================
# 12. Spectrum of triangular pulse wave
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Harmonic orders (x-axis: harmonic number n)
n_vals = np.array([0, 1, 3, 5, 7, 9])

# Amplitudes: DC=1, A_n = 8/(pi^2 * n^2) for odd n
A_vals = np.array([1.0, 8/np.pi**2, 8/(np.pi**2 * 9), 8/(np.pi**2 * 25),
                   8/(np.pi**2 * 49), 8/(np.pi**2 * 81)])

# Phases: all zero for this even-signal cosine expansion
phi_vals = np.zeros_like(n_vals, dtype=float)

# --- Amplitude spectrum ---
markerline, stemlines, baseline = ax1.stem(n_vals, A_vals, linefmt='b-', markerfmt='bo', basefmt='k-')
stemlines.set_linewidth(1.5)
markerline.set_markersize(8)
ax1.set_title('Amplitude Spectrum  $A_n$', fontsize=12)
ax1.set_xlabel(r'$n$  (harmonic order)')
ax1.set_ylabel(r'$A_n$')
ax1.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
ax1.set_xlim(-0.3, 9.5)
ax1.set_ylim(-0.02, 1.1)
ax1.axhline(0, color='gray', linewidth=0.5)
ax1.grid(True, alpha=0.3)
ax1.text(6.5, 0.6, r'$\propto \frac{1}{n^2}$', fontsize=11, color='red')

# --- Phase spectrum ---
ax2.stem(n_vals, phi_vals, linefmt='b-', markerfmt='bo', basefmt='k-')
ax2.set_title('Phase Spectrum  $\\varphi_n$', fontsize=12)
ax2.set_xlabel(r'$n$  (harmonic order)')
ax2.set_ylabel(r'$\varphi_n$')
ax2.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
ax2.set_xlim(-0.3, 9.5)
ax2.set_ylim(-0.5, 0.5)
ax2.axhline(0, color='gray', linewidth=0.5)
ax2.grid(True, alpha=0.3)

fig.suptitle('Spectrum of Triangular Pulse Wave', fontsize=13)
fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_triangle_spectrum.png'))
plt.close(fig)

print("Figure 12 (triangular wave spectrum) saved.")

# ============================================================
# 13-16. FT Table figures: waveform + spectrum pairs
# ============================================================

# --- 13. Singular functions: delta, step, sgn, DC ---
fig, axes = plt.subplots(4, 2, figsize=(12, 12))

# (a) delta(t) -> 1
t = np.linspace(-3, 3, 1000)
ax = axes[0, 0]
ax.annotate('', xy=(0, 1), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='b', lw=2))
ax.text(0.3, 0.7, '1', fontsize=12, color='b')
ax.set_title(r'$\delta(t)$', fontsize=11)
ax.set_xlim(-3, 3); ax.set_ylim(-0.2, 1.5)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)
ax.set_xlabel('$t$')
ax = axes[0, 1]
ax.axhline(1, color='b', lw=1.8)
ax.set_title(r'$F(j\omega)=1$', fontsize=11)
ax.set_xlim(-3, 3); ax.set_ylim(-0.2, 1.8)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)
ax.set_xlabel(r'$\omega$')

# (b) u(t) -> πδ(ω) + 1/(jω)
ax = axes[1, 0]
ax.plot(t, np.heaviside(t, 1), 'b', lw=1.8)
ax.set_title(r'$u(t)$', fontsize=11)
ax.set_xlim(-3, 3); ax.set_ylim(-0.2, 1.5)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)
ax.set_xlabel('$t$')
ax = axes[1, 1]
ax.annotate('', xy=(0, 1), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='b', lw=2))
ax.text(0.4, 0.7, r'$\pi$', fontsize=11, color='b')
w = np.linspace(-3, 3, 1000); w = w[w != 0]
ax.plot(w, -1/w, 'r--', lw=1, alpha=0.6, label=r'imag: $-1/\omega$')
ax.set_title(r'$\pi\delta(\omega)+1/j\omega$', fontsize=11)
ax.set_xlim(-3, 3); ax.set_ylim(-5, 5)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)
ax.legend(fontsize=8); ax.set_xlabel(r'$\omega$')

# (c) sgn(t) -> 2/(jω)
ax = axes[2, 0]
ax.plot(t[t<0], -np.ones_like(t[t<0]), 'b', lw=1.8)
ax.plot(t[t>0], np.ones_like(t[t>0]), 'b', lw=1.8)
ax.plot([0, 0], [-1, 1], 'b', lw=1.8)
ax.set_title(r'$\mathrm{sgn}(t)$', fontsize=11)
ax.set_xlim(-3, 3); ax.set_ylim(-1.5, 1.5)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)
ax.set_xlabel('$t$')
ax = axes[2, 1]
w = np.linspace(-3, 3, 1000); w = w[w != 0]
ax.plot(w, -2/w, 'r', lw=1.8, label=r'imag: $-2/\omega$')
ax.set_title(r'$2/j\omega$  (imaginary odd)', fontsize=11)
ax.set_xlim(-3, 3); ax.set_ylim(-8, 8)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)
ax.legend(fontsize=8); ax.set_xlabel(r'$\omega$')

# (d) DC 1 -> 2πδ(ω)
ax = axes[3, 0]
ax.axhline(1, color='b', lw=1.8)
ax.set_title(r'$1$  (DC)', fontsize=11)
ax.set_xlim(-3, 3); ax.set_ylim(-0.2, 1.8)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)
ax.set_xlabel('$t$')
ax = axes[3, 1]
ax.annotate('', xy=(0, 1), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='b', lw=2))
ax.text(0.4, 0.7, r'$2\pi$', fontsize=11, color='b')
ax.set_title(r'$2\pi\delta(\omega)$', fontsize=11)
ax.set_xlim(-3, 3); ax.set_ylim(-0.2, 2)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)
ax.set_xlabel(r'$\omega$')

fig.suptitle('FT Table: Singular Functions  (1-4)', fontsize=14, fontweight='bold')
fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_ft_table_singular.png'))
plt.close(fig)

# --- 14. Gate function: rectangular pulse <-> Sa ---
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
tau = 2
t = np.linspace(-4, 4, 1000)
f = np.heaviside(t + tau/2, 1) - np.heaviside(t - tau/2, 1)
ax = axes[0]
ax.plot(t, f, 'b', lw=1.8)
ax.fill_between(t, f, alpha=0.15, color='b')
ax.set_title(r'Rectangular pulse  $G_\tau(t)$  ($\tau=2$)', fontsize=11)
ax.set_xlabel('$t$'); ax.set_xlim(-3, 3); ax.set_ylim(-0.2, 1.5)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)

w = np.linspace(-10, 10, 2000)
F = tau * np.sinc(w * tau / 2 / np.pi)  # numpy sinc(x)=sin(πx)/(πx)
ax = axes[1]
ax.plot(w, F, 'r', lw=1.8)
ax.set_title(r'Spectrum  $\tau\,\mathrm{Sa}(\omega\tau/2)$', fontsize=11)
ax.set_xlabel(r'$\omega$'); ax.set_xlim(-10, 10)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)

fig.suptitle('FT Table: Rectangular Pulse (Gate)  (No.13)', fontsize=14, fontweight='bold')
fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_ft_table_gate.png'))
plt.close(fig)

# --- 15. Triangular pulse <-> Sa^2 ---
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
tau = 3
t = np.linspace(-5, 5, 1000)
f = np.maximum(1 - np.abs(t)/tau, 0)
ax = axes[0]
ax.plot(t, f, 'b', lw=1.8)
ax.fill_between(t, f, alpha=0.15, color='b')
ax.set_title(r'Triangular pulse  ($\tau=3$)', fontsize=11)
ax.set_xlabel('$t$'); ax.set_xlim(-5, 5); ax.set_ylim(-0.2, 1.3)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)

w = np.linspace(-10, 10, 2000)
F = tau * (np.sinc(w * tau / 2 / np.pi))**2
ax = axes[1]
ax.plot(w, F, 'r', lw=1.8)
ax.set_title(r'Spectrum  $\tau[\mathrm{Sa}(\omega\tau/2)]^2$', fontsize=11)
ax.set_xlabel(r'$\omega$'); ax.set_xlim(-10, 10)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)

fig.suptitle('FT Table: Triangular Pulse  (No.17)', fontsize=14, fontweight='bold')
fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_ft_table_triangle.png'))
plt.close(fig)

# --- 16. cos ω₀t and sin ω₀t ---
fig, axes = plt.subplots(2, 2, figsize=(10, 7))
omega0 = 2
t = np.linspace(-np.pi, np.pi, 1000)
# cos
ax = axes[0, 0]
ax.plot(t, np.cos(omega0 * t), 'b', lw=1.5)
ax.set_title(r'$\cos\omega_0 t$  ($\omega_0=2$)', fontsize=11)
ax.set_xlabel('$t$'); ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-1.5, 1.5)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)
ax = axes[0, 1]
ax.annotate('', xy=(-omega0, 0.8), xytext=(-omega0, 0), arrowprops=dict(arrowstyle='->', color='b', lw=2))
ax.annotate('', xy=(omega0, 0.8), xytext=(omega0, 0), arrowprops=dict(arrowstyle='->', color='b', lw=2))
ax.text(-omega0+0.15, 0.65, r'$\pi$', fontsize=10, color='b')
ax.text(omega0+0.15, 0.65, r'$\pi$', fontsize=10, color='b')
ax.set_title(r'$\pi[\delta(\omega+\omega_0)+\delta(\omega-\omega_0)]$', fontsize=11)
ax.set_xlim(-5, 5); ax.set_ylim(-0.2, 1.2)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)
ax.set_xlabel(r'$\omega$')
# sin
ax = axes[1, 0]
ax.plot(t, np.sin(omega0 * t), 'b', lw=1.5)
ax.set_title(r'$\sin\omega_0 t$  ($\omega_0=2$)', fontsize=11)
ax.set_xlabel('$t$'); ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-1.5, 1.5)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)
ax = axes[1, 1]
# sin spectrum: jπ[δ(ω+ω0) - δ(ω-ω0)] = imaginary odd
ax.annotate('', xy=(-omega0, -0.8), xytext=(-omega0, 0), arrowprops=dict(arrowstyle='->', color='r', lw=2))
ax.annotate('', xy=(omega0, 0.8), xytext=(omega0, 0), arrowprops=dict(arrowstyle='->', color='b', lw=2))
ax.text(-omega0+0.15, -0.95, r'$-j\pi$', fontsize=10, color='r')
ax.text(omega0+0.15, 0.65, r'$+j\pi$', fontsize=10, color='b')
ax.set_title(r'$j\pi[\delta(\omega+\omega_0)-\delta(\omega-\omega_0)]$', fontsize=11)
ax.set_xlim(-5, 5); ax.set_ylim(-1.2, 1.2)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)
ax.set_xlabel(r'$\omega$')

fig.suptitle('FT Table: Sinusoidal Signals  (No.8-9)', fontsize=14, fontweight='bold')
fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_ft_table_sinusoid.png'))
plt.close(fig)

print("Figures 13-16 (FT table) saved.")
