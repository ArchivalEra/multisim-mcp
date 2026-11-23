import schemdraw
import schemdraw.elements as elm

d = schemdraw.Drawing()
# 仔细观察：
# 为什么之前的图里，受控电流源会画到上面去？
# 因为它用了：elm.SourceControlledI().at((SRC_X, AC_TOP_Y)).to((SRC_X, GND_Y))
# 在 schemdraw 中，Element2Term 只有当起点在下，终点在上时才是 theta=90。
# 当起点在上 (4.0)，终点在下 (1.2) 时，如果调用了错误的方法，或者没有调用正确的 .reverse() 或 .down()，位置就会错乱！
# 让我们在独立测试脚本中验证各种正确的写法：
s = elm.SourceControlledI().down().at((2, 4)).to((2, 1))
print("s endpoints:", s.endpoints)
d.add(s)
d.save("/tmp/test_sc_correct.png")
