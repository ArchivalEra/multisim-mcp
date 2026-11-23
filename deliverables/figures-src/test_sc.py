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

def test_source_and_cap():
    # 测试受控源在 schemdraw 中垂直放置与箭头方向
    d = schemdraw.Drawing()
    
    # 1. 默认 SourceControlledI 指向右
    s1 = elm.SourceControlledI().right().label("right (0°)")
    d.add(s1)
    
    # 2. 向上: up() 或 theta=90
    s2 = elm.SourceControlledI().up().at((3, 0)).label("up (90°)")
    d.add(s2)
    
    # 3. 向下: down() 或 theta=270
    s3 = elm.SourceControlledI().down().at((6, 3)).label("down (270°)")
    d.add(s3)
    
    # 4. 电容断开测试
    c = elm.Capacitor().at((9, 1)).to((11, 1)).label("C (断开)", loc="top")
    d.add(c)
    
    d.save("/mnt/hdd/kimicode-projects/multisim-mcp/deliverables/figures-batch4/test_elements.png")
    print("Saved test_elements.png")

if __name__ == "__main__":
    test_source_and_cap()
