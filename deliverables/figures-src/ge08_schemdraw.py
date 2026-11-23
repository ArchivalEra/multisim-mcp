#!/usr/bin/env python3
"""fig-ge-08 共射放大：左直流通路、右微变等效。
高校模电教材级工程图规范，绝对坐标精确定位，白底不透明 RGB 输出。
"""
import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["Noto Sans CJK SC"] + list(
    matplotlib.rcParams["font.sans-serif"]
)
matplotlib.rcParams["savefig.transparent"] = False
matplotlib.rcParams["savefig.facecolor"] = "white"

import schemdraw  # noqa: E402
import schemdraw.elements as elm  # noqa: E402
from PIL import Image  # noqa: E402

OUT = "/mnt/hdd/kimicode-projects/multisim-mcp/deliverables/figures-batch4/fig-ge-08.png"

d = schemdraw.Drawing()
d.config(unit=2.0, lw=1.3, fontsize=12)

# ========================================================
# 坐标系统设计：
# 标题行：Y = 7.2
# Vcc 顶轨 / 交流输入输出对齐高度：
#   左栏 Vcc 顶轨：Y = 5.8
#   左栏 Rc/Rb 顶端：Y = 5.8
#   右栏微变等效上轨：Y = 4.0
#   共用地轨 / 发射极对齐高度：Y = 1.2
# ========================================================

GND_Y = 1.2

# ==================== 左栏：直流通路 ====================
# 标题
d.add(elm.Label().at((2.8, 7.2)).label("直流通路（电容视为断开）", fontsize=14, halign="center"))

# 直流电源 Vcc (放在最左侧 x = 0.8)
d.add(elm.SourceV().at((0.8, GND_Y)).to((0.8, 5.8)).label("$V_{CC}$", loc="left"))
d.add(elm.Ground().at((0.8, GND_Y)))
d.add(elm.Dot().at((0.8, 5.8)))

# Vcc 顶部分支母线
d.add(elm.Line().at((0.8, 5.8)).to((4.4, 5.8)))
d.add(elm.Dot().at((2.2, 5.8)))
d.add(elm.Dot().at((4.4, 5.8)))

# Rb 支路 (x = 2.2)
d.add(elm.Resistor().at((2.2, 5.8)).to((2.2, 3.4)).label("$R_b$", loc="left"))

# NPN 三极管 (正常朝向：base 在左，collector 在右上，emitter 在右下)
# 显式创建独立的 BjtNpn 实例，绝不链式调用旋转
q1 = elm.BjtNpn(circle=True).at((3.4, 2.4))
d.add(q1)

# 基极连线：从 Rb 底部 (2.2, 3.4) 垂直向下至基极高度 (2.2, q1.base[1])，再水平连到 q1.base
d.add(elm.Line().at((2.2, 3.4)).to((2.2, q1.base[1])))
d.add(elm.Line().at((2.2, q1.base[1])).to(q1.base))

# Rc 支路 (位于集电极正上方 x = q1.collector[0])
rc_x = q1.collector[0]
rc_node = (rc_x, 4.0)
d.add(elm.Resistor().at((rc_x, 5.8)).to(rc_node).label("$R_c$", loc="right"))
d.add(elm.Dot().at(rc_node))

# 从 Rc 底部节点直接垂直引线连到三极管 collector
d.add(elm.Line().at(rc_node).to(q1.collector))

# 发射极垂直引线向下接地
d.add(elm.Line().at(q1.emitter).to((q1.emitter[0], GND_Y)))
d.add(elm.Ground().at((q1.emitter[0], GND_Y)))

# 输出端与断开的电容 C：从 Rc 底部节点向右引出
# 规范的断开画法：开路两端带有小圆圈端子，中间断开一段距离，标注 C (断开)
out_dot_left = (rc_x + 0.6, rc_node[1])
out_dot_right = (rc_x + 1.6, rc_node[1])
d.add(elm.Line().at(rc_node).to(out_dot_left))
d.add(elm.Dot(open=True).at(out_dot_left))
d.add(elm.Gap().at(out_dot_left).to(out_dot_right).label("C (断开)", loc="top"))
d.add(elm.Dot(open=True).at(out_dot_right))
d.add(elm.Line().at(out_dot_right).to((out_dot_right[0] + 0.6, rc_node[1])))

# 左栏底部文字：Q 点
d.add(elm.Label().at((2.8, 0.2)).label("Q 点：$I_{BQ}$、$I_{CQ}$、$U_{CEQ}$", fontsize=12, halign="center"))


# ==================== 中间分割虚线与竖排文字 ====================
SEP_X = 7.2
d.add(elm.Line().at((SEP_X, 6.7)).to((SEP_X, 0.5)).style(ls="--", color="#888888", lw=1.2))

# 竖排文字：虚线左侧“大写算工作点”，虚线右侧“小写算放大”
txt_left = "大\n写\n算\n工\n作\n点"
txt_right = "小\n写\n算\n放\n大"
d.add(elm.Label().at((SEP_X - 0.45, 3.6)).label(txt_left, fontsize=12, halign="center", color="#333333"))
d.add(elm.Label().at((SEP_X + 0.45, 3.6)).label(txt_right, fontsize=12, halign="center", color="#333333"))


# ==================== 右栏：微变等效（交流通路） ====================
# 标题
d.add(elm.Label().at((11.8, 7.2)).label("微变等效（交流通路）", fontsize=14, halign="center"))

# 微变等效模型拓扑：
# 上轨（交流集电极母线）：Y = 4.0
# 下轨（公共发射极地线）：Y = 1.2
# 支路位置：
# B 端子：x = 8.2
# r_be 支路：x = 9.4，接在输入 B 与公共地 E 之间
# 受控电流源 βIb：x = 11.6，从上轨流向下轨（方向向下，从 C 流向 E）
# r_o 支路：x = 13.2，在输出侧并联在 C 与 E 之间
# C 端子：x = 14.2

AC_TOP_Y = 4.0
B_TERM_X = 8.2
RBE_X = 9.4
SRC_X = 11.6
RO_X = 13.2
C_TERM_X = 14.2

# 1. 输入端口 B
d.add(elm.Dot(open=True).at((B_TERM_X, AC_TOP_Y)).label("B", loc="left"))
d.add(elm.Line().at((B_TERM_X, AC_TOP_Y)).to((RBE_X, AC_TOP_Y)))
d.add(elm.Dot().at((RBE_X, AC_TOP_Y)))

# r_be 支路 (垂直向下连接至下轨)
d.add(elm.Resistor().at((RBE_X, AC_TOP_Y)).to((RBE_X, GND_Y)).label("$r_{be}$", loc="left"))

# 2. 受控电流源 βIb：
# 从上轨 (C) 向下流向下轨 (E)，电流源内部菱形箭头必须向下
# schemdraw SourceControlledI 默认内部箭头从 start 指向 end
# 因此 start=(SRC_X, AC_TOP_Y), end=(SRC_X, GND_Y) 时，箭头向下
d.add(elm.Dot().at((SRC_X, AC_TOP_Y)))
d.add(elm.SourceControlledI().at((SRC_X, AC_TOP_Y)).to((SRC_X, GND_Y)).label(r"$\beta I_b$", loc="right"))

# 3. 输出电阻 r_o 支路
d.add(elm.Line().at((SRC_X, AC_TOP_Y)).to((RO_X, AC_TOP_Y)))
d.add(elm.Dot().at((RO_X, AC_TOP_Y)))
d.add(elm.Resistor().at((RO_X, AC_TOP_Y)).to((RO_X, GND_Y)).label("$r_o$", loc="right"))

# 4. 输出端 C
d.add(elm.Line().at((RO_X, AC_TOP_Y)).to((C_TERM_X, AC_TOP_Y)))
d.add(elm.Dot(open=True).at((C_TERM_X, AC_TOP_Y)).label("C", loc="right"))

# 5. 公共发射极地线 (E)
d.add(elm.Dot(open=True).at((B_TERM_X, GND_Y)).label("E", loc="left"))
d.add(elm.Line().at((B_TERM_X, GND_Y)).to((C_TERM_X, GND_Y)))
d.add(elm.Dot().at((RBE_X, GND_Y)))
d.add(elm.Dot().at((SRC_X, GND_Y)))
d.add(elm.Dot().at((RO_X, GND_Y)))
d.add(elm.Dot(open=True).at((C_TERM_X, GND_Y)).label("E", loc="right"))

# 交流接地符号（只画一个，居中位于受控源下方）
d.add(elm.Ground().at((SRC_X, GND_Y)))

# 6. 右侧参数与说明（4行分立放置，真实换行，布局平衡）
INFO_X = 15.2
INFO_Y = 4.8
d.add(elm.Label().at((INFO_X, INFO_Y)).label(r"$A_u$ 电压放大", fontsize=12, halign="left"))
d.add(elm.Label().at((INFO_X, INFO_Y - 0.75)).label(r"$r_i$ 输入电阻", fontsize=12, halign="left"))
d.add(elm.Label().at((INFO_X, INFO_Y - 1.50)).label(r"$r_o$ 输出电阻", fontsize=12, halign="left"))
d.add(elm.Label().at((INFO_X, INFO_Y - 2.25)).label("直流源按交流接地", fontsize=12, halign="left"))

# 保存并输出图像
d.save(OUT, dpi=300)

# 确保为 100% 白底不透明 RGB 图像
im = Image.open(OUT)
if im.mode != "RGB":
    bg = Image.new("RGB", im.size, (255, 255, 255))
    if im.mode == "RGBA":
        bg.paste(im, mask=im.split()[3])
    else:
        bg.paste(im)
    bg.save(OUT)

print("Iteration 3 generated successfully:", OUT)
