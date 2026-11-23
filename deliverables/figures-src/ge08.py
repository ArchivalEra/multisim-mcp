#!/usr/bin/env python3
"""fig-ge-08 共射放大：直流通路与微变等效（交流通路）对齐比较工程图。
严格遵循要求：
1. 器件全使用现成 schemdraw 符号库（BjtNpn, Resistor, Capacitor, SourceControlledI, SourceV, Ground 等）。
2. 左栏三极管为标准竖直 NPN：基极横线在左（接 Rb）、集电极在上（接 Rc 到 Vcc）、发射极在右下带向外箭头直接接地。
3. 右栏微变等效电路：输入端为基极与地之间的 rbe，受控源 βIb 从 C 流向 E（向下），并联 ro 以及交流接地后的集电极负载电阻 Rc，输出端接 C、E。
4. 明确标注 ri 输入电阻区间（在微变等效输入端清晰标出由 B、E 两端看入的 ri 与区间线/看入箭头），并标出 ro。
5. 两栏之间设分界虚线，保留「大写算工作点」「小写算放大」两句话，绝不与任何电路文字重叠。
6. 无压字无压线（通过 collide3, overlaptext, whiten 检查）。
"""
import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["Noto Sans CJK SC"] + list(
    matplotlib.rcParams["font.sans-serif"]
)
matplotlib.rcParams["savefig.transparent"] = False
matplotlib.rcParams["savefig.facecolor"] = "white"

import schemdraw
import schemdraw.elements as elm
from PIL import Image

OUT = "/mnt/hdd/kimicode-projects/multisim-mcp/deliverables/figures-batch4/fig-ge-08.png"

d = schemdraw.Drawing()
d.config(unit=3.0, lw=1.4, fontsize=13)

# ---------------- 基准高度与水平网格规划 ----------------
# 标题行 Y = 6.2
# 左栏电源与上母线 Y = 4.8
# 公共地线高度 GND_Y = 1.0
GND_Y = 1.0

# ==================== 左栏：直流通路（电容视为断开） ====================
d.add(elm.Label().at((3.2, 6.2)).label("直流通路（电容视为断开）", fontsize=15, halign="center"))

# 1. 直流电源 Vcc 支路 (x = 0.8)
d.add(elm.SourceV().up().at((0.8, GND_Y)).to((0.8, 4.8)))
d.add(elm.Label().at((0.25, 3.2)).label("$V_{CC}$", fontsize=13, halign="right"))
d.add(elm.Ground().at((0.8, GND_Y)))
d.add(elm.Dot().at((0.8, 4.8)))

# 4. NPN 三极管先加入画布确定位置与绝对引脚坐标 (x = 3.6, y = 2.2)
q1 = d.add(elm.BjtNpn(circle=True).right().at((3.6, 2.2)))
rc_x = q1.absanchors["collector"].x

# 2. Vcc 顶部母线 (连接到 Rb 与 Rc，严格止于 rc_x，绝不向右冒头)
d.add(elm.Line().right().at((0.8, 4.8)).to((rc_x, 4.8)))

# 3. Rb 偏置电阻支路 (x = 2.2)
d.add(elm.Dot().at((2.2, 4.8)))
d.add(elm.Resistor().down().at((2.2, 4.8)).to((2.2, 3.0)))
d.add(elm.Label().at((1.65, 3.9)).label("$R_b$", fontsize=13, halign="right"))

# 基极引线连接：从 Rb 底部 (2.2, 3.0) 垂直引至 q1 基极水平线，再横向接入基极
q_base_pt = q1.absanchors["base"]
d.add(elm.Line().down().at((2.2, 3.0)).to((2.2, q_base_pt.y)))
d.add(elm.Line().right().at((2.2, q_base_pt.y)).to(q_base_pt))

# 5. Rc 集电极电阻支路
q_coll_pt = q1.absanchors["collector"]
rc_node = (rc_x, 3.4)
d.add(elm.Dot().at((rc_x, 4.8)))
d.add(elm.Resistor().down().at((rc_x, 4.8)).to(rc_node).label("$R_c$", loc="right"))
d.add(elm.Dot().at(rc_node))
# Rc 底部垂直连入三极管集电极
d.add(elm.Line().down().at(rc_node).to(q_coll_pt))

# 6. 发射极垂直引线下地
q_emit_pt = q1.absanchors["emitter"]
d.add(elm.Line().down().at(q_emit_pt).to((q_emit_pt.x, GND_Y)))
d.add(elm.Ground().at((q_emit_pt.x, GND_Y)))

# 7. 输出耦合电容画成断开样式并标「C（断开）」
c_lead_1 = (rc_x + 0.4, rc_node[1])
c_open_1 = (rc_x + 0.8, rc_node[1])
c_open_2 = (rc_x + 1.8, rc_node[1])
c_lead_out = (rc_x + 2.3, rc_node[1])

d.add(elm.Line().right().at(rc_node).to(c_lead_1))
d.add(elm.Dot(open=True).at(c_lead_1))
d.add(elm.Capacitor().right().at(c_open_1).to(c_open_2).label("C (断开)", loc="top"))
d.add(elm.Dot(open=True).at(c_open_2))
d.add(elm.Line().right().at(c_open_2).to(c_lead_out))
d.add(elm.Dot(open=True).at(c_lead_out))

# 8. 左栏底部标：Q 点
d.add(elm.Label().at((3.2, -0.4)).label("Q 点：$I_{BQ}$、$I_{CQ}$、$U_{CEQ}$", fontsize=13, halign="center"))


# ==================== 中间分割虚线与两侧竖排文字 ====================
SEP_X = 7.7
d.add(elm.Line().down().at((SEP_X, 5.8)).to((SEP_X, 0.4)).style(ls="--", color="#888888", lw=1.2))

# 虚线两侧竖排文字
txt_left = "大\n写\n算\n工\n作\n点"
txt_right = "小\n写\n算\n放\n大"
d.add(elm.Label().at((SEP_X - 0.45, 3.1)).label(txt_left, fontsize=13, halign="center", color="#333333"))
d.add(elm.Label().at((SEP_X + 0.45, 3.1)).label(txt_right, fontsize=13, halign="center", color="#333333"))


# ==================== 右栏：微变等效（交流通路） ====================
d.add(elm.Label().at((15.4, 6.2)).label("微变等效（交流通路）", fontsize=15, halign="center"))

AC_TOP_Y = 3.6
PORT_B_X = 11.2
RBE_X = 12.5
SRC_X = 14.3
RO_X = 16.5
RC_AC_X = 18.2
PORT_C_X = 19.4

# 1. 输入端口 B 与 ri 测量区间指示
d.add(elm.Dot(open=True).at((PORT_B_X, AC_TOP_Y)).label("B", loc="left"))
d.add(elm.Dot(open=True).at((PORT_B_X, GND_Y)).label("E", loc="left"))

# ri 测量范围指示：
# 在 PORT_B_X 左侧画出跨接在 B 与 E 之间的测量范围区间线与看入箭头
BRACKET_X = PORT_B_X - 0.5
d.add(elm.Line().at((PORT_B_X - 0.2, AC_TOP_Y)).to((BRACKET_X, AC_TOP_Y)).style(color="#555555", lw=1.0))
d.add(elm.Line().at((BRACKET_X, AC_TOP_Y)).to((BRACKET_X, GND_Y)).style(color="#555555", lw=1.0))
d.add(elm.Line().at((BRACKET_X, GND_Y)).to((PORT_B_X - 0.2, GND_Y)).style(color="#555555", lw=1.0))
# 向右看入微变等效电路的箭头线
MID_Y = (AC_TOP_Y + GND_Y) / 2
d.add(elm.Arrow().right().at((BRACKET_X, MID_Y)).to((PORT_B_X - 0.1, MID_Y)).style(color="#333333", lw=1.1))
# ri 标签放置在区间线外侧左边，与「小写算放大」(SEP_X=7.7) 间隔充分
d.add(elm.Label().at((BRACKET_X - 0.2, MID_Y)).label(r"$r_i$", fontsize=13, halign="right"))

# 输入端相连到 rbe（输入顶轨止于此，绝不向右延伸——B 与 C 只能靠受控源耦合）
d.add(elm.Line().right().at((PORT_B_X, AC_TOP_Y)).to((RBE_X, AC_TOP_Y)))
d.add(elm.Dot().at((RBE_X, AC_TOP_Y)))

# 控制电流 Ib 方向：自 B 流向 E，箭头画在输入线上方
d.add(elm.Arrow().right().at((PORT_B_X + 0.4, AC_TOP_Y + 0.3)).to((RBE_X - 0.4, AC_TOP_Y + 0.3)).style(color="#333333", lw=1.1))
d.add(elm.Label().at(((PORT_B_X + RBE_X) / 2, AC_TOP_Y + 0.75)).label(r"$I_b$", fontsize=12, halign="center"))

# rbe 支路 (垂直向下连接至下轨地线)
d.add(elm.Resistor().down().at((RBE_X, AC_TOP_Y)).to((RBE_X, GND_Y)))
d.add(elm.Label().at((RBE_X - 0.4, MID_Y)).label(r"$r_{be}$", fontsize=13, halign="right"))
d.add(elm.Dot().at((RBE_X, GND_Y)))

# 2. 受控电流源 βIb 支路（输出顶轨从受控源顶端开始，与输入顶轨完全断开）：
# 从交流集电极母线 (C) 向下流向公共发射极地线 (E)
d.add(elm.Dot().at((SRC_X, AC_TOP_Y)))
d.add(elm.Line().down().at((SRC_X, AC_TOP_Y)).to((SRC_X, 2.8)))

src_elem = elm.SourceControlledI().down().at((SRC_X, 2.8)).length(1.0)
d.add(src_elem)
d.add(elm.Line().down().at((SRC_X, 1.8)).to((SRC_X, GND_Y)))
d.add(elm.Dot().at((SRC_X, GND_Y)))

# 受控源标签 βIb：放置在受控源右侧
d.add(elm.Label().at((SRC_X + 0.65, 2.3)).label(r"$\beta I_b$", fontsize=13, halign="left"))

# 3. 输出电阻 ro (rce) 支路 (RO_X = 16.5, 与 SRC_X + 0.65 错开 1.5 以上)
d.add(elm.Line().right().at((SRC_X, AC_TOP_Y)).to((RO_X, AC_TOP_Y)))
d.add(elm.Dot().at((RO_X, AC_TOP_Y)))
d.add(elm.Resistor().down().at((RO_X, AC_TOP_Y)).to((RO_X, GND_Y)))
d.add(elm.Label().at((RO_X - 0.4, MID_Y)).label(r"$r_o$", fontsize=13, halign="right"))
d.add(elm.Dot().at((RO_X, GND_Y)))

# 4. 交流接地的集电极电阻 Rc 支路 (Vcc交流接地后 Rc 与 ro 并联)
d.add(elm.Line().right().at((RO_X, AC_TOP_Y)).to((RC_AC_X, AC_TOP_Y)))
d.add(elm.Dot().at((RC_AC_X, AC_TOP_Y)))
d.add(elm.Resistor().down().at((RC_AC_X, AC_TOP_Y)).to((RC_AC_X, GND_Y)).label(r"$R_c$", loc="right"))
d.add(elm.Dot().at((RC_AC_X, GND_Y)))

# 5. 交流输出端口 C 与 E
d.add(elm.Line().right().at((RC_AC_X, AC_TOP_Y)).to((PORT_C_X, AC_TOP_Y)))
d.add(elm.Dot(open=True).at((PORT_C_X, AC_TOP_Y)).label("C", loc="right"))

# 6. 公共发射极地线 (下母线)
d.add(elm.Line().right().at((PORT_B_X, GND_Y)).to((PORT_C_X, GND_Y)))
d.add(elm.Dot(open=True).at((PORT_C_X, GND_Y)).label("E", loc="right"))

# 交流接地符号（居中位于公共发射极地线下侧）
d.add(elm.Ground().at(((RBE_X + SRC_X) / 2, GND_Y)))

# 7. 右侧四行说明
INFO_X = 20.6
INFO_Y = 4.2
d.add(elm.Label().at((INFO_X, INFO_Y)).label(r"$A_u$ 电压放大", fontsize=13, halign="left"))
d.add(elm.Label().at((INFO_X, INFO_Y - 0.75)).label(r"$r_i$ 输入电阻", fontsize=13, halign="left"))
d.add(elm.Label().at((INFO_X, INFO_Y - 1.50)).label(r"$r_o$ 输出电阻", fontsize=13, halign="left"))
d.add(elm.Label().at((INFO_X, INFO_Y - 2.25)).label("直流源按交流接地", fontsize=13, halign="left"))

# 保存图像
d.save(OUT, dpi=300)

# 转纯白底 RGB 保证无透明层与发虚问题
im = Image.open(OUT)
if im.mode != "RGB":
    bg = Image.new("RGB", im.size, (255, 255, 255))
    if im.mode == "RGBA":
        bg.paste(im, mask=im.split()[3])
    else:
        bg.paste(im)
    bg.save(OUT)

print("Saved cleanly to:", OUT)
