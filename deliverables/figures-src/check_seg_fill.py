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

def inspect():
    # 测试在默认和放大 unit 下，SourceControlledI 的菱形内部到底是不是透明的：
    d = schemdraw.Drawing()
    s = elm.SourceControlledI()
    print("s default fill:", s.params.get("fill"))
    for i, seg in enumerate(s.segments):
        print(f"seg {i}:", seg.path, "fill:", getattr(seg, "fill", None), "arrow:", getattr(seg, "arrow", None))

if __name__ == "__main__":
    inspect()
