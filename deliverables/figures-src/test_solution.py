import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["Noto Sans CJK SC"] + list(
    matplotlib.rcParams["font.sans-serif"]
)
matplotlib.rcParams["savefig.transparent"] = False

import schemdraw
import schemdraw.elements as elm

def main():
    # 测试如何在 schemdraw 中正确绘制断开电容和受控源
    # 1. 断开电容：
    # 题目：输出耦合电容画成断开样式并标「C（断开）」
    # 避坑：标了「断开」但电容符号还画成完整电容。器件必须用 schemdraw 现成器件：elm.Capacitor。
    # 怎么把 elm.Capacitor 画成断开样式？
    # 方案：断开样式通常是在电容极板或引脚处断开，或者电容的一极悬空断开！
    # 比如：左引脚连到左极板，右极板断开留出间隙（开路圈圈）！
    # 在 schemdraw 中，可以放一个 elm.Capacitor，但右端断开不闭合，或者用打断线示意！
    pass

if __name__ == "__main__":
    main()
