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

d = schemdraw.Drawing()
# 测试 SourceControlledI 的箭头到底在哪个方向：
# 1. 默认向右 (theta=0)
s1 = elm.SourceControlledI().right().at((0, 0))
# 2. 向上 (theta=90)
s2 = elm.SourceControlledI().up().at((3, 0))
# 3. 向下 (theta=270)
s3 = elm.SourceControlledI().down().at((6, 3))
# 4. reverse 向下
s4 = elm.SourceControlledI(reverse=True).down().at((9, 3))

d.add(s1)
d.add(s2)
d.add(s3)
d.add(s4)
d.save("/tmp/test_sc_arrow_large.png", dpi=300)
