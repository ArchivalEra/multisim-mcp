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
# 让我们看看 schemdraw 的 SourceControlledI 到底是怎样的：
s = elm.SourceControlledI()
for i, seg in enumerate(s.segments):
    print(f"seg[{i}]: path={seg.path}, arrow={getattr(seg, 'arrow', None)}")

# 重点看箭头的定义：Segment([(0.25, 0), (0.75, 0)], arrow='->')
# 注意！菱形是 (0,0) -> (0.5, 0.5) -> (1, 0) -> (0.5, -0.5) -> (0,0)
# 中心的箭头是从 (0.25, 0) 到 (0.75, 0)，指向 x 正方向！
# 也就是说，Element 沿主轴方向（从 start 到 end）走！
# 当 element 是从下往上 (dy > 0, theta = 90) 时，箭头指向 +y（向上）！
# 当 element 是从上往下时，为什么之前 theta 会变成向上或者 end 跑到 7.0？
# 让我们看下面的测试：
s_down = elm.SourceControlledI().at((2, 4)).to((2, 1))
print("s_down theta:", s_down.theta)
print("s_down endpoints:", s_down.absanchors['start'], s_down.absanchors['end'])
