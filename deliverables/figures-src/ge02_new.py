import matplotlib; matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["Noto Sans CJK SC"] + list(matplotlib.rcParams["font.sans-serif"])
matplotlib.rcParams["savefig.transparent"] = False

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# 画布调整为 16 x 9.8 英寸
fig = plt.figure(figsize=(16, 9.8), dpi=200)

# 网格布局
gs = fig.add_gridspec(2, 2, width_ratios=[1.0, 1.25], height_ratios=[1, 1],
                      left=0.06, right=0.95, bottom=0.15, top=0.86, wspace=0.25, hspace=0.45)

ax_left = fig.add_subplot(gs[:, 0])
ax_top = fig.add_subplot(gs[0, 1])
ax_bot = fig.add_subplot(gs[1, 1])

ax_left.axis("off")

# 绘制左栏卡片圆角背景（y从0.01到0.98，完美包容所有文字）
rect = mpatches.FancyBboxPatch((0.01, 0.01), 0.98, 0.98, transform=ax_left.transAxes,
                              boxstyle="round,pad=0.02,rounding_size=0.03",
                              ec="#B0C4DE", fc="#F8FAFD", lw=1.5)
ax_left.add_patch(rect)

# ----------------- 左栏内容排版（紧凑优雅，彻底不出框） -----------------
ax_left.text(0.5, 0.94, "【代数形式解析】", transform=ax_left.transAxes,
             ha="center", va="top", fontsize=15, fontweight="bold", color="#1B365D")

# 区域一：已知相量 (y=0.86 到 0.76)
known_text = (
    "已知相量：\n"
    r"    $\mathrm{U}_1 = 3 + \mathrm{j}4$" "\n"
    r"    $\mathrm{U}_2 = 3 - \mathrm{j}4$"
)
ax_left.text(0.08, 0.86, known_text, transform=ax_left.transAxes,
             ha="left", va="top", fontsize=12, color="#333333", linespacing=1.2)

# 分割线 1
line1 = plt.Line2D([0.06, 0.94], [0.73, 0.73], transform=ax_left.transAxes, color="#D0D7DE", lw=1)
ax_left.add_line(line1)

# 区域二：相量之和 (y=0.70 到 0.44)
sum_text = (
    "一、相量之和（菱形法则）：\n"
    r"    公式：$\mathrm{U}_1 + \mathrm{U}_2 = (3 + \mathrm{j}4) + (3 - \mathrm{j}4)$" "\n"
    r"    实部相加：$3 + 3 = 6$" "\n"
    r"    虚部相加：$4 + (-4) = 0$" "\n"
    r"    合相量：$6 + \mathrm{j}0$（落在 $\mathrm{Re}$ 轴正半轴）"
)
ax_left.text(0.08, 0.70, sum_text, transform=ax_left.transAxes,
             ha="left", va="top", fontsize=11.5, color="#1B5E20", linespacing=1.2)

# 分割线 2
line2 = plt.Line2D([0.06, 0.94], [0.41, 0.41], transform=ax_left.transAxes, color="#D0D7DE", lw=1)
ax_left.add_line(line2)

# 区域三：相量之差 (y=0.38 开始，底端约在 0.08，彻底完全处于卡片内部)
diff_text = (
    "二、相量之差（首尾相接）：\n"
    r"    公式：$\mathrm{U}_1 - \mathrm{U}_2 = \mathrm{U}_1 + (-\mathrm{U}_2)$" "\n"
    r"    相反相量：$-\mathrm{U}_2 = -3 + \mathrm{j}4$（指向左上）" "\n"
    r"    实部相减：$3 - 3 = 0$" "\n"
    r"    虚部相减：$4 - (-4) = 8$" "\n"
    r"    合相量：$0 + \mathrm{j}8$（竖直向上，落在 $\mathrm{Im}$ 轴）"
)
ax_left.text(0.08, 0.38, diff_text, transform=ax_left.transAxes,
             ha="left", va="top", fontsize=11.5, color="#880E4F", linespacing=1.2)

# ----------------- 右上：相量和 -----------------
ax_top.set_title(r"相量加法：$\mathrm{U}_1 + \mathrm{U}_2$ 菱形法则（合相量 $6 + \mathrm{j}0$ 落在 $\mathrm{Re}$ 正半轴）",
                 fontsize=12, fontweight="bold", pad=12, color="#1B365D", loc="left")
ax_top.axhline(0, color="#666666", lw=1, ls="-", alpha=0.7)
ax_top.axvline(0, color="#666666", lw=1, ls="-", alpha=0.7)
ax_top.grid(True, ls=":", alpha=0.4)

ax_top.plot([3, 6], [4, 0], color="#0072B2", ls="--", lw=1.3, alpha=0.7)
ax_top.plot([3, 6], [-4, 0], color="#D9381E", ls="--", lw=1.3, alpha=0.7)

ax_top.annotate("", xy=(3, 4), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#D9381E", lw=2.2, mutation_scale=15))
ax_top.text(1.2, 2.7, r"$\mathrm{U}_1 = 3 + \mathrm{j}4$", color="#D9381E", fontsize=11, fontweight="bold")

ax_top.annotate("", xy=(3, -4), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#0072B2", lw=2.2, mutation_scale=15))
ax_top.text(1.2, -3.0, r"$\mathrm{U}_2 = 3 - \mathrm{j}4$", color="#0072B2", fontsize=11, fontweight="bold")

ax_top.annotate("", xy=(6, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#2E7D32", lw=2.8, mutation_scale=18))
ax_top.text(3.5, 0.6, r"$\mathrm{U}_1 + \mathrm{U}_2 = 6 + \mathrm{j}0$", color="#2E7D32", fontsize=11, fontweight="bold")

ax_top.set_xlim(-1, 7.5)
ax_top.set_ylim(-5.5, 5.5)
ax_top.set_xlabel(r"$\mathrm{Re}$ (实轴)", fontsize=11)
ax_top.set_ylabel(r"$\mathrm{Im}$ (虚轴)", fontsize=11)

# ----------------- 右下：相量差 -----------------
ax_bot.set_title(r"相量减法：$\mathrm{U}_1 + (-\mathrm{U}_2)$ 首尾相接（合相量 $0 + \mathrm{j}8$ 竖直向上）",
                 fontsize=12, fontweight="bold", pad=12, color="#1B365D", loc="left")
ax_bot.axhline(0, color="#666666", lw=1, ls="-", alpha=0.7)
ax_bot.axvline(0, color="#666666", lw=1, ls="-", alpha=0.7)
ax_bot.grid(True, ls=":", alpha=0.4)

ax_bot.annotate("", xy=(3, 4), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#D9381E", lw=2.2, mutation_scale=15))
ax_bot.text(1.8, 1.8, r"$\mathrm{U}_1 = 3 + \mathrm{j}4$", color="#D9381E", fontsize=10.5, fontweight="bold")

# -U2 指向左上
ax_bot.annotate("", xy=(0, 8), xytext=(3, 4),
                arrowprops=dict(arrowstyle="-|>", color="#E69F00", lw=2.2, mutation_scale=15))
ax_bot.text(1.8, 6.2, r"$-\mathrm{U}_2 = -3 + \mathrm{j}4$" "\n" "(首尾相接，指左上)", color="#D97706", fontsize=10.5, fontweight="bold", ha="left")

ax_bot.annotate("", xy=(3, -4), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#0072B2", lw=1.2, ls=":", mutation_scale=12, alpha=0.5))
ax_bot.text(1.5, -2.5, r"$\mathrm{U}_2$ (参考)", color="#0072B2", fontsize=9.5, alpha=0.6)

# 合相量 0 + j8 竖直向上
ax_bot.annotate("", xy=(0, 8), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#880E4F", lw=2.8, mutation_scale=18))
ax_bot.text(-0.3, 4.0, r"$\mathrm{U}_1 - \mathrm{U}_2 = 0 + \mathrm{j}8$", color="#880E4F", fontsize=11, fontweight="bold", ha="right")

ax_bot.set_xlim(-4.5, 5.5)
ax_bot.set_ylim(-5, 9.5)
ax_bot.set_xlabel(r"$\mathrm{Re}$ (实轴)", fontsize=11)
ax_bot.set_ylabel(r"$\mathrm{Im}$ (虚轴)", fontsize=11)

# ----------------- 底部说明 -----------------
fig.text(0.5, 0.045, "底部说明：虚部一正一负，和抵消（实数 $6+\\mathrm{j}0$）、差加倍（纯虚数 $0+\\mathrm{j}8$）。",
         ha="center", va="center", fontsize=12.5, fontweight="bold", color="#1B365D",
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#FFF3CD", edgecolor="#FFEBAA", lw=1.2))

# 顶部总标题：放于左栏上方中央
fig.text(0.25, 0.96, "相量加减 = 首尾相接", fontsize=16, fontweight="bold", ha="center", va="center", color="#0F172A")

out_path = "/mnt/hdd/kimicode-projects/multisim-mcp/deliverables/figures-batch4/fig-ge-02.png"
plt.savefig(out_path, dpi=200)
plt.close()
print("Saved to", out_path)
