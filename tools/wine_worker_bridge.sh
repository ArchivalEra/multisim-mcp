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
#   MSIM_WINE_DISPLAY  X11 display fallback (default :88, Xvfb/Xephyr)
#   MSIM_WINE_PYTHON   Windows Python path (default C:\Python310\python.exe)
#   MSIM_FORCE_BACKEND wayland|x11 — otherwise: wayland when a compositor
#                      socket is reachable (Wine 11 winewayland.drv composites
#                      straight onto the real desktop), X11 fallback. The COM
#                      automation itself needs no visible window; the display
#                      choice only decides where Multisim's GUI appears.
set -euo pipefail

WINE_PREFIX="${MSIM_WINE_PREFIX:-$HOME/.multisim143}"
XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
export XDG_RUNTIME_DIR
WORKER_PYTHON="${MSIM_WINE_PYTHON:-C:\\Python310\\python.exe}"

export WINEPREFIX="$WINE_PREFIX"
# Node/libuv under Wine fails on pipe stdio; the vendored codec path reads
# temp files instead. Keep it on for this bridge unconditionally.
export MULTISIM_MCP_WINE_COMPAT=1
# Wine-side codec: node.exe lives in system32, decoder in C:\codec. The
# frontend may also point MULTISIM_MCP_EWD/EWE at host paths for a Linux
# node — those are only meaningful to the Linux frontend, never to this
# worker, so the Wine-side paths must win inside the worker.
export MULTISIM_MCP_EWD='C:\codec\ewd.js'
export MULTISIM_MCP_EWE='C:\codec\ewe.js'
export PATH="$PATH:/opt/wine-stable/bin"
export PATH="/opt/wine-stable/bin:$PATH"

force="${MSIM_FORCE_BACKEND:-}"
want_wayland() {
  [ -n "${WAYLAND_DISPLAY:-}" ] && return 0
  [ -S "$XDG_RUNTIME_DIR/wayland-0" ] && return 0
  return 1
}
case "$force" in
  wayland)
    export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-0}"
    unset DISPLAY
    ;;
  x11)
    export DISPLAY="${MSIM_WINE_DISPLAY:-:88}"
    ;;
  "")
    if want_wayland; then
      export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-0}"
      unset DISPLAY
    else
      export DISPLAY="${MSIM_WINE_DISPLAY:-:88}"
    fi
    ;;
  *)
    echo "wine_worker_bridge.sh: unknown MSIM_FORCE_BACKEND '$force'" >&2
    exit 2
    ;;
esac

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
