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
# Let's inspect how to draw a controlled current source from top to bottom
# In schemdraw:
# SourceControlledI:
# When drawn with .down(), theta=-90.
# Where is the arrow pointing?
# Let's check segments of SourceControlledI().down()!
s = elm.SourceControlledI().down().at((0, 4)).length(3)
d.add(s)
d.save("/mnt/hdd/kimicode-projects/multisim-mcp/deliverables/figures-batch4/test_sc_down.png")
