# Running multisim-mcp on Linux (Wine bridge)

This fork adds a Linux bridge so the MCP frontend can drive a Wine-installed
Multisim 14.3 through the exact same COM worker protocol used on Windows.
No upstream source files are modified; everything lives in
`tools/wine_worker_bridge.sh` plus environment variables.

## How it works

- The Multisim COM server (`MultisimInterface.MultisimApp`) is an in-process
  32-bit DLL (`MSInterface.dll`). Any 32-bit COM client inside the same Wine
  prefix can load it directly — verified working under Wine 11.
- `tools/wine_worker_bridge.sh` pretends to be the "32-bit Windows Python"
  that `com_worker_client._python_prefix()` expects. It re-executes the
  frontend's bootstrap inside `wine C:\Python310\python.exe`, maps POSIX paths
  in the bootstrap code to Wine's `Z:\` drive, and disables the parent-pid
  watchdog (a Linux pid is invisible to the Wine-side `_pid_alive`, which
  would otherwise kill the worker ~0.5 s after startup).
- The frontend (MCP server, CLI, tests) runs as native Linux Python; the JSON
  stdio protocol crosses the Wine boundary unchanged.

## One-time setup (done on this machine)

1. Multisim 14.3 installed in `~/.multisim143` (see the multisim-linux repo).
2. 32-bit Windows Python 3.10.11 installed into the prefix at `C:\Python310`
   (python.org's last 32-bit installer; 3.9 and earlier lack
   `dataclass(slots=True)`, 3.11+ has no 32-bit build):
   ```bash
   wine python-3.10.11.exe /quiet InstallAllUsers=0 TargetDir="C:\Python310" \
     Include_test=0 AssociateFiles=0 Shortcuts=0
   ```
3. Inside that Wine Python: `pywin32==306` and `typing-extensions`.
4. On the Linux host: `npm install electronics-workbench-decoder@0.2.0` and a
   venv with `mcp>=2,<3` for the frontend.
5. Local component pack derived from your own licensed Multisim samples
   (never redistributed):
   ```bash
   MULTISIM_MCP_EWD=/path/to/ewd MULTISIM_MCP_EWE=/path/to/ewe \
     python tools/bootstrap_local_component_pack.py \
     --samples-root "$HOME/.multisim143/drive_c/users/Public/Documents/National Instruments/Circuit Design Suite 14.3/samples" \
     --output ~/.multisim-mcp-local/component-pack --force
   ```
   The pack build mixes two worlds: `.ms14` decoding runs the host Node
   codec, while the blank-design scaffold runs the Wine COM worker. On this
   fork both paths are proven; 162 template files were generated.

## Running the MCP server

```bash
export MULTISIM_MCP_WORKER_PYTHON=/path/to/this-fork/tools/wine_worker_bridge.sh
export MULTISIM_MCP_TEMPLATE_DIR=~/.multisim-mcp-local/component-pack
export MULTISIM_MCP_EWD=/path/to/ewd   # host Node codec
export MULTISIM_MCP_EWE=/path/to/ewe
export MSIM_WINE_DISPLAY=:88           # Xvfb/Xephyr hosting Multisim's GUI
# optional: MSIM_WINE_PREFIX (default ~/.multisim143), MSIM_WINE_PYTHON
python -m multisim_mcp.server          # stdio MCP, 123 tools
```

`doctor` should report Windows detected / 32-bit worker / pywin32 / codecs OK.
The only expected warning is extended component families (CD4017, DFF8, SWB,
TIMER8) that need an extra carrier derived from your own designs.

## Path conventions

- Circuit paths handed to tools are Windows paths (`C:\...`) — they are opened
  by Multisim inside Wine.
- Output directories (`output_dir` for snapshots/reports) are Linux paths;
  the worker reaches them through Wine's automatic `Z:` drive (which maps to
  `/`). Both sides then see the same files.
- Verified end-to-end: `open_circuit` on NI's `Non-InvertingOpAmp.ms14` →
  `snapshot_open_circuit` produced `multisim-exported.cir` and
  `design-snapshot.json` on the Linux side.

## Known limits

- Empty (component-less) designs produce no netlist file; `ReportNetlist`
  writes nothing for them. Snapshot needs a circuit with components.
- Some NI sample netlists trip upstream parsers (`duplicate component refdes`
  on LowPassFilter.ms14; `allow_unsupported=True` only gets past the record
  banner). Non-InvertingOpAmp.ms14 works.
- The `I/O operation on closed file` message from the stderr reader thread is
  a harmless shutdown race in `com_worker_client._read_error`.
