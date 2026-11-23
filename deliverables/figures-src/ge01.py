import matplotlib; matplotlib.use("Agg")
matplotlib.rcParams["font.family"]="sans-serif"
matplotlib.rcParams["font.sans-serif"]=["Noto Sans CJK SC"]+list(matplotlib.rcParams["font.sans-serif"])
matplotlib.rcParams["savefig.transparent"]=False

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, ConnectionPatch

# 画布尺寸：总宽高比 15.0 x 5.4 英寸
fig = plt.figure(figsize=(15.0, 5.4), dpi=200)

# 三栏子图采用绝对坐标定位，彻底保证物理对齐：
# 底部留白 0.22，高度统一 0.58
# 画布高 5.4 inch，子图高度 = 5.4 * 0.58 = 3.132 inch
# 为了让中栏成为严格的正圆，中栏的物理宽度必须等于 3.132 inch，
# 对应在 15 inch 宽画布中的相对比例 = 3.132 / 15.0 = 0.2088
b = 0.22
h = 0.58
w_mid = 0.2088
w_side = 0.25

# 水平间距排布
# 左栏 left: 0.06 -> right: 0.31
# 中栏 left: 0.395 -> right: 0.6038
# 右栏 left: 0.69 -> right: 0.94
ax0 = fig.add_axes([0.06, b, w_side, h])
ax1 = fig.add_axes([0.395, b, w_mid, h])
ax2 = fig.add_axes([0.69, b, w_side, h])

# 统一三栏纵轴与横轴对应范围（幅值 311 保持严格一致）
YLIM = (-420, 420)
R = 311

# ==================== 左栏：波形 ====================
ax0.set_title("波形", fontsize=15, pad=12, fontweight="bold", color="#111111")
ax0.set_xlim(-0.15, 1.25)
ax0.set_ylim(YLIM)

# 数据：一个周期正弦
t = np.linspace(0, 1.0, 500)
u = R * np.sin(2 * np.pi * t)

# 坐标轴箭头
ax0.annotate("", xy=(1.20, 0), xytext=(-0.10, 0),
             arrowprops=dict(arrowstyle="-|>", color="#333333", lw=1.2, mutation_scale=12))
ax0.annotate("", xy=(0, 400), xytext=(0, -400),
             arrowprops=dict(arrowstyle="-|>", color="#333333", lw=1.2, mutation_scale=12))
ax0.text(1.22, -25, r"$t$", fontsize=13, ha="left", va="center")
ax0.text(-0.04, 395, r"$u$", fontsize=13, ha="right", va="center")

# 正弦曲线
ax0.plot(t, u, color="#1f77b4", lw=2.4)

# 峰值 311 标注
ax0.plot([0.25], [311], "o", color="#1f77b4", ms=5)
ax0.text(0.25, 335, "峰值 311", color="#1f77b4", fontsize=11, ha="center", va="bottom", fontweight="bold")
ax0.text(-0.03, 311, "311", color="#1f77b4", fontsize=10.5, ha="right", va="center")
ax0.plot([-0.015, 0.015], [311, 311], color="#1f77b4", lw=1)

# 谷值 -311 标注
ax0.plot([0.75], [-311], "o", color="#1f77b4", ms=4, alpha=0.6)
ax0.text(-0.03, -311, "-311", color="#666666", fontsize=10.5, ha="right", va="center")
ax0.plot([-0.015, 0.015], [-311, -311], color="#666666", lw=1)

# 原点 0
ax0.text(-0.03, -22, "0", color="#666666", fontsize=10.5, ha="right", va="center")

# 周期 T 标注
ax0.plot([1.0, 1.0], [0, -220], color="#d62728", ls="--", lw=1.0, alpha=0.8)
ax0.plot([0.0, 0.0], [0, -220], color="#d62728", ls="--", lw=1.0, alpha=0.8)
ax0.annotate("", xy=(1.0, -180), xytext=(0.0, -180),
             arrowprops=dict(arrowstyle="<->", color="#d62728", lw=1.3, mutation_scale=12))
ax0.text(0.5, -200, "周期 T", color="#d62728", fontsize=11, ha="center", va="top", fontweight="bold")
ax0.text(1.0, 20, r"$T$", fontsize=11, ha="center", va="bottom", color="#d62728")

ax0.set_xticks([])
ax0.set_yticks([])
for spine in ax0.spines.values():
    spine.set_visible(False)

# 底部说明文字
ax0.text(0.5, -0.15, "时域瞬时值波形\n随时间 $t$ 连续变化，峰值 311 与周期 $T$ 直观可见",
         fontsize=10.5, ha="center", va="top", color="#222222", linespacing=1.4, transform=ax0.transAxes)


# ==================== 中栏：旋转箭头 ====================
ax1.set_title("旋转箭头", fontsize=15, pad=12, fontweight="bold", color="#111111")
ax1.set_xlim(-420, 420)
ax1.set_ylim(YLIM)

# 辅助正圆轨迹 (半径 311)
theta = np.linspace(0, 2*np.pi, 250)
ax1.plot(R * np.cos(theta), R * np.sin(theta), color="#aec7e8", ls="--", lw=1.3)

# 坐标参考轴
ax1.annotate("", xy=(390, 0), xytext=(-380, 0),
             arrowprops=dict(arrowstyle="-|>", color="#777777", lw=1.0, mutation_scale=10))
ax1.annotate("", xy=(0, 400), xytext=(0, -380),
             arrowprops=dict(arrowstyle="-|>", color="#777777", lw=1.0, mutation_scale=10))
ax1.text(-15, -20, "0", fontsize=10.5, color="#777777", ha="right", va="top")

# t = 0 初态旋转箭头（位于实轴正半轴，与右栏相量同向）
ax1.annotate("", xy=(R, 0), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color="#2ca02c", lw=2.6, mutation_scale=18))
ax1.plot([R], [0], "o", color="#2ca02c", ms=5)
# 文字避开实轴和虚线圆，放在箭头下方偏左位置，防止压线
ax1.text(120, -55, "长度 311", color="#2ca02c", fontsize=10.5, ha="center", va="top", fontweight="bold")
ax1.text(R + 25, 25, r"$t=0$", color="#2ca02c", fontsize=10, ha="left", va="bottom")

# 转速 w 标注（逆时针圆弧箭头，从 25° 到 70°）
arc_r = 150
arc_w = Arc((0, 0), arc_r*2, arc_r*2, angle=0, theta1=25, theta2=70, color="#ff7f0e", lw=1.8)
ax1.add_patch(arc_w)
head_x = arc_r * np.cos(np.deg2rad(73))
head_y = arc_r * np.sin(np.deg2rad(73))
ax1.annotate("", xy=(head_x - 3, head_y + 2), xytext=(head_x, head_y),
             arrowprops=dict(arrowstyle="-|>", color="#ff7f0e", lw=1.8, mutation_scale=12))
ax1.text(105, 175, r"转速 $\omega$", color="#ff7f0e", fontsize=11, ha="center", va="bottom", fontweight="bold")

# 圆最高点 (0, 311)
ax1.plot([0], [311], "o", color="#1f77b4", ms=4, alpha=0.6)

ax1.set_xticks([])
ax1.set_yticks([])
for spine in ax1.spines.values():
    spine.set_visible(False)

# 底部说明文字
ax1.text(0.5, -0.15, r"几何旋转动态模型" + "\n" + r"圆半径为 311，以转速 $\omega$ 逆时针旋转，纵轴投影即为瞬时值",
         fontsize=10.5, ha="center", va="top", color="#222222", linespacing=1.4, transform=ax1.transAxes)


# ==================== 右栏：相量 ====================
# 正弦交流相量（模 311，正弦式初相位 phi = 0 对应相量沿虚轴正向/90°，端点高度恰好为 311！）
ax2.set_title("相量", fontsize=15, pad=12, fontweight="bold", color="#111111")
ax2.set_xlim(-120, 420)
ax2.set_ylim(YLIM)

# 复平面坐标轴
ax2.annotate("", xy=(390, 0), xytext=(-90, 0),
             arrowprops=dict(arrowstyle="-|>", color="#333333", lw=1.2, mutation_scale=12))
ax2.annotate("", xy=(0, 400), xytext=(0, -400),
             arrowprops=dict(arrowstyle="-|>", color="#333333", lw=1.2, mutation_scale=12))
ax2.text(395, -22, r"$\mathrm{Re}$", fontsize=13, ha="left", va="center", fontweight="bold")
ax2.text(-15, 395, r"$\mathrm{Im}$", fontsize=13, ha="right", va="center", fontweight="bold")
ax2.text(-15, -20, "0", fontsize=10.5, color="#666666", ha="right", va="top")

# 相量箭头：模 311，沿虚轴正向，端点高度恰好落在 (0, 311)！
ax2.annotate("", xy=(0, 311), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color="#9467bd", lw=2.8, mutation_scale=18))
ax2.plot([0], [311], "o", color="#9467bd", ms=6)

# 标注模 311 与刻度 311
ax2.text(25, 155, "模 311", color="#9467bd", fontsize=11, ha="left", va="center", fontweight="bold")
ax2.text(-15, 311, "311", color="#1f77b4", fontsize=10.5, ha="right", va="center")
ax2.plot([-8, 8], [311, 311], color="#1f77b4", lw=1)

# 标注初相位 phi = 0°（与虚轴夹角/初相基准）
ax2.text(25, 290, r"初相位 $\varphi$ = 0°", color="#d62728", fontsize=11, ha="left", va="center", fontweight="bold")

ax2.set_xticks([])
ax2.set_yticks([])
for spine in ax2.spines.values():
    spine.set_visible(False)

# 底部说明文字
ax2.text(0.5, -0.15, r"频域复数相量" + "\n" + r"消去时间因子，以模 311 和初相位 $\varphi$ 将交流分析转化为复数代数",
         fontsize=10.5, ha="center", va="top", color="#222222", linespacing=1.4, transform=ax2.transAxes)


# 1. 峰值高度贯穿水平虚线：从左栏波形峰值点 (0.25, 311) 水平引出，穿过中栏圆顶 (0, 311)，直达右栏相量箭头端点 (0, 311)
con_peak = ConnectionPatch(
    xyA=(0.25, 311), coordsA=ax0.transData,
    xyB=(0, 311), coordsB=ax2.transData,
    color="#1f77b4", linestyle=":", linewidth=1.3, alpha=0.85
)
fig.add_artist(con_peak)

# 栏间提示小标签，均落在 y=311 高度线上
fig.text(0.352, 0.69, "峰值高度对应", fontsize=9.5, color="#1f77b4", ha="center", va="center",
         bbox=dict(boxstyle="round,pad=0.25", facecolor="#ffffff", edgecolor="#aec7e8", alpha=0.95))

fig.text(0.647, 0.69, "幅值高度对应", fontsize=9.5, color="#1f77b4", ha="center", va="center",
         bbox=dict(boxstyle="round,pad=0.25", facecolor="#ffffff", edgecolor="#aec7e8", alpha=0.95))

output_png = "/mnt/hdd/kimicode-projects/multisim-mcp/deliverables/figures-batch4/fig-ge-01.png"
plt.savefig(output_png, dpi=200)
print("Saved fig-ge-01.png successfully")
