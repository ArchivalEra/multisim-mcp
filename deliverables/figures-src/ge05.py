import matplotlib; matplotlib.use("Agg")
matplotlib.rcParams["font.family"]="sans-serif"
matplotlib.rcParams["font.sans-serif"]=["Noto Sans CJK SC"]+list(matplotlib.rcParams["font.sans-serif"])
matplotlib.rcParams["savefig.transparent"]=False

import matplotlib.pyplot as plt
import numpy as np

# 创建画布：三栏并排，比例协调匀称
fig, axes = plt.subplots(1, 3, figsize=(15, 6.2), dpi=300)

# 典雅高对比工程三相色：A相正红、B相工程绿、C相深海蓝
colors = {
    'A': '#E63946',  # 鲜明红
    'B': '#2A9D8F',  # 典雅绿
    'C': '#1D3557'   # 深海蓝
}

arrow_kwargs = dict(angles='xy', scale_units='xy', scale=1, width=0.016, headwidth=4.2, headlength=5.5)

# --- 1. 正序栏 (正序分量) ---
# A: 向上 (90°) -> (0, 1)
# B: 右下 (-30°) -> (sqrt(3)/2, -0.5)
# C: 左下 (210°) -> (-sqrt(3)/2, -0.5)
# 走向分析：从 A(90°) -> B(-30°) -> C(210°) 沿圆周走是顺时针方向。
ax = axes[0]
ax.set_title("正序分量", fontsize=20, fontweight='bold', pad=18)

# 相量箭头 (长度 1.0)
ax.quiver(0, 0, 0, 1, color=colors['A'], **arrow_kwargs)
ax.quiver(0, 0, np.sqrt(3)/2, -0.5, color=colors['B'], **arrow_kwargs)
ax.quiver(0, 0, -np.sqrt(3)/2, -0.5, color=colors['C'], **arrow_kwargs)

# 字母标签 (斜体印刷体)
ax.text(0, 1.16, r"$A$", color=colors['A'], fontsize=18, fontweight='bold', ha='center', va='bottom')
ax.text(np.sqrt(3)/2 + 0.12, -0.55, r"$B$", color=colors['B'], fontsize=18, fontweight='bold', ha='left', va='top')
ax.text(-np.sqrt(3)/2 - 0.12, -0.55, r"$C$", color=colors['C'], fontsize=18, fontweight='bold', ha='right', va='top')

# 顺时针旋转引导弧线 (从 A 走向 B)
r = 0.45
theta_pos = np.linspace(np.radians(70), np.radians(-10), 50)
ax.plot(r * np.cos(theta_pos), r * np.sin(theta_pos), color='#777777', linestyle='--', linewidth=1.5)
ax.annotate('', xy=(r * np.cos(np.radians(-10)), r * np.sin(np.radians(-10))),
            xytext=(r * np.cos(np.radians(8)), r * np.sin(np.radians(8))),
            arrowprops=dict(arrowstyle="-|>", color="#777777", lw=1.5, mutation_scale=12))

ax.set_xlim(-1.45, 1.45)
ax.set_ylim(-1.60, 1.45)
ax.set_aspect('equal')
ax.axis('off')
ax.text(0, -1.18, r"$A \rightarrow B \rightarrow C$ 顺时针 120°", fontsize=14, ha='center', fontweight='bold', color='#111111')
ax.text(0, -1.42, "大小相等、互差 120°", fontsize=13, ha='center', color='#555555')


# --- 2. 负序栏 (负序分量) ---
# A 向上 (90°)、B 左下 (210°)、C 右下 (-30°)
# 严格遵守硬性要求：“「顺时针 / 逆时针」的方向词必须与箭头实际走向一致：从 A 走到 B 再走到 C，如果走的是顺时针就写顺时针。写完自己拿坐标核一遍。”
# 坐标严格核实：A(12点) -> B(8点) -> C(4点)，从 A 走到 B 再走到 C 走的是逆时针，说明写「$A \rightarrow B \rightarrow C$ 逆时针 120°」
ax = axes[1]
ax.set_title("负序分量", fontsize=20, fontweight='bold', pad=18)

ax.quiver(0, 0, 0, 1, color=colors['A'], **arrow_kwargs)
ax.quiver(0, 0, -np.sqrt(3)/2, -0.5, color=colors['B'], **arrow_kwargs)
ax.quiver(0, 0, np.sqrt(3)/2, -0.5, color=colors['C'], **arrow_kwargs)

ax.text(0, 1.16, r"$A$", color=colors['A'], fontsize=18, fontweight='bold', ha='center', va='bottom')
ax.text(-np.sqrt(3)/2 - 0.12, -0.55, r"$B$", color=colors['B'], fontsize=18, fontweight='bold', ha='right', va='top')
ax.text(np.sqrt(3)/2 + 0.12, -0.55, r"$C$", color=colors['C'], fontsize=18, fontweight='bold', ha='left', va='top')

# 逆时针旋转引导弧线 (从 A 走向 B)
theta_neg = np.linspace(np.radians(110), np.radians(190), 50)
ax.plot(r * np.cos(theta_neg), r * np.sin(theta_neg), color='#777777', linestyle='--', linewidth=1.5)
ax.annotate('', xy=(r * np.cos(np.radians(190)), r * np.sin(np.radians(190))),
            xytext=(r * np.cos(np.radians(172)), r * np.sin(np.radians(172))),
            arrowprops=dict(arrowstyle="-|>", color="#777777", lw=1.5, mutation_scale=12))

ax.set_xlim(-1.45, 1.45)
ax.set_ylim(-1.60, 1.45)
ax.set_aspect('equal')
ax.axis('off')
ax.text(0, -1.18, r"$A \rightarrow B \rightarrow C$ 逆时针 120°", fontsize=14, ha='center', fontweight='bold', color='#111111')
ax.text(0, -1.42, "大小相等、互差 120°", fontsize=13, ha='center', color='#555555')


# --- 3. 零序栏 (零序分量) ---
# 硬性要求：
# 1. 零序栏必须一眼看出是三支同向的箭头，不能只画成一支。
# 2. 三支全部同向（都向上），横向略错开以便看清是三支。
# 3. 底部说明「三支同向、同相位」和「大小相等」。
# 尺寸优化：基准起点 y = -0.5，与正负序 B、C 箭头的底部最低点齐平；
# 箭头模长 1.0 (至 y = 0.5)，使零序箭头群体在垂直方向完全居中，与正负序整体重心完美契合！
ax = axes[2]
ax.set_title("零序分量", fontsize=20, fontweight='bold', pad=18)

offsets = [-0.42, 0.0, 0.42]
labels = [r"$A$", r"$B$", r"$C$"]
keys = ['A', 'B', 'C']
y_start = -0.5
arrow_len = 1.0  # 严格保持与正序、负序各相量完全相同模长 (1.0)

# 基准起点参考线（虚线与 -0.5 齐平）
ax.plot([-0.70, 0.70], [y_start, y_start], color='#CCCCCC', linestyle='--', linewidth=1.2)

for off, label, key in zip(offsets, labels, keys):
    ax.quiver(off, y_start, 0, arrow_len, color=colors[key], **arrow_kwargs)
    ax.text(off, y_start + arrow_len + 0.16, label, color=colors[key], fontsize=18, fontweight='bold', ha='center', va='bottom')

ax.set_xlim(-1.45, 1.45)
ax.set_ylim(-1.60, 1.45)
ax.set_aspect('equal')
ax.axis('off')
ax.text(0, -1.18, "三支同向、同相位", fontsize=14, ha='center', fontweight='bold', color='#111111')
ax.text(0, -1.42, "大小相等", fontsize=13, ha='center', color='#555555')

plt.tight_layout()
output_path = "/mnt/hdd/kimicode-projects/multisim-mcp/deliverables/figures-batch4/fig-ge-05.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Rendered: {output_path}")
