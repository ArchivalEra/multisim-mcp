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

# 左右两轨
d.add(elm.Line().at((0, 4)).to((6, 4)))
d.add(elm.Line().at((0, 1)).to((6, 1)))

# 观察 SourceControlledI 从 (2, 1) 到 (2, 4)：
# 它的起点是 (2, 1)，终点是 (2, 4)
# 箭头方向是从起点指向终点，即向上 (1 -> 4)
# 如果我们想要箭头向下：
# 起点应该是 (2, 4)，终点应该是 (2, 1)！
# 为什么之前在 (11.6, 4.0) 到 (11.6, 1.2) 会画到上面去？
# 让我们看看下面这行代码实际画在哪里：
s_down = elm.SourceControlledI().at((3, 4)).to((3, 1))
d.add(s_down)

d.save("/mnt/hdd/kimicode-projects/multisim-mcp/deliverables/figures-batch4/test_diag.png")
