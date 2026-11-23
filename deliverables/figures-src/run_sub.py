import subprocess
import sys

# Test executing python script via subprocess using the target python
cmd = ["/tmp/figvenv/bin/python", "-c", "import schemdraw; print('schemdraw ok', schemdraw.__version__)"]
res = subprocess.run(cmd, capture_output=True, text=True)
print("stdout:", res.stdout)
print("stderr:", res.stderr)
print("rc:", res.returncode)
