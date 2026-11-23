import schemdraw
import schemdraw.elements as elm

d = schemdraw.Drawing()
# 让我们看看 schemdraw 的 SourceControlledI 尺寸到底是多少：
s = elm.SourceControlledI()
print("s segments:")
for seg in s.segments:
    print(seg.path, getattr(seg, "arrow", None))

# 默认的菱形顶点只有：
# Point(0,0), Point(0.5,0.5), Point(1,0), Point(0.5,-0.5), Point(0,0)
# 宽度只有 1.0 个绘图单位，高度只有 1.0 个绘图单位！
# 如果 unit=2.0 甚至 1.0，这只有 10~20 个像素！线宽 1.3 的时候直接糊成黑色小方块！
# 来看参数：
print("s defaults:", s._element_defaults)
