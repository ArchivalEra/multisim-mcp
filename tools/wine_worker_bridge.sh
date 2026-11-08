#!/usr/bin/env bash
# Wine COM worker bridge for multisim-mcp on Linux.
#
# The upstream frontend (com_worker_client._bootstrap_command) invokes:
#   $WORKER_PYTHON -c "<bootstrap>" --parent-pid <pid>
# On Linux the "32-bit Windows Python" is Wine's C:\Python310\python.exe, so
# this wrapper receives those arguments and re-executes them under wine.
# The bootstrap code is taken verbatim from argv (-c value) and path-mapped
# to Z:\... so the Wine-side Python can read the checkout.
#
# Frontend usage:
#   MULTISIM_MCP_WORKER_PYTHON=/path/to/tools/wine_worker_bridge.sh \
#   python -m multisim_mcp.server
#
# Environment:
#   MSIM_WINE_PREFIX   Wine prefix with Multisim 14.3 (default ~/.multisim143)
#   MSIM_WINE_DISPLAY  display for Multisim's GUI (default :88, Xvfb/Xephyr)
#   MSIM_WINE_PYTHON   Windows Python path (default C:\Python310\python.exe)
set -euo pipefail

WINE_PREFIX="${MSIM_WINE_PREFIX:-$HOME/.multisim143}"
WINE_DISPLAY="${MSIM_WINE_DISPLAY:-:-88}"
WINE_DISPLAY="${MSIM_WINE_DISPLAY:-:88}"
WORKER_PYTHON="${MSIM_WINE_PYTHON:-C:\\Python310\\python.exe}"

export WINEPREFIX="$WINE_PREFIX"
export DISPLAY="$WINE_DISPLAY"
export PATH="/opt/wine-stable/bin:$PATH"

bootstrap=""
parent_args=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    -c) bootstrap="$2"; shift 2 ;;
    --parent-pid)
      # The frontend's pid is a Linux pid; the Wine-side _pid_alive watchdog
      # cannot see it and kills the worker ~0.5s after start (os._exit(70)).
      # Disable the watchdog (0): worker lifetime is already bounded by
      # stdin EOF (run_worker returns) and the frontend's terminate.
      parent_args=("$1" "0"); shift 2 ;;
    *) parent_args=("$1"); shift ;;
  esac
done

# MultisimWorkerProcess(worker_command=[this-script]) passes no -c at all
# (_bootstrap_command only runs when worker_command is unset). Fall back to
# the same default bootstrap the frontend would have built.
if [[ -z "$bootstrap" ]]; then
  bootstrap="import runpy,sys;sys.path[:0]=['${MSIM_MCP_PACKAGE_DIR:-$(cd "$(dirname "$0")/../mcp_server" && pwd)}'];runpy.run_module('multisim_mcp.com_worker',run_name='__main__')"
fi

# Map POSIX paths inside the bootstrap to Wine's Z:\ drive form:
# '/mnt/hdd/...' inside a Python string literal → 'Z:\mnt\hdd\...'.
win_bootstrap="${bootstrap//Z:/Z:}"
if [[ "$bootstrap" == *"'/mnt/"* || "$bootstrap" == *"\"/mnt/"* || "$bootstrap" == *"'/home/"* ]]; then
  # Only rewrite path-like segments, not the whole code string.
  while [[ "$bootstrap" =~ (/mnt/[^\'\"]*|/home/[^\'\"]*) ]]; do
    posix="${BASH_REMATCH[1]}"
    win="Z:\\${posix//\//\\}"
    bootstrap="${bootstrap/$posix/$win}"
  done
fi
# Strip the accidental duplicate backslash produced by leading '/' mapping.
bootstrap="${bootstrap//Z:\\\\/Z:\\}"
bootstrap="${bootstrap//Z:\/\//Z:\\}"

exec wine "$WORKER_PYTHON" -c "$bootstrap" "${parent_args[@]}"
