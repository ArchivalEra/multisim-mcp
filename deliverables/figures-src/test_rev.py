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

# 观察 SourceControlledI
# 在 schemdraw 中，SourceControlledI 从 (x, y1) 到 (x, y2)：
# 如果起点是 y=1.2, 终点是 y=4.0:
# start=(x, 1.2), end=(x, 4.0)，箭头朝上！
# 如果起点是 y=4.0, 终点是 y=1.2:
# 刚才的图里，受控源竟然从 4.0 往上画到了 6.8！为什么？
# 因为 schemdraw 的 Element2Term 在 .to() 时，计算 dy = 1.2 - 4.0 = -2.8, theta = -90
# 但是它的内部 transform 是顺时针还是逆时针旋转？
# 让我们测试不同的写法，直接把正确的受控源画出来：
s1 = elm.SourceControlledI().at((2, 1.2)).to((2, 4.0)).reverse()
d.add(s1)

d.save("/mnt/hdd/kimicode-projects/multisim-mcp/deliverables/figures-batch4/test_rev.png")
print("Saved test_rev")
