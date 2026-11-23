import matplotlib; matplotlib.use("Agg")
matplotlib.rcParams["font.family"]="sans-serif"
matplotlib.rcParams["font.sans-serif"]=["Noto Sans CJK SC"]+list(matplotlib.rcParams["font.sans-serif"])
matplotlib.rcParams["savefig.transparent"]=False

import matplotlib.pyplot as plt
import numpy as np

# Create figure
fig, ax = plt.subplots(figsize=(8.8, 6.2), dpi=200)
ax.set_xlim(0, 10)
ax.set_ylim(0, 7.0)
ax.axis("off")

# Colors
c_a = "#D9381E"  # Red for Phase A
c_b = "#2B7A0B"  # Green for Phase B
c_c = "#1E56A0"  # Blue for Phase C
c_dark = "#1E293B"

# Title
ax.text(5.0, 6.6, "三次谐波为什么同相位", ha="center", va="center", fontsize=16, fontweight="bold", color="#0F172A")

# ==================== Upper: Fundamental (基波) ====================
# Left label card
ax.text(0.95, 4.95, "基波", ha="center", va="center", fontsize=14, fontweight="bold", color="#1D3557", 
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#EBF2FA", edgecolor="#90B4CE", lw=1.2))

# Center point for 3-phase vectors
orig_x, orig_y = 3.25, 4.75
r = 1.35

# Phase A: 90 deg (Up)
ax.annotate("", xy=(orig_x, orig_y + r), xytext=(orig_x, orig_y),
            arrowprops=dict(arrowstyle="-|>", color=c_a, lw=2.8, mutation_scale=16))
ax.text(orig_x, orig_y + r + 0.12, r"$A$", ha="center", va="bottom", fontsize=13, fontweight="bold", color=c_a)

# Phase B: -30 deg (Right-down: 90 - 120 = -30)
bx = orig_x + r * np.cos(np.radians(-30))
by = orig_y + r * np.sin(np.radians(-30))
ax.annotate("", xy=(bx, by), xytext=(orig_x, orig_y),
            arrowprops=dict(arrowstyle="-|>", color=c_b, lw=2.8, mutation_scale=16))
ax.text(bx + 0.14, by - 0.08, r"$B$", ha="left", va="top", fontsize=13, fontweight="bold", color=c_b)

# Phase C: 210 deg (Left-down: 90 + 120 = 210)
cx = orig_x + r * np.cos(np.radians(210))
cy = orig_y + r * np.sin(np.radians(210))
ax.annotate("", xy=(cx, cy), xytext=(orig_x, orig_y),
            arrowprops=dict(arrowstyle="-|>", color=c_c, lw=2.8, mutation_scale=16))
ax.text(cx - 0.14, cy - 0.08, r"$C$", ha="right", va="top", fontsize=13, fontweight="bold", color=c_c)

# Central dot
ax.plot(orig_x, orig_y, "o", color="#333333", markersize=5)

# Arc indicators for 120°
r_arc = 0.52
def draw_arc(th1, th2):
    th = np.linspace(np.radians(th1), np.radians(th2), 30)
    ax.plot(orig_x + r_arc * np.cos(th), orig_y + r_arc * np.sin(th), color="#94A3B8", lw=1.2, ls=":")

draw_arc(-30, 90)
draw_arc(90, 210)
draw_arc(210, 330)

# 120° labels near the arcs
ax.text(orig_x + 0.48, orig_y + 0.42, r"$120^\circ$", fontsize=9.5, color="#64748B")
ax.text(orig_x - 0.68, orig_y + 0.42, r"$120^\circ$", fontsize=9.5, color="#64748B")
ax.text(orig_x, orig_y - 0.72, r"$120^\circ$", ha="center", fontsize=9.5, color="#64748B")

# Upper Right Label / Explanation Card
fund_box_text = (
    r"$1 \times 120^\circ = 120^\circ$" + "\n\n"
    "• 三支从同一点出发，互差 120°\n"
    "• 对称三相基波矢量和为零"
)
ax.text(5.05, 4.95, fund_box_text, ha="left", va="center", fontsize=11, color=c_dark, linespacing=1.45,
        bbox=dict(boxstyle="round,pad=0.6", facecolor="#F8FAFC", edgecolor="#CBD5E1", lw=1.2))

# Dividing line
ax.plot([0.5, 9.5], [3.65, 3.65], color="#E2E8F0", lw=1.2, linestyle="--")

# ==================== Lower: 3rd Harmonic (三次谐波) ====================
# Left label card
ax.text(0.95, 2.3, "三次谐波", ha="center", va="center", fontsize=14, fontweight="bold", color="#7C2D12",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#FFEDD5", edgecolor="#FDBA74", lw=1.2))

# Three parallel arrows shifted slightly horizontally
xs = [2.45, 3.25, 4.05]
phases = [(r"$A$", c_a), (r"$B$", c_b), (r"$C$", c_c)]
h_len = 1.35
base_y = 1.6

for x, (p_name, col) in zip(xs, phases):
    ax.annotate("", xy=(x, base_y + h_len), xytext=(x, base_y),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=2.8, mutation_scale=16))
    ax.text(x, base_y + h_len + 0.12, p_name, ha="center", va="bottom", fontsize=13, fontweight="bold", color=col)
    ax.plot(x, base_y, "o", color=col, markersize=4.5)

# Harmonic explanation text
harm_box_text = (
    r"$3 \times 120^\circ = 360^\circ$" + "\n\n"
    "• 回到同向，三支重合相干\n"
    "• 横向略错开以便看清是三支，全部同向"
)
ax.text(5.05, 2.3, harm_box_text, ha="left", va="center", fontsize=11, color=c_dark, linespacing=1.45,
        bbox=dict(boxstyle="round,pad=0.6", facecolor="#FFFDF9", edgecolor="#FED7AA", lw=1.2))

# ==================== Bottom: Key Takeaway ====================
bottom_text = "所以三次谐波属于零序分量；零序通路（如中性线、三角形接法）决定它流不流。"
ax.text(5.0, 0.6, bottom_text, ha="center", va="center", fontsize=11.5, fontweight="bold", color="#991B1B",
        bbox=dict(boxstyle="round,pad=0.6", facecolor="#FEF2F2", edgecolor="#FCA5A5", lw=1.5))

plt.tight_layout()
plt.savefig("/mnt/hdd/kimicode-projects/multisim-mcp/deliverables/figures-batch4/fig-ge-06.png", dpi=200)
