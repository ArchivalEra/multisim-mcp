import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["Noto Sans CJK SC"] + list(matplotlib.rcParams["font.sans-serif"])
matplotlib.rcParams["savefig.transparent"] = False

import matplotlib.pyplot as plt
import numpy as np

def create_figure():
    # 画布高 4.8 吋，三栏并排，紧凑饱满
    fig, axes = plt.subplots(1, 3, figsize=(14.0, 4.8), dpi=200)
    fig.patch.set_facecolor("white")
    
    titles = ["电阻元件 (R)", "电感元件 (L)", "电容元件 (C)"]
    bottom_texts = [r"$U$ 与 $I$ 同相", r"$I$ 滞后 $U$ 90°", r"$I$ 超前 $U$ 90°"]
    
    axis_color = "#333333"
    axis_lw = 1.3
    u_color = "#D32F2F"   # 电压相量红
    i_color = "#1976D2"   # 电流相量蓝
    
    # 坐标范围收紧至 0.82，大幅扩大图元占比，视觉饱满无空旷感
    lim = 0.82
    
    for idx, ax in enumerate(axes):
        ax.set_facecolor("white")
        ax.set_aspect("equal")
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        
        # 隐藏自带四周边框与默认刻度
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        
        # 坐标轴（实线带箭头，原点对称居中）
        # Re 轴 (横轴)
        ax.annotate(
            "", xy=(0.74, 0), xytext=(-0.68, 0),
            arrowprops=dict(
                arrowstyle="-|>", 
                mutation_scale=15, 
                color=axis_color, 
                lw=axis_lw
            ),
            zorder=2
        )
        ax.text(0.74, -0.09, r"$\mathrm{Re}$", fontsize=13, fontweight="bold", color=axis_color, ha="center", va="top")
        
        # Im 轴 (纵轴)
        ax.annotate(
            "", xy=(0, 0.74), xytext=(0, -0.68),
            arrowprops=dict(
                arrowstyle="-|>", 
                mutation_scale=15, 
                color=axis_color, 
                lw=axis_lw
            ),
            zorder=2
        )
        ax.text(0.08, 0.74, r"$\mathrm{Im}$", fontsize=13, fontweight="bold", color=axis_color, ha="left", va="center")
        
        # 原点 O 标记（严格置于第三象限）
        ax.text(-0.06, -0.06, "O", fontsize=12, color="#757575", ha="right", va="top")
        
        # 顶部栏目标题（置于 x=0 原点正上方）
        ax.text(
            0, 0.92, titles[idx], 
            fontsize=15, fontweight="bold", ha="center", va="center", color="#212121",
            bbox=dict(boxstyle="round,pad=0.45", fc="#F8F9FA", ec="#E0E0E0", lw=1.2)
        )
        
        # 相量长度设置：比例饱满
        u_len = 0.58
        i_len = 0.43
        
        if idx == 0:
            # R 栏：同相
            # U 与 I 平行错开绘制：U 略偏上(y=0.026)，I 略偏下(y=-0.026)
            ax.annotate(
                "", xy=(u_len, 0.026), xytext=(0, 0.026),
                arrowprops=dict(arrowstyle="-|>", mutation_scale=18, color=u_color, lw=3.0),
                zorder=4
            )
            ax.text(u_len + 0.05, 0.05, r"$U$", fontsize=17, fontweight="bold", color=u_color, ha="left", va="bottom")
            
            ax.annotate(
                "", xy=(i_len, -0.026), xytext=(0, -0.026),
                arrowprops=dict(arrowstyle="-|>", mutation_scale=18, color=i_color, lw=3.0),
                zorder=4
            )
            ax.text(i_len + 0.05, -0.05, r"$I$", fontsize=17, fontweight="bold", color=i_color, ha="left", va="top")
            
        elif idx == 1:
            # L 栏：I 滞后 U 90°
            # U 沿 +Re，I 沿 -Im
            ax.annotate(
                "", xy=(u_len, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", mutation_scale=18, color=u_color, lw=3.0),
                zorder=4
            )
            ax.text(u_len + 0.05, 0.05, r"$U$", fontsize=17, fontweight="bold", color=u_color, ha="left", va="bottom")
            
            ax.annotate(
                "", xy=(0, -i_len), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", mutation_scale=18, color=i_color, lw=3.0),
                zorder=4
            )
            # I 标签放置在垂直箭头末端右侧留白处，避免压在圆弧线上
            ax.text(0.08, -i_len * 0.95, r"$I$", fontsize=17, fontweight="bold", color=i_color, ha="left", va="top")
            
            # 圆弧带箭头：从 U(0°) 顺时针指向 I(-90°)
            arc_r = 0.28
            theta = np.linspace(-0.04, -np.pi/2 + 0.16, 40)
            ax.plot(arc_r * np.cos(theta), arc_r * np.sin(theta), color="#555555", lw=1.4, ls="-")
            ax.annotate(
                "", xy=(0, -arc_r), 
                xytext=(arc_r * np.cos(-np.pi/2 + 0.18), arc_r * np.sin(-np.pi/2 + 0.18)),
                arrowprops=dict(arrowstyle="-|>", mutation_scale=13, color="#555555", lw=1.4),
                zorder=3
            )
            # 90° 标注稍远离圆弧，留出呼吸空间
            ax.text(0.26, -0.26, "90°", fontsize=13, fontweight="bold", color="#424242", ha="center", va="center")
            
        elif idx == 2:
            # C 栏：I 超前 U 90°
            # U 沿 +Re，I 沿 +Im
            ax.annotate(
                "", xy=(u_len, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", mutation_scale=18, color=u_color, lw=3.0),
                zorder=4
            )
            ax.text(u_len + 0.05, 0.05, r"$U$", fontsize=17, fontweight="bold", color=u_color, ha="left", va="bottom")
            
            ax.annotate(
                "", xy=(0, i_len), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", mutation_scale=18, color=i_color, lw=3.0),
                zorder=4
            )
            # I 标签放置在垂直箭头顶端右侧留白处，避免压在圆弧线上
            ax.text(0.08, i_len * 0.95, r"$I$", fontsize=17, fontweight="bold", color=i_color, ha="left", va="bottom")
            
            # 圆弧带箭头：从 U(0°) 逆时针指向 I(+90°)
            arc_r = 0.28
            theta = np.linspace(0.04, np.pi/2 - 0.16, 40)
            ax.plot(arc_r * np.cos(theta), arc_r * np.sin(theta), color="#555555", lw=1.4, ls="-")
            ax.annotate(
                "", xy=(0, arc_r), 
                xytext=(arc_r * np.cos(np.pi/2 - 0.18), arc_r * np.sin(np.pi/2 - 0.18)),
                arrowprops=dict(arrowstyle="-|>", mutation_scale=13, color="#555555", lw=1.4),
                zorder=3
            )
            # 90° 标注
            ax.text(0.26, 0.26, "90°", fontsize=13, fontweight="bold", color="#424242", ha="center", va="center")
            
        # 底部说明文本（置于 x=0 原点正下方）
        # 硬性要求：U 与 90° 之间要有间隔，不能连成一个字符串。
        ax.text(
            0, -0.92, bottom_texts[idx],
            fontsize=14, fontweight="bold", ha="center", va="center", color="#1E3A8A",
            bbox=dict(boxstyle="round,pad=0.45", fc="#EFF6FF", ec="#BFDBFE", lw=1.2)
        )
    
    # 边距精调：三栏等高对称对齐
    plt.subplots_adjust(left=0.03, right=0.97, top=0.82, bottom=0.18, wspace=0.20)
    
    out_path = "/mnt/hdd/kimicode-projects/multisim-mcp/deliverables/figures-batch4/fig-ge-03.png"
    plt.savefig(out_path, dpi=200)
    plt.close()

if __name__ == "__main__":
    create_figure()
