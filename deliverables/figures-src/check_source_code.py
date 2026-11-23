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

def inspect_source_code():
    import inspect
    print("SourceControlled:")
    print(inspect.getsource(elm.SourceControlled))
    print("="*40)
    print("SourceControlledI:")
    print(inspect.getsource(elm.SourceControlledI))

if __name__ == "__main__":
    inspect_source_code()
