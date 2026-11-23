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
# Let's inspect SourceControlledI:
# When SourceControlledI is created, its default orientation is theta=0 (horizontal, pointing right).
# If we do .down(), it rotates 90 degrees clockwise (theta=-90 or 270).
# Let's see:
s = elm.SourceControlledI().down().at((2, 4)).length(2.5)
d.add(s)
d.save("/mnt/hdd/kimicode-projects/multisim-mcp/deliverables/figures-batch4/test_pure_down.png", dpi=300)
