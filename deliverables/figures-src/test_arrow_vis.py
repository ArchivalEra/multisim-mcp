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

# 让我们测试受控源内部箭头在垂直状态下的表现
d = schemdraw.Drawing()
d.config(unit=2.0, lw=1.3)

# 1. 默认 SourceControlledI
s1 = elm.SourceControlledI().at((0, 0)).to((2, 0)) # 水平向右
d.add(s1)

# 2. 从 (4, 3) 垂直向下连到 (4, 0)
s2 = elm.SourceControlledI().at((4, 3)).to((4, 0))
d.add(s2)

# 3. 从 (7, 0) 垂直向上连到 (7, 3)
s3 = elm.SourceControlledI().at((7, 0)).to((7, 3))
d.add(s3)

d.save("/tmp/test_arrow_vis.png", dpi=300)
print("Saved /tmp/test_arrow_vis.png")
