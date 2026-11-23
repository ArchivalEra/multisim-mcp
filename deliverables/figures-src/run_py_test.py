import subprocess

script = """
import schemdraw
import schemdraw.elements as elm

# 1. 查找所有受控源相关和电容相关类
print("Source classes:", [k for k in dir(elm) if "Source" in k])
print("Capacitor classes:", [k for k in dir(elm) if "Capacitor" in k])

# 2. 检查 SourceControlledI
s = elm.SourceControlledI()
print("SourceControlledI params:", s.params)
print("segments:", len(s.segments))
"""

cmd = ["/tmp/figvenv/bin/python", "-c", script]
res = subprocess.run(cmd, capture_output=True, text=True)
print("OUT:\n", res.stdout)
print("ERR:\n", res.stderr)
