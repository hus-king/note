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
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
cases = [
    (r'$\sigma_0 > 0$', 'FT: NOT exist', 'LT exists'),
    (r'$\sigma_0 < 0$', r'FT: $F(s)\vert_{s=j\omega}$', 'LT exists'),
    (r'$\sigma_0 = 0$', r'FT: $F(s)|_{s=j\omega} +$ singular', 'LT exists'),
]
for ax, (title, ft, lt) in zip(axes, cases):
    ax.axhline(0, color='gray', lw=0.8)
    ax.axvline(0, color='gray', lw=0.8)
    ax.set_xlim(-4, 4); ax.set_ylim(-3, 3)
    ax.set_xlabel(r'$\sigma$'); ax.set_ylabel(r'$j\omega$', fontsize=9)
    ax.set_title(title, fontsize=11)
    ax.text(1.5, 2, ft, fontsize=10, color='red', ha='center')
    ax.text(1.5, 1.2, lt, fontsize=10, color='green', ha='center')
    # mark jω axis
    ax.axvline(0, color='blue', lw=0.5, alpha=0.3)
    ax.text(-0.3, 2.8, r'$j\omega$', fontsize=9, color='blue', alpha=0.6)
    ax.grid(True, alpha=0.2)

fig.suptitle('Laplace Transform vs Fourier Transform', fontsize=13, fontweight='bold')
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

print("Chapter 5 figures saved.")
