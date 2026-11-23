import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["Noto Sans CJK SC"] + list(matplotlib.rcParams["font.sans-serif"])
matplotlib.rcParams["savefig.transparent"] = False

import numpy as np
import matplotlib.pyplot as plt

# 目标输出路径
out_png = "/mnt/hdd/kimicode-projects/multisim-mcp/deliverables/figures-batch4/fig-ge-07.png"

# 参数设置
RC = 1.0
t_trig = 0.5           # 触发时刻
t_pw = 0.20            # 触发脉冲宽度（窄脉冲）
Tp = 1.0986 * RC       # ln(3) * RC ≈ 1.1 RC
t_thres = t_trig + Tp  # 达到 2/3 Ucc 的时刻 ≈ 1.60
t_total = 4.2          # 横轴终点

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(9.5, 6.4), sharex=True,
    gridspec_kw={'height_ratios': [1, 2.3], 'hspace': 0.12}
)

# ==================== 1. 上行：触发脉冲 ====================
t_trig_wave = np.array([0, t_trig, t_trig, t_trig + t_pw, t_trig + t_pw, t_total])
v_trig_wave = np.array([1.0, 1.0, 0.0, 0.0, 1.0, 1.0])

ax1.plot(t_trig_wave, v_trig_wave, color="#1f77b4", lw=2.2)
ax1.set_ylim(-0.25, 1.7)
ax1.set_ylabel("触发输入", fontsize=11, fontweight="bold")
ax1.set_yticks([0, 1.0])
ax1.set_yticklabels(["0", "高电平"], fontsize=10)
ax1.grid(True, linestyle=":", alpha=0.5)

# 标注窄脉冲：移到触发脉冲上方的空白区，加引线指向窄脉冲
ax1.annotate(
    "", xy=(t_trig + t_pw/2, 0.0),
    xytext=(t_trig + t_pw/2 + 0.35, 1.25),
    arrowprops=dict(arrowstyle="->", color="#1f77b4", lw=1.2)
)
ax1.text(
    t_trig + t_pw/2 + 0.40, 1.25,
    "低有效窄脉冲\n(触发信号)",
    fontsize=9.5, color="#1f77b4", ha="left", va="center"
)

ax1.set_title("555 单稳态的 RC 充电曲线", fontsize=14, pad=12, fontweight="bold")

# ==================== 2. 下行：电容电压 Uc ====================
# 实际暂稳态充电曲线
t_charge = np.linspace(t_trig, t_thres, 300)
uc_charge = 1.0 * (1.0 - np.exp(-(t_charge - t_trig) / RC))

# 饱和趋势延伸虚线
t_sat = np.linspace(t_thres, t_total, 300)
uc_sat = 1.0 * (1.0 - np.exp(-(t_sat - t_trig) / RC))

# 翻转后快速放电及恢复
t_disc_end = t_thres + 0.05
t_disc = np.array([t_thres, t_disc_end])
uc_disc = np.array([2/3, 0.0])

# 绘制曲线
ax2.plot([0, t_trig], [0, 0], color="#d62728", lw=2.2)
ax2.plot(t_charge, uc_charge, color="#d62728", lw=2.5, label=r"电容电压 $U_c$ 充电曲线")
ax2.plot(t_disc, uc_disc, color="#d62728", lw=2.2)
ax2.plot([t_disc_end, t_total], [0, 0], color="#d62728", lw=2.2)

# 饱和趋势虚线
ax2.plot(t_sat, uc_sat, color="#d62728", linestyle="--", lw=1.8, alpha=0.8, label=r"向 $U_{cc}$ 饱和充电趋势")

# 水平参考线：Ucc 与 2/3 Ucc
ax2.axhline(1.0, color="#666666", linestyle="--", lw=1.2)
ax2.text(t_total - 0.08, 1.02, r"充电饱和上限 $U_{cc}$", ha="right", va="bottom",
         fontsize=10, color="#444444", fontweight="bold")

ax2.axhline(2/3, color="#7b1fa2", linestyle="--", lw=1.2)
ax2.text(t_total - 0.08, 2/3 + 0.02, r"阈值参考线 $\frac{2}{3} U_{cc}$", ha="right", va="bottom",
         fontsize=10, color="#7b1fa2", fontweight="bold")

# 竖直对齐参考线
for ax in (ax1, ax2):
    ax.axvline(t_trig, color="#e65100", linestyle=":", lw=1.2)
ax2.axvline(t_thres, color="#7b1fa2", linestyle=":", lw=1.2)

# 交点标记与引线标注
ax2.plot(t_thres, 2/3, marker='o', color="#7b1fa2", markersize=6, zorder=5)
ax2.annotate(
    r"交点 $(\frac{2}{3} U_{cc})$",
    xy=(t_thres, 2/3),
    xytext=(t_thres + 0.35, 2/3 - 0.16),
    arrowprops=dict(arrowstyle="->", color="#7b1fa2", lw=1.2),
    fontsize=9.5, color="#7b1fa2", ha="left", va="center",
    bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#7b1fa2", alpha=0.9)
)

# 触发时刻和翻转时刻在横轴上方/下方的标注
ax2.text(t_trig, -0.06, "触发时刻", ha="center", va="top", fontsize=9.5, color="#e65100")
ax2.text(t_thres, -0.06, "翻转时刻", ha="center", va="top", fontsize=9.5, color="#7b1fa2")

# 双向箭头标注 Tp ≈ 1.1RC
# 置于 y = 0.83 高度（在 2/3 Ucc 上方、Ucc 下方，完全避开所有曲线和参考线）
arrow_y = 0.83
ax2.annotate(
    '', xy=(t_trig, arrow_y), xytext=(t_thres, arrow_y),
    arrowprops=dict(arrowstyle='<->', color='#b71c1c', lw=1.6)
)
ax2.text(
    (t_trig + t_thres) / 2, arrow_y + 0.03, r"$T_p \approx 1.1RC$",
    ha='center', va='bottom', fontsize=11.5, fontweight='bold', color='#b71c1c',
    bbox=dict(boxstyle='round,pad=0.25', facecolor='#fffde7', edgecolor='#b71c1c', alpha=0.95)
)

# 坐标轴与范围
ax2.set_ylim(-0.16, 1.25)
ax2.set_ylabel(r"电容电压 $U_c$", fontsize=11, fontweight="bold")
ax2.set_yticks([0, 2/3, 1.0])
ax2.set_yticklabels(["0", r"$\frac{2}{3} U_{cc}$", r"$U_{cc}$"], fontsize=10)
ax2.set_xlabel("时间 $t$", fontsize=11, fontweight="bold")
ax2.grid(True, linestyle=":", alpha=0.5)

# 图例
ax2.legend(loc="lower right", framealpha=0.92, fontsize=9.5)

# 底部说明
fig.text(
    0.5, 0.02,
    "说明：脉宽与 $T_p$ 无关（触发脉冲只负责起跑，输出暂稳态脉宽仅由 $RC$ 决定）。",
    ha="center", fontsize=10.5, fontweight="bold", color="#8b0000"
)

# 边距
plt.subplots_adjust(top=0.91, bottom=0.15, left=0.10, right=0.94)

plt.savefig(out_png, dpi=300)
plt.close()
