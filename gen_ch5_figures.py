import matplotlib.pyplot as plt
import numpy as np
import os

out = '/Users/hesiqi/Desktop/note/note/images'
plt.rcParams.update({'font.family': 'serif', 'font.size': 10, 'axes.titlesize': 11,
                     'figure.dpi': 140, 'savefig.dpi': 140, 'savefig.bbox': 'tight'})

# ============================================================
# 1. ROC types — four regions in s-plane
# ============================================================
fig, axes = plt.subplots(1, 4, figsize=(14, 3.5))
titles = [r'Right-sided\n($\sigma > \sigma_0$)', r'Left-sided\n($\sigma < \sigma_0$)',
          r'Two-sided\n($\sigma_1 < \sigma < \sigma_2$)', r'Finite-length\n(entire plane)']
colors_roc = ['blue', 'red', 'purple', 'green']

for i, (ax, title, c) in enumerate(zip(axes, titles, colors_roc)):
    ax.axhline(0, color='gray', lw=0.8)
    ax.axvline(0, color='gray', lw=0.8)
    ax.set_xlim(-4, 4); ax.set_ylim(-3, 3)
    ax.set_xlabel(r'$\sigma$'); ax.set_ylabel(r'$j\omega$', fontsize=9)
    ax.set_title(title, fontsize=10)

    if i == 0:  # right-sided: sigma > sigma0 = 1
        ax.axvspan(1, 4, alpha=0.15, color=c)
        ax.axvline(1, color=c, linestyle='--', lw=1.5, label=r'$\sigma_0=1$')
        ax.legend(fontsize=8)
    elif i == 1:  # left-sided: sigma < sigma0 = -0.5
        ax.axvspan(-4, -0.5, alpha=0.15, color=c)
        ax.axvline(-0.5, color=c, linestyle='--', lw=1.5, label=r'$\sigma_0=-0.5$')
        ax.legend(fontsize=8)
    elif i == 2:  # two-sided: a < sigma < b (strip)
        ax.axvspan(0.5, 2.5, alpha=0.15, color=c)
        ax.axvline(0.5, color=c, linestyle='--', lw=1.2, label=r'$\sigma_1=0.5$')
        ax.axvline(2.5, color=c, linestyle='--', lw=1.2, label=r'$\sigma_2=2.5$')
        ax.legend(fontsize=8)
    elif i == 3:  # entire s-plane
        ax.axvspan(-4, 4, alpha=0.12, color=c)
        ax.text(0, 1.5, 'entire plane', ha='center', fontsize=10, color=c)

    ax.grid(True, alpha=0.2)

fig.suptitle('Convergence Regions (ROC) of Laplace Transform', fontsize=13, fontweight='bold')
fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_ch5_roc.png'))
plt.close(fig)

# ============================================================
# 2. Laplace vs Fourier — three cases
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))

case_data = [
    (r'$\sigma_0 > 0$', 'right', 'FT: does NOT exist', 'LT exists'),
    (r'$\sigma_0 < 0$', 'left', r'FT: $F(j\omega)=F(s)|_{s=j\omega}$', 'LT exists'),
    (r'$\sigma_0 = 0$', 'boundary', 'FT: exists (with singular term)', 'LT exists'),
]

for ax, (title, shade, ft, lt) in zip(axes, case_data):
    ax.axhline(0, color='gray', lw=1)
    ax.axvline(0, color='gray', lw=1)
    ax.set_xlim(-4, 4); ax.set_ylim(-3, 3)
    ax.set_xlabel(r'$\sigma$', fontsize=11)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.15)

    ax.text(0.3, 2.8, r'$j\omega$', fontsize=9, color='blue', alpha=0.7)

    if shade == 'right':
        ax.axvspan(1, 4, alpha=0.15, color='green')
        ax.axvline(1, color='green', linestyle='--', lw=1.5, label=r'$\sigma_0$')
        ax.plot(1, 0, 'go', markersize=8)
    elif shade == 'left':
        ax.axvspan(-4, -1, alpha=0.15, color='green')
        ax.axvline(-1, color='green', linestyle='--', lw=1.5, label=r'$\sigma_0$')
        ax.plot(-1, 0, 'go', markersize=8)
    elif shade == 'boundary':
        ax.axvspan(-4, 4, alpha=0.1, color='green')
        ax.axvline(0, color='green', linestyle='--', lw=1.5, alpha=0.5)

    ax.text(2, 2.2, ft, fontsize=12, color='red', ha='center',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax.text(2, 1.0, lt, fontsize=12, color='green', ha='center',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax.legend(fontsize=8, loc='upper left')

fig.suptitle('Laplace Transform vs Fourier Transform', fontsize=14, fontweight='bold')
fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_ch5_lt_vs_ft.png'))
plt.close(fig)

# ============================================================
# 3. s-domain RLC element models
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(13, 7))

# Row 1: time domain
td_labels = ['Resistor', 'Inductor', 'Capacitor']
td_formulas = [r'$u_R = R\,i_R$', r'$u_L = L\frac{di_L}{dt}$', r'$u_C = \frac{1}{C}\int i_C dt + u_C(0^-)$']
for ax, label, formula in zip(axes[0], td_labels, td_formulas):
    ax.text(0.5, 0.6, label, ha='center', fontsize=13, fontweight='bold')
    ax.text(0.5, 0.3, formula, ha='center', fontsize=11)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title('Time Domain', fontsize=10, color='gray')

# Row 2: s-domain
sd_formulas = [r'$U_R(s)=R\,I_R(s)$', r'$U_L(s)=sL\,I_L(s)-Li_L(0^-)$', r'$U_C(s)=\frac{1}{sC}I_C(s)+\frac{u_C(0^-)}{s}$']
for ax, label, formula in zip(axes[1], td_labels, sd_formulas):
    ax.text(0.5, 0.6, label, ha='center', fontsize=13, fontweight='bold')
    ax.text(0.5, 0.3, formula, ha='center', fontsize=10)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title('s-Domain', fontsize=10, color='gray')

fig.suptitle('RLC Element Models in Time Domain vs s-Domain', fontsize=14, fontweight='bold')
fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_ch5_rlc.png'))
plt.close(fig)

# ============================================================
# 4. Time-shift property — four cases
# ============================================================
fig, axes = plt.subplots(1, 4, figsize=(15, 3.5))
t0 = 1
t = np.linspace(-1, 4, 1000)
omega = 2*np.pi
f_orig = np.sin(omega * t)

cases = [
    (r'(a) $f(t-t_0)$', np.sin(omega * (t - t0)), 'No LT', 'red'),
    (r'(b) $f(t-t_0)u(t)$', np.sin(omega * (t - t0)) * np.heaviside(t, 1), 'No LT', 'red'),
    (r'(c) $f(t)u(t-t_0)$', np.sin(omega * t) * np.heaviside(t - t0, 1), 'No LT', 'red'),
    (r'(d) $f(t-t_0)u(t-t_0)$  OK', np.sin(omega * (t - t0)) * np.heaviside(t - t0, 1), r'$e^{-st_0}F(s)$', 'green'),
]

for ax, (title, data, result, color) in zip(axes, cases):
    ax.plot(t, data, 'b', lw=1.5)
    ax.axvline(t0, color='gray', linestyle='--', lw=0.6, alpha=0.5)
    ax.set_title(title, fontsize=10)
    ax.set_xlim(-1, 4); ax.set_ylim(-1.5, 1.5)
    ax.axhline(0, color='gray', lw=0.5)
    ax.set_xlabel('$t$')
    ax.text(0.5, 1.2, result, ha='center', fontsize=10, color=color, fontweight='bold')
    ax.grid(True, alpha=0.2)

fig.suptitle('Time-Shift Property: Only (d) is Valid for Unilateral LT', fontsize=13, fontweight='bold')
fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_ch5_timeshift.png'))
plt.close(fig)

# ============================================================
# 5. Block diagram basic elements
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(11, 3))

for ax, (title, sym) in zip(axes, [
    ('Scalar Multiplier', r'$y = a \cdot x$'),
    ('Integrator', r'$y = \int x \, dt$'),
    ('Adder', r'$y = x_1 + x_2$'),
]):
    ax.text(0.5, 0.55, sym, ha='center', va='center', fontsize=14,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
    ax.set_title(title, fontsize=11)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xticks([]); ax.set_yticks([])

fig.suptitle('Basic Block Diagram Elements', fontsize=13, fontweight='bold')
fig.tight_layout()
plt.savefig(os.path.join(out, 'xh_ch5_blocks.png'))
plt.close(fig)

# ============================================================
# 7. Triangular pulse — waveform + derivatives for LT methods
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(12, 7))

t = np.linspace(-0.5, 2.5, 1000)
# Triangular pulse
f = np.where((t >= 0) & (t < 1), t, np.where((t >= 1) & (t <= 2), 2 - t, 0))
# f'(t) = u(t) - 2u(t-1) + u(t-2)
fp = np.heaviside(t, 1) - 2*np.heaviside(t-1, 1) + np.heaviside(t-2, 1)
# f''(t) = δ(t) - 2δ(t-1) + δ(t-2)

# --- Top-left: f(t) triangular pulse ---
ax = axes[0, 0]
ax.plot(t, f, 'b', lw=2); ax.fill_between(t, f, alpha=0.08, color='b')
ax.set_title(r'$f(t)$: triangular pulse', fontsize=12)
ax.set_xlabel('$t$'); ax.set_xlim(-0.5, 2.5); ax.set_ylim(-0.1, 1.3)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)
for x in [0, 1, 2]:
    ax.axvline(x, color='red', linestyle='--', lw=0.5, alpha=0.4)

# --- Top-right: decomposition into ramps ---
ax = axes[0, 1]
t_plot = np.linspace(-0.5, 2.5, 1000)
r1 = np.maximum(t_plot, 0)  # t·u(t)
r2 = -2 * np.maximum(t_plot - 1, 0)  # -2(t-1)u(t-1)
r3 = np.maximum(t_plot - 2, 0)  # (t-2)u(t-2)
ax.plot(t_plot, r1, 'b--', lw=1, alpha=0.6, label=r'$t\,u(t)$')
ax.plot(t_plot, r2, 'r--', lw=1, alpha=0.6, label=r'$-2(t-1)u(t-1)$')
ax.plot(t_plot, r3, 'g--', lw=1, alpha=0.6, label=r'$(t-2)u(t-2)$')
ax.plot(t_plot, r1+r2+r3, 'k', lw=2, label='sum')
ax.set_title(r'Method 2: $f=t u(t)-2(t-1)u(t-1)+(t-2)u(t-2)$', fontsize=11)
ax.set_xlabel('$t$'); ax.set_xlim(-0.5, 2.5); ax.set_ylim(-2, 1.5)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)
ax.legend(fontsize=7.5, loc='lower left')

# --- Bottom-left: f'(t) ---
ax = axes[1, 0]
ax.plot(t, fp, 'b', lw=2)
ax.fill_between(t[t<1], fp[t<1], alpha=0.08, color='b')
ax.fill_between(t[(t>=1)&(t<2)], fp[(t>=1)&(t<2)], alpha=0.08, color='r')
ax.set_title(r"$f'(t) = u(t) - 2u(t-1) + u(t-2)$", fontsize=12)
ax.set_xlabel('$t$'); ax.set_xlim(-0.5, 2.5); ax.set_ylim(-2.5, 1.5)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)

# --- Bottom-right: f''(t) impulse train ---
ax = axes[1, 1]
ax.annotate('', xy=(0, 1), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='b', lw=2.5))
ax.text(0.2, 0.55, '1', fontsize=11, color='b')
ax.annotate('', xy=(1, -2), xytext=(1, 0), arrowprops=dict(arrowstyle='->', color='r', lw=2.5))
ax.text(1.2, -1.5, '-2', fontsize=11, color='r')
ax.annotate('', xy=(2, 1), xytext=(2, 0), arrowprops=dict(arrowstyle='->', color='g', lw=2.5))
ax.text(2.2, 0.55, '1', fontsize=11, color='g')
ax.set_title(r"$f''(t) = \delta(t) - 2\delta(t-1) + \delta(t-2)$", fontsize=12)
ax.set_xlabel('$t$'); ax.set_xlim(-0.5, 2.5); ax.set_ylim(-2.5, 1.5)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.2)

fig.suptitle('Example 2: Triangular Pulse — Four LT Methods', fontsize=14, fontweight='bold')
fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_ch5_triangle_lt.png'))
plt.close(fig)

print("Figure 7 (triangular pulse) saved.")

# ============================================================
# 6. Bilateral ROC example — strip of convergence
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

# Left: b > a — ROC exists
ax = axes[0]
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
a, b_val = 1, 3
ax.axvspan(a, b_val, alpha=0.15, color='purple')
ax.axvline(a, color='blue', linestyle='--', lw=1.5, label=r'$\sigma=a$')
ax.axvline(b_val, color='red', linestyle='--', lw=1.5, label=r'$\sigma=b$')
ax.plot(a, 0, 'bx', markersize=10, label=r'pole at $s=a$')
ax.plot(b_val, 0, 'rx', markersize=10, label=r'pole at $s=b$')
ax.set_title(r'$b > a$: ROC exists  ($a<\sigma<b$)', fontsize=12)
ax.set_xlabel(r'$\sigma$'); ax.set_ylabel(r'$j\omega$')
ax.set_xlim(-1, 5); ax.set_ylim(-3, 3)
ax.text(2, 2, 'ROC: strip', ha='center', fontsize=11, color='purple')
ax.legend(fontsize=8, loc='lower left')
ax.grid(True, alpha=0.2)

# Right: b < a — no ROC
ax = axes[1]
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
a, b_val = 2, 0.5
ax.axvline(a, color='blue', linestyle='--', lw=1.5, label=r'$\sigma=a$')
ax.axvline(b_val, color='red', linestyle='--', lw=1.5, label=r'$\sigma=b$')
ax.plot(a, 0, 'bx', markersize=10, label=r'pole at $s=a$')
ax.plot(b_val, 0, 'rx', markersize=10, label=r'pole at $s=b$')
ax.set_title(r'$b < a$: NO ROC  (empty intersection)', fontsize=12)
ax.set_xlabel(r'$\sigma$'); ax.set_ylabel(r'$j\omega$')
ax.set_xlim(-1, 5); ax.set_ylim(-3, 3)
ax.annotate(r'$\sigma>b$', xy=(1.5, 2), fontsize=9, color='red', alpha=0.6)
ax.annotate(r'$\sigma<a$', xy=(3.5, 2), fontsize=9, color='blue', alpha=0.6)
ax.annotate('No overlap!', xy=(2, -1.5), ha='center', fontsize=11, color='red')
ax.legend(fontsize=8, loc='lower left')
ax.grid(True, alpha=0.2)

fig.suptitle(r'Bilateral LT ROC: $f(t)=e^{at}u(t)+e^{bt}u(-t)$', fontsize=13, fontweight='bold')
fig.tight_layout()
plt.savefig(os.path.join(out, 'xh_ch5_bilateral_roc.png'))
plt.close(fig)

print("Figure 6 (bilateral ROC) saved.")

# ============================================================
# Chapter 6 figures
# ============================================================

# --- Ch6-1: Pole position → h(t) waveform mapping ---
fig, axes = plt.subplots(2, 3, figsize=(15, 9))

def add_splane_inset(ax, poles, color='r'):
    """Add an s-plane inset in the upper-right corner with labeled pole positions"""
    inset = ax.inset_axes([0.55, 0.55, 0.42, 0.43])
    inset.axhline(0, color='gray', lw=0.8)
    inset.axvline(0, color='gray', lw=0.8)
    inset.set_xlim(-4, 4); inset.set_ylim(-5.5, 5.5)
    inset.set_xticks([]); inset.set_yticks([])
    # use fill_between to cover full y range
    y_vals = np.linspace(-5.5, 5.5, 10)
    inset.fill_betweenx(y_vals, -4, 0, alpha=0.07, color='green')
    inset.fill_betweenx(y_vals, 0, 4, alpha=0.07, color='red')
    for p in poles:
        inset.plot(p[0], p[1], 'x', color=color, markersize=14, markeredgewidth=2.5)
    inset.text(3.5, -0.8, r'$\sigma$', fontsize=8, color='gray')
    inset.text(0.3, 5.0, r'$j\omega$', fontsize=8, color='gray')
    inset.set_title('s-plane', fontsize=8, color='gray')

# (a) Left-half real pole: e^{-αt}u(t)
ax = axes[0, 0]
t = np.linspace(0, 5, 500)
ax.plot(t, np.exp(-1.5*t), 'b', lw=2)
ax.set_title(r'(a) Left real: $e^{-\alpha t}u(t)$', fontsize=10)
ax.set_xlabel('$t$'); ax.set_xlim(0, 5); ax.set_ylim(-0.1, 1.2)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)
ax.text(0.5, 0.8, r'$\to 0$', fontsize=11, color='green')
add_splane_inset(ax, [(-1.5, 0)], 'r')

# (b) Left-half complex conjugate: e^{-αt}sin(βt)
ax = axes[0, 1]
t = np.linspace(0, 8, 500)
ax.plot(t, np.exp(-0.5*t)*np.sin(3*t), 'b', lw=1.5)
ax.set_title(r'(b) Left complex: $e^{-\alpha t}\sin(\beta t)$', fontsize=10)
ax.set_xlabel('$t$'); ax.set_xlim(0, 8); ax.set_ylim(-1.1, 1.1)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)
ax.text(0.5, 0.7, r'$\to 0$', fontsize=11, color='green')
add_splane_inset(ax, [(-0.5, 3), (-0.5, -3)], 'r')

# (c) jω-axis single pole: sin(βt) (steady)
ax = axes[0, 2]
t = np.linspace(0, 8, 500)
ax.plot(t, np.sin(3*t), 'b', lw=1.5)
ax.set_title(r'(c) $j\omega$ single: $\sin(\beta t)$', fontsize=10)
ax.set_xlabel('$t$'); ax.set_xlim(0, 8); ax.set_ylim(-1.3, 1.3)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)
ax.text(0.5, 0.9, 'steady', fontsize=11, color='orange')
add_splane_inset(ax, [(0, 3), (0, -3)], 'orange')

# (d) jω-axis double pole: t·sin(βt) (growing)
ax = axes[1, 0]
t = np.linspace(0, 8, 500)
ax.plot(t, 0.2*t*np.sin(3*t), 'b', lw=1.5)
ax.set_title(r'(d) $j\omega$ double: $t\sin(\beta t)$', fontsize=10)
ax.set_xlabel('$t$'); ax.set_xlim(0, 8); ax.set_ylim(-2, 2)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)
ax.text(0.5, 1.5, r'$\to\infty$', fontsize=11, color='red')
add_splane_inset(ax, [(0, 3.2), (0, 2.8), (0, -2.8), (0, -3.2)], 'red')  # double pole

# (e) Right-half real pole: e^{αt}u(t) (diverging)
ax = axes[1, 1]
t = np.linspace(0, 3, 500)
ax.plot(t, np.exp(1.5*t), 'b', lw=2)
ax.set_title(r'(e) Right real: $e^{\alpha t}u(t)$', fontsize=10)
ax.set_xlabel('$t$'); ax.set_xlim(0, 3); ax.set_ylim(-1, 20)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)
ax.text(0.3, 15, r'$\to\infty$', fontsize=11, color='red')
add_splane_inset(ax, [(1.5, 0)], 'r')

# (f) Right-half complex: e^{αt}sin(βt) (diverging oscillation)
ax = axes[1, 2]
t = np.linspace(0, 3, 500)
ax.plot(t, np.exp(1.2*t)*np.sin(5*t), 'b', lw=1.5)
ax.set_title(r'(f) Right complex: $e^{\alpha t}\sin(\beta t)$', fontsize=10)
ax.set_xlabel('$t$'); ax.set_xlim(0, 3); ax.set_ylim(-15, 15)
ax.axhline(0, color='gray', lw=0.5); ax.grid(True, alpha=0.3)
ax.text(0.3, 12, r'$\to\infty$', fontsize=11, color='red')
add_splane_inset(ax, [(1.2, 5), (1.2, -5)], 'r')

fig.suptitle('Pole Position → $h(t)$ Waveform  (Ch6.2)', fontsize=14, fontweight='bold')
fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_ch6_pole_h.png'))
plt.close(fig)

# --- Ch6-2: Vector method for frequency response ---
fig, ax = plt.subplots(figsize=(8, 6))
# s-plane with axes
ax.axhline(0, color='gray', lw=1)
ax.axvline(0, color='gray', lw=1)
ax.set_xlim(-5, 2); ax.set_ylim(-4, 4)
ax.set_xlabel(r'$\sigma$', fontsize=12); ax.set_ylabel(r'$j\omega$', fontsize=12)

# Poles (×) and zeros (○)
# Example: one zero at origin, one pole at -1
zero = (0, 0)
pole = (-1.5, 0)
ax.plot(zero[0], zero[1], 'ko', markersize=12, markerfacecolor='none', markeredgewidth=2)
ax.text(zero[0]+0.2, zero[1]+0.3, 'o (zero)', fontsize=10)
ax.plot(pole[0], pole[1], 'rx', markersize=14, markeredgewidth=2)
ax.text(pole[0]+0.2, pole[1]+0.3, r'$\times$ (pole)', fontsize=10, color='red')

# jω point at ω=2
jomega = (0, 2.5)
ax.plot(jomega[0], jomega[1], 'b.', markersize=10)
ax.text(jomega[0]+0.15, jomega[1]+0.1, r'$j\omega$', fontsize=11, color='blue')

# Vector from zero to jω: B∠β
ax.annotate('', xy=jomega, xytext=zero,
            arrowprops=dict(arrowstyle='->', color='green', lw=2))
mid_b = ((zero[0]+jomega[0])/2 + 0.2, (zero[1]+jomega[1])/2)
ax.text(mid_b[0], mid_b[1], r'$B e^{j\beta}$', fontsize=10, color='green')

# Vector from pole to jω: A∠α
ax.annotate('', xy=jomega, xytext=pole,
            arrowprops=dict(arrowstyle='->', color='red', lw=2))
mid_a = ((pole[0]+jomega[0])/2 - 0.4, (pole[1]+jomega[1])/2)
ax.text(mid_a[0], mid_a[1], r'$A e^{j\alpha}$', fontsize=10, color='red')

ax.set_title(r'Vector Method: $H(j\omega)=H_0\frac{B}{A}e^{j(\beta-\alpha)}$', fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.2)
fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_ch6_vector.png'))
plt.close(fig)

# --- Ch6-3: RC high-pass filter |H(jω)| ---
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
tau = 1  # RC
w = np.logspace(-2, 2, 500)
Hmag = w / np.sqrt(w**2 + 1/tau**2)
phi = np.pi/2 - np.arctan(w*tau)

axes[0].semilogx(w, Hmag, 'b', lw=2)
axes[0].axhline(1/np.sqrt(2), color='gray', linestyle='--', lw=0.6, alpha=0.5)
axes[0].axvline(1/tau, color='red', linestyle='--', lw=0.6, alpha=0.5, label=r'$\omega_c=1/RC$')
axes[0].set_title(r'$|H(j\omega)|$', fontsize=12)
axes[0].set_xlabel(r'$\omega$'); axes[0].set_ylabel(r'$|H|$')
axes[0].set_ylim(-0.05, 1.1)
axes[0].axhline(0, color='gray', lw=0.5); axes[0].grid(True, alpha=0.3)
axes[0].legend(fontsize=8)

axes[1].semilogx(w, phi, 'r', lw=2)
axes[1].axhline(np.pi/4, color='gray', linestyle='--', lw=0.6, alpha=0.5)
axes[1].axvline(1/tau, color='red', linestyle='--', lw=0.6, alpha=0.5)
axes[1].set_title(r'$\varphi(\omega)$', fontsize=12)
axes[1].set_xlabel(r'$\omega$'); axes[1].set_ylabel(r'$\varphi$')
axes[1].axhline(0, color='gray', lw=0.5); axes[1].grid(True, alpha=0.3)

fig.suptitle(r'RC High-Pass Filter: $H(s)=\frac{s}{s+1/RC}$', fontsize=13, fontweight='bold')
fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_ch6_rc_hp.png'))
plt.close(fig)

# --- Ch6-4: Stability regions in s-plane ---
fig, ax = plt.subplots(figsize=(8, 6))
ax.axhline(0, color='gray', lw=1)
ax.axvline(0, color='gray', lw=1)
ax.set_xlim(-5, 3); ax.set_ylim(-4, 4)
ax.set_xlabel(r'$\sigma$', fontsize=12); ax.set_ylabel(r'$j\omega$', fontsize=12)

# Left half-plane: stable
ax.axvspan(-5, 0, alpha=0.1, color='green')
ax.text(-2.5, 3, 'STABLE', fontsize=14, color='green', ha='center', fontweight='bold',
        alpha=0.5)
ax.text(-2.5, 2, r'Re$[p_i] < 0$', fontsize=10, color='green', ha='center')

# Right half-plane: unstable
ax.axvspan(0, 3, alpha=0.1, color='red')
ax.text(1.5, 3, 'UNSTABLE', fontsize=14, color='red', ha='center', fontweight='bold',
        alpha=0.5)
ax.text(1.5, 2, r'Re$[p_i] > 0$', fontsize=10, color='red', ha='center')

# jω axis: critically stable
ax.axvline(0, color='orange', lw=3, alpha=0.5, label=r'Re$[p_i]=0$ (critical)')
ax.text(0.3, -0.3, 'critical', fontsize=9, color='orange', rotation=90)

# Example poles
# Stable pole
ax.plot(-2, 1.5, 'go', markersize=10)
ax.text(-2+0.2, 1.5, 'stable pole', fontsize=9, color='green')
# Unstable pole
ax.plot(1.5, -1.5, 'ro', markersize=10)
ax.text(1.5+0.2, -1.5, 'unstable pole', fontsize=9, color='red')
# Critical pole (single, on jω)
ax.plot(0, 2.5, 'o', color='orange', markersize=10)
ax.text(0+0.2, 2.5, 'crit. pole (single)', fontsize=9, color='orange')

ax.set_title('Stability Regions in s-Plane', fontsize=13, fontweight='bold')
ax.legend(fontsize=9, loc='lower right')
ax.grid(True, alpha=0.2)
fig.tight_layout()
fig.savefig(os.path.join(out, 'xh_ch6_stability.png'))
plt.close(fig)

print("Chapter 6 figures saved.")

print("Chapter 5 figures saved.")
