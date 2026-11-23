import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["Noto Sans CJK SC"] + list(
    matplotlib.rcParams["font.sans-serif"]
)
matplotlib.rcParams["savefig.transparent"] = False

import schemdraw
import schemdraw.elements as elm

d = schemdraw.Drawing()
d.config(unit=2.0, lw=1.3, fontsize=12)

# 测试各器件：
# 1. BjtNpn
q = elm.BjtNpn(circle=True).at((3, 3))
d.add(q)

# 2. Resistor
r = elm.Resistor().at((1, 3)).to((1, 1)).label("$R_1$")
d.add(r)

# 3. SourceControlledI 向上还是向下？
# 当从 (6, 1) 连到 (6, 4) 时：arrow points from 1 to 4 (UP)
# 当从 (8, 4) 连到 (8, 1) 时：arrow points from 4 to 1 (DOWN)
s_up = elm.SourceControlledI().at((6, 1)).to((6, 4)).label("UP", loc="right")
d.add(s_up)

s_down = elm.SourceControlledI().at((8, 4)).to((8, 1)).label("DOWN", loc="right")
d.add(s_down)

# 4. 电容断开样式：
# 断开样式：用 elm.Capacitor，但两侧极板断开或带有断开标记
# 题目要求：
# 输出耦合电容画成断开样式并标「C（断开）」
# 标了「断开」但电容符号还画成完整电容 -> 属于常见错误！
# 器件必须用 schemdraw 现成器件：elm.BjtNpn、elm.Resistor、elm.Capacitor、elm.SourceControlledI、elm.Ground。不许用 Line 拼出器件形状。
c = elm.Capacitor().at((10, 3)).to((12, 3)).label("C (断开)", loc="top")
d.add(c)

d.save("/mnt/hdd/kimicode-projects/multisim-mcp/deliverables/figures-batch4/test_run.png")
print("Saved test_run.png successfully")
