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
d.config(unit=2.0, lw=1.3, fontsize=12)

# 测试受控源在 schemdraw 中的完整连接与朝向：
# 在微变等效中：
# 上轨（集电极母线）: Y = 4.0
# 下轨（公共地线）: Y = 1.0
# 受控源应该从 (x, 1.0) 向上连到 (x, 4.0)，或者从 (x, 4.0) 向下连到 (x, 1.0)
# 让我们看看：
# 1. 为什么用户图里受控源往上飘到了标题？
# 因为它用了：elm.SourceControlledI().at((SRC_X, 4.0)).to((SRC_X, 1.0))
# 在 schemdraw 中，SourceControlledI 继承自 SourceControlled，它把 self.params['theta'] = 90！
# 结果 .to() 算出来角度之后又被内部 theta 干扰，导致方向完全反了（从 4.0 往上画到了 7.0）！
# 2. 正确画法：
# 从 (4, 1.0) 连到 (4, 4.0)，不带 .to()，或者使用 .down().at((4, 4.0)).length(3.0)！
# 让我们测试：
s_down = elm.SourceControlledI().down().at((4, 4.0)).length(3.0)
d.add(s_down)
print("s_down endpoints:", s_down.absanchors['start'], s_down.absanchors['end'])

d.save("/mnt/hdd/kimicode-projects/multisim-mcp/deliverables/figures-batch4/test_correct_sc.png", dpi=300)
