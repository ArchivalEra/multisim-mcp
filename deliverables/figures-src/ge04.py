import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["Noto Sans CJK SC"] + list(matplotlib.rcParams["font.sans-serif"])
matplotlib.rcParams["savefig.transparent"] = False

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Arc, FancyBboxPatch

def draw_impedance_triangle():
    # 画布设置
    fig, ax = plt.subplots(figsize=(11.6, 5.0), dpi=300)
    
    # 直角三角形几何顶点
    p_origin = np.array([0.9, 1.1])
    r_len = 4.2
    x_len = 3.0
    p_right = p_origin + np.array([r_len, 0.0])
    p_top = p_origin + np.array([r_len, x_len])
    
    # 填充三角形几何内部背景色
    triangle = Polygon([p_origin, p_right, p_top], closed=True, 
                       facecolor='#F4F7FA', edgecolor='none', zorder=1)
    ax.add_patch(triangle)
    
    # 三条直角三角形边绘制
    # 横边 R - 经典工程蓝
    ax.plot([p_origin[0], p_right[0]], [p_origin[1], p_right[1]], 
            color='#1F77B4', lw=3.2, zorder=3, solid_capstyle='round')
    # 竖边 X - 工程绿
    ax.plot([p_right[0], p_top[0]], [p_right[1], p_top[1]], 
            color='#2CA02C', lw=3.2, zorder=3, solid_capstyle='round')
    # 斜边 Z - 醒目红
    ax.plot([p_origin[0], p_top[0]], [p_origin[1], p_top[1]], 
            color='#D62728', lw=3.5, zorder=3, solid_capstyle='round')
    
    # 顶点标记
    for p in [p_origin, p_right, p_top]:
        ax.plot(p[0], p[1], 'o', color='#2C3E50', markersize=5, zorder=4)
        
    # 直角符号标记 (在 p_right 处)
    sq_size = 0.35
    sq_x = [p_right[0] - sq_size, p_right[0] - sq_size, p_right[0]]
    sq_y = [p_right[1], p_right[1] + sq_size, p_right[1] + sq_size]
    ax.plot(sq_x, sq_y, color='#555555', lw=1.5, zorder=2)
    ax.plot(p_right[0] - sq_size/2, p_right[1] + sq_size/2, '.', color='#555555', markersize=3.5, zorder=2)
    
    # 角度 φ 弧线标记 (在 p_origin 处)
    phi_deg = np.degrees(np.arctan2(x_len, r_len))
    arc_radius = 1.15
    arc = Arc(p_origin, arc_radius * 2, arc_radius * 2, angle=0, theta1=0, theta2=phi_deg,
              color='#E65100', lw=2.0, zorder=3)
    ax.add_patch(arc)
    
    # φ 文本标注 (严格使用字符 'φ')
    phi_rad = np.radians(phi_deg / 2)
    phi_text_dist = arc_radius + 0.32
    phi_x = p_origin[0] + phi_text_dist * np.cos(phi_rad)
    phi_y = p_origin[1] + phi_text_dist * np.sin(phi_rad)
    ax.text(phi_x, phi_y, 'φ', fontsize=16, fontweight='bold', color='#E65100',
            ha='center', va='center', zorder=4)
    
    # 边长标注 (严格对应题目要求：横边标 R，竖边标 X 并注明 X = XL − XC，斜边标 Z，全部带单位 Ω)
    # 1. 横边 R: 下方
    ax.text(p_origin[0] + r_len / 2, p_origin[1] - 0.42, 'R (Ω)', 
            fontsize=14, fontweight='bold', color='#1F77B4', ha='center', va='top')
    
    # 2. 竖边 X: 右侧，注明 X (Ω) 及 X = XL − XC
    ax.text(p_right[0] + 0.28, p_origin[1] + x_len / 2, 
            'X (Ω)\n(X = XL − XC)', 
            fontsize=13.5, fontweight='bold', color='#2CA02C', ha='left', va='center', linespacing=1.35)
    
    # 3. 斜边 Z: 落在斜边上方留白处，法向充分外移，与斜边保持明显间距，彻底消除压线
    hyp_mid = (p_origin + p_top) / 2
    normal_vec = np.array([-np.sin(np.radians(phi_deg)), np.cos(np.radians(phi_deg))])
    z_pos = hyp_mid + normal_vec * 0.75
    ax.text(z_pos[0], z_pos[1], 'Z (Ω)', 
            fontsize=14, fontweight='bold', color='#D62728', 
            ha='center', va='center', rotation=phi_deg)

    # 右侧文字区卡片：起点设在 8.2，彻底拉开间距，完全消除压框与穿框风险
    info_box_x = 8.2
    info_box_y = 0.95
    info_box_w = 4.4
    info_box_h = 3.3
    
    info_card = FancyBboxPatch((info_box_x, info_box_y), info_box_w, info_box_h,
                               boxstyle='round,pad=0.2,rounding_size=0.2',
                               facecolor='#F8F9FA', edgecolor='#D0D7DE', lw=1.2, zorder=2)
    ax.add_patch(info_card)
    
    # 卡片内部标题
    ax.text(info_box_x + info_box_w/2, info_box_y + info_box_h - 0.35, '阻抗关系与量纲', 
            fontsize=14, fontweight='bold', color='#24292F', ha='center', va='center')
    
    # 卡片分割线
    ax.plot([info_box_x + 0.25, info_box_x + info_box_w - 0.25], 
            [info_box_y + info_box_h - 0.72, info_box_y + info_box_h - 0.72], 
            color='#E1E4E8', lw=1.0, zorder=3)
    
    # 公式 1: Z = √(R² + X²)
    ax.text(info_box_x + 0.45, info_box_y + info_box_h - 1.25, 
            r"$Z = \sqrt{R^{2} + X^{2}}$", 
            fontsize=15, fontweight='bold', color='#24292F', ha='left', va='center', zorder=3)
    
    # 公式 2: φ = arctan(X/R)
    ax.text(info_box_x + 0.45, info_box_y + info_box_h - 1.85, 
            r"$\varphi = \arctan(X/R)$", 
            fontsize=14.5, fontweight='bold', color='#24292F', ha='left', va='center', zorder=3)
    
    # 核心结论提示
    ax.text(info_box_x + 0.45, info_box_y + 0.65, 
            '三个边都是 Ω，\n同一个量纲才能构成三角形。', 
            fontsize=12, fontweight='bold', color='#C0392B', ha='left', va='center', linespacing=1.45, zorder=3)
    
    # 顶部总标题与整体画布水平中心对齐
    # x 范围有效宽度约 [0.3, 12.8]，中心约在 6.55
    ax.text(6.55, 4.75, '阻抗三角形', fontsize=16, fontweight='bold', color='#1A1A1A', ha='center', va='center')
    
    # 视区范围
    ax.set_xlim(0, 13.0)
    ax.set_ylim(0.2, 5.15)
    ax.set_aspect('equal')
    ax.axis('off')
    
    output_png = '/mnt/hdd/kimicode-projects/multisim-mcp/deliverables/figures-batch4/fig-ge-04.png'
    plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("PNG generated successfully at:", output_png)

if __name__ == "__main__":
    draw_impedance_triangle()
