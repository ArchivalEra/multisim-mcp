# 02-figure-live-renderer: course-site figure renderer commission

**Status:** ready-for-agent

**Settling:** `python3 reflect-local/figure_live_criteria.py --selftest` — rc=0 ⇒ the
structural contract **and** the geometry gate (`geometry.mjs`: wire×box, wire×text,
topology mutants + hand-fanout regression) hold on the shipped fixture; rc=1 ⇒ at
least one is broken. Reopened 2026-11-09 by course-site mail 083: the earlier
"resolved" rested on a string-grep checker that could not see 14 wire-through-box
crossings; conditions 1/2/4/5 are now fixed, condition 3 (AI read channel) answered
in mail 084, awaiting their acceptance.

**From:** course site (`GONGCHENGSHUXUE20260917`) mail 078, 2026-11-09.
**Scope:** proposal + a runnable validation artifact only. Never edit the course
site's `站点/` tree and never commit for them (mail rule 1 and 4).

## What was commissioned

Replace the build-time DSL→SVG baking in `站点/plugins/figures.mjs` with a live,
browser-side, data-driven figure renderer. Requirements live in the course site's
local `.kimi-code/需求-图元渲染方案选型.md` (not in git). Summary of the hard
constraints:

1. One data description projects twice: graphic for humans, structured text
   (netlist / level string) for the AI reader. The AI projection is a first-class
   product, not a caption.
2. Six measured defects must not recur: wire through a box, same defect on another
   topology, text cut by a wire, stacked input labels, uncontrolled component
   orientation, flat waveform with no high/low reference.
3. Pure front end, no server, no CDN, vendored; theme-inheriting; zoomable.
4. Author writes at most a dozen lines per circuit.
5. Click a component to inspect it; change a state and the figure redraws.
6. Deliverables: library/format selection (name + license + maintenance + size),
   per-genre minimal usable compromise for logic / wave / kmap / net, and a
   runnable validation artifact (7-gate logic figure + multi-row waveform, with
   data files).

## Research results (npm registry, measured 2026-11-09, `npm view`)

| package | version | license | unpacked | last modified | verdict |
|---|---|---|---|---|---|
| wavedrom | 3.8.0 | MIT | 835 KB | 2026-10-25 | use for wave |
| elkjs | 0.13.0 | EPL-2.0 OR GPL-3.0-or-later | 8.2 MB | 2026-10-28 | use for logic layout |
| netlistsvg | 1.0.2 | MIT | 1.4 MB | 2022-05-10 | reference only (stale) |
| digitaljs | 0.14.2 | BSD-2-Clause | 14.6 MB | 2026-02-10 | reference only (ANSI gates; runtime IEC overlay failed; the 14.6 MB "too heavy" reason is retracted, see R-figure-size-20261109) |
| @joint/core | 4.3.4 | MPL-2.0 | 6.3 MB | 2026-10-27 | not needed for a static-render demo |
| d3 | 7.9.2 | ISC | 882 KB | 2026-11-03 | not needed |

## Boundary

This ticket is about a renderer for a **different repository**. Its source of
truth is that repository's local requirement document; do not copy that document
into this repository as a tracked file (`no_requirements_in_git`). Record intent
here, in the questions ledger, with a settling command.

---

## 结案附记（2026-11-09，交付方案全文）

**交付方：** multisim-mcp
**日期：** 2026-11-09
**对应委托：** 课程站 `mail/078` §4、`/.kimi-code/需求-图元渲染方案选型.md`
**验证件：** 同目录 `index.html`（双击 `file://` 可开）、`data/`、`vendor/`
**结构检查器：** 本仓 `zreflect/figure_live_criteria.py`

---

## 0. 结论先行

这个领域没有一个「电路图的 MathLive」。MathLive 能存在，是因为数学排版的一维/二维语法是封闭的；电路图不是——门级有向图、时序波形、卡诺图、模拟原理图是四种不同的东西，没有单一数据格式能把它们都装进去还能自动排得对。

**所以结论是分层组合，不是找一个库：**

| 图种 | 推荐 | 许可证 | 解包体积 | 维护状态 | 要自己写的那一层 |
|---|---|---|---|---|---|
| 门级逻辑 | **ELK (elkjs) 0.13.0** 做分层布局与正交走线 + 原生 SVG 画 IEC 方框门 | EPL-2.0 OR GPL-3.0-or-later | 8.2 MB | 活跃（2026-10-28） | 端口约束、符号绘制、文本投影 |
| 时序波形 | **WaveDrom 3.8.0** / WaveJSON | MIT | 835 KB | 活跃（2026-10-25） | 恒高恒低的参考轨、结构化电平串 |
| 卡诺图 | 不引库，原生 SVG 格网 | — | 0 | — | 循环码、圈组几何 |
| 模拟电路 | **不自动布局**：数据里显式给坐标与朝向 | — | 0 | — | 元件符号库、引脚端点表 |

`netlistsvg 1.0.2`（MIT，1.4 MB，2022-05-10 后停更，ELK 锁 0.3.0）与 `digitaljs 0.14.2`（BSD-2-Clause，14.6 MB）都**不推荐直接采用**：前者四年没动、符号是美国 ANSI 曲线门而非 IEC 方框；后者为「可仿真」付了 14 MB 与一套自有 IR，而这里要的是「可读的题面图」，不是逻辑模拟器。**（retracted 2026-11-09：以体积排除 DigitalJS 是错的；真实依据是 ANSI 符号与实测覆盖层失败，见 R-figure-size-20261109 与下方结案补记）**

一句话：**用成熟库解决公认的难题（分层布局、波形排版），用显式数据解决不能交给自动布局的东西（朝向、对称性、电平参照）。** 这正好对应需求书 §5.7「哪些约束能让自动布局变可靠」。

---

## 1. 需求书 §5 逐题回答

**Q1 这个领域的 MathLive 是谁？**
没有单一答案。数字时序波形有 WaveDrom（成熟、活跃、数据驱动）；门级原理图有 ELK 作为布局后端，但符号与交互要自己包一层；模拟原理图没有成熟的「给网表就画对」的浏览器组件——`netlistsvg` 是最接近的，但它停更且默认 ANSI 符号，二极管朝向这类题面语义它不保证。

**Q2 门级自动布线是公认难题吗？**
是。一般图的正交布线、交叉最小化是 NP 难的；业界可用的可靠子集是 **Sugiyama 分层布局 + 端口侧约束 + 禁止反馈边**，ELK 正是这个算法的成熟实现（`elk.algorithm=layered`、`elk.port.side=WEST/EAST`、`elk.edgeRouting=ORTHOGONAL`）。实测：`deliverables/figure-live/index.html` 里 7 门图的门位、端口、拐点全部由 ELK 算出，没有手写坐标常数。
**最小可用折中**：只允许从左到右的有向无环图；反馈线（如 8.04、8.12 那种 Q→J 回接）不进自动布局，改由数据显式给「回接通道」。这一条要写进 DSL 契约，不能靠布局器猜。

**Q3 模拟电路有能直接用的吗？**
没有能同时保证「尖朝右」「对称性」的。需求书 §3.5 的二极管朝向决定答案，这类语义**必须由数据显式指定**（`orientation: right`），自动布局只能消费它、不能推断它。所以 `net` 图种建议放弃通用自动布局：数据里带 `x,y,rotation,ports`，渲染器只负责把符号按端点接起来。这放弃了「作者少写几行」里的一点便利，换回「朝向不会被猜错」。

**Q4 多行波形有成熟组件吗？**
有，WaveDrom。它天然处理时钟沿对齐、多行共用时间轴、标签，产物是 SVG（text 节点可搜索）。**但需求书 §3.6 的「恒高/恒低判不出」是 WaveDrom 不解决的**：`wave: "1...."` 画出来就是一条平线，读者不知道它在高轨还是低轨。验证件里我在波形下方补了明确的高低参考轨（`1（高）` / `0（低）`），并把每一行的电平串原样写进文本投影——两层保险，不靠读者猜。

**Q5 该不该改用既有网表格式？**
**门级与模拟：不建议改成 SPICE 子集。** SPICE 的节点是电气节点，题面里的 `A/B/C/Y` 是逻辑变量；把 `and A B -> Y` 写成 `.subckt` 会让写作业解析的人多写三倍，而且丢掉 IEC 方框符号信息。建议保留自己的 JSON schema（验证件里的 `logic-7gate.json` 就是），它是「一行一只门」的最薄格式。
**波形：建议直接采用 WaveJSON**，它是既有格式、生态现成、能直接喂 WaveDrom，代价只是把现有 `CP: 0011...` 的冒号写法换成 `{name, wave}`。

**Q6 有没有更彻底的路？**
「数据 + 成熟渲染后端」就是本方案，但要拆成两个后端：ELK 只算布局（不画图），WaveDrom 只画波形（不管电路）。交互层（点击、改状态、换主题、缩放）由自己那层原生 DOM 承担，验证件已经证明这层很薄（`index.html` 约 300 行，含样式与数据加载）。

---

## 2. 六类坏状怎么判（对应需求书 §3、§六）

现有的自研检查是「导线不得穿门框、画布宽度不依赖书写顺序、输入标签间距不小于字高、每行必须画高低参考轨、削顶真取 min/max」。本方案逐条给判据：

| 坏状 | 本方案怎么不再出现 | 可跑检查 |
|---|---|---|
| ① 线穿方框 | 门框是独立 `<rect>`，导线端点只落在 port 上；ELK 的 edge sections 不含框内点 | `figure_live_criteria.py` 检 port 声明；几何检查：任一 wire 段与任一 gate rect 求交，交集必须只在边界 |
| ② 同拓扑复发 | 不调间距常数，换拓扑由 ELK 重新分层 | 检查器对变异后的数据（删一只门 / 加一条边）重跑，布局仍由 ELK 给出 |
| ③ 字被线切开 | 文字是 SVG `<text>`，且绘制顺序在导线之后；标签坐标由门框算出，不由导线算出 | `figure_live_criteria.py` 检 `el('text')`、禁 `<use>`；几何检查：wire 段与 text bbox 不相交 |
| ④ 输入标签堆叠 | 主输入固定左列、等距分排（验证件 `terminals`），不随图拓扑漂移 | 检查器检 `terminals[n] =` 固定列 |
| ⑤ 元件朝向控不住 | `net` 图种由数据显式给 `orientation`，不进自动布局 | 数据 schema 校验；这是契约，不是几何启发式 |
| ⑥ 波形判不出常高常低 | 高低参考轨 + 电平串文本投影双保险 | 检查器检 `rail-hi`/`rail-lo`、数据里必须同时存在恒高串与恒低串 |

**双投影**是硬需求，本方案把结构化文本当一等产物：右侧「文本投影」区直接从同一份 JSON 生成网表（每门一行，带类型、输入、实时值）和电平串，大模型不看图也能答题。改输入时 SVG 与文本一起重算，实测通过。

---

## 3. 迁移代价（需求书 §七）

**现有 28 个图元的数据要不要重写？** 分三类：

- **波形 18 个**：机械转换，写个一次性脚本把 `标签: 0011...` 转成 `{name, wave}` 即可，语义不变。`wave 40 ; guides ...` 对应 WaveJSON 的 `config`/`head`，需要一个小映射表。
- **门级 9 个**：机械转换，`and A B -> Y` → `{id, type, in, label}`，保留 `^B^` 这类记法为字符串标签。反馈边按 §1 Q2 显式标注为回接通道。
- **卡诺图 4 个**：保留格值，圈组 `box r1-2 c0-3` 改成显式坐标区间，渲染器自己画循环码网格。
- **模拟 2 个**：**必须人工重写**，`net-7-05` 与 `net-1-01` 要补每个元件的 `x,y,rotation,ports`；这是唯一不能机械迁移的部分，代价 2 条 × 十来行。

**页面引用方式会不会变？** 不变。`:::figure <id> | 图注` 继续用，构建期不再烘死 SVG，而是把 `<id>` 对应的 JSON 内嵌进页面、由前端组件渲染。图注仍在 Markdown 里，仍可被搜索。

**AI 那侧的文本投影怎么保留？** 由组件在渲染时同步输出一段结构化文本（网表 / 电平串），挂在 `<pre id="projection">` 或等价的 `data-` 属性里；它不是图注，是数据的另一投影。现有「额外烘出来的结构表」可以退役。

**要放弃什么？**
1. 构建期产物是 SVG 字符串这件事——改成浏览器内渲染（首屏多一次 JS 执行，换来可交互）。
2. 自研 `figures.mjs` 的 BFS 分层与全部间距常数——ELK 接管，常数不再有调参价值。
3. `net` 图种的「全自动摆位」——朝向与对称性必须显式给，这部分作者多写几行。

---

## 4. 验证件（可运行）

`deliverables/figure-live/index.html`，纯静态：

- `vendor/` 下是 `elk.bundled.js`、`wavedrom.unpkg.min.js` 与两份许可证全文，无 CDN、无联网；
- `data/logic-7gate.json`：7 门逻辑图（习题 7.14 的三非门 + 四与非门），`data/wave-multirow.json`：CP/D/Q/EN 四行波形，含恒高与恒低；
- 点门看属性、改输入立即重算并同步文本投影、主题切换走 CSS 变量、缩放走 viewBox；
- 浏览器里实测：点 `Y` 门显示 `type=nand, inputs=[p1, p2, p3], values=[1, 1, 1], output=0`；把 `B` 从 1 拨到 0，`nB` 由 0→1，文本投影里 `nB [not] ... value=0` 同步变 `value=1`；放大按钮 100%→125% 生效；
- 结构检查器 `python3 zreflect/figure_live_criteria.py` rc=0，`--selftest` 用变异副本验证能抓到违规（rc=0，mutant_detected=True）。

**已知边界（不粉饰）**：验证件里主输入端子是固定左列、扇出走线自己算的正交折线，门体之间的边由 ELK 给；这套混合是最小可跑折中，不是完整产品。反馈环、`net` 图种的显式朝向、卡诺图、SPICE 风格网表都没做——它们属于方案的下一阶段，需求书只要求「最小验证件」。

---

## 结案补记 2（2026-11-09，DigitalJS 复核）

**撤回 080 / 本台账里「14.6 MB 太重」这条依据。** 课程站已自带 56 MB 的
Pyodide + Octave WASM 内核（整个 `站点/` 138 MB）；14.6 MB 是 npm 解包体积
（含源码、map、测试页），DigitalJS 真正给浏览器的 JS 是 2.9 MB
（`main.js` 2.39 MB + `285.main.js` 558 KB + `821.main.js` 77 KB）。
体积不构成排除理由，把两种体积混为一谈是我的错。

按用户要求仍做了实测件：不改库源码，运行时隐藏 `path.gate`、给每个门补
IEC 方框与 `&`/`≥1`/`=1` 文本。结果：DigitalJS 内建的 ELK 把 3 只门叠在
同一位置，覆盖层返回「IEC 覆盖 0 只门」，而且它的 `and_path`/`or_path`
本来就是 ANSI 曲线门。**该路径废弃**，实验件、临时服务与浏览器标签都已
清除；本仓 `retractions.json` 登记了两条撤回（R-figure-size-20261109、
R-figure-digitaljs-ansi-20261109），`check_retractions.py` 实跑 rc=0。

**维持原方案**：ELK 只算布局 + 原生 SVG 画 IEC 方框门，WaveDrom 画波形，
卡诺图原生 SVG，模拟电路数据显式给朝向。结论没变，但依据换成了实测事实。

---

## 结案补记 3（2026-11-09，083 验收反馈处置）

课程站 083 判定：六图五可用、8.12 一处复位反馈对调；方案分层架构**有条件采纳**，
五条缺一不可。逐条处置：

1. **扇出交给 ELK**：主输入建成 ELK 节点、`elk.partitioning.partition=0`，门按拓扑
   深度给 partition；删掉全部手写通道常数。复算 0 段穿透（旧版 14 段）。
2. **几何判据**：新增 `deliverables/figure-live/geometry.mjs`，跑与页面同一条 ELK
   路径，做 wire×box 与 wire×text 求交；`--selftest` 含删门/加边两个拓扑变异 +
   手写扇出回归变异（后者必须被抓到）。`figure_live_criteria.py` 现在调用它。
3. **AI 读页通道**：查课程站 `站点/plugins/webmcp-tools.mjs`——`site_read` 走
   `renderMarkdown`，`skipTags` 含 `SCRIPT,STYLE,NOSCRIPT,TEMPLATE,SVG`，`PRE` 按
   代码块读 `textContent`。通道在**已加载页面的 DOM 上**执行（WebMCP 工具由页面
   JS 注册、桥 `executeTool` 调用），所以运行时写进 `<pre>` 的投影**读得到**；
   但若改成构建期静态 HTML 且不执行 JS，`SCRIPT` 里的 JSON 会被整段丢弃。
   结论：投影必须落在 `PRE`/普通元素，不能只放 `script[type=application/json]`。
4. **levels 派生**：删掉 `wave-multirow.json` 的 `levels` 副本，运行时由
   `signals[].wave` 派生；四行统一到 17 拍；标题改「四行」。
5. **file:// 与放大**：数据内联进 HTML（`#data-logic`/`#data-wave`），不再 fetch；
   去掉 `svg{max-width:100%}`，逻辑图套 `#logic-wrap{overflow:auto}`。

8.12 已按 076 §4 对调：`R₀(1)←Q₂`、`R₀(2)←Q₁`，SVG/PNG 重生成并读图复核。
两条新撤回登记在 `retractions.json`（R-figure-geometry-20261109、
R-figure-file-protocol-20261109）。图源与重建脚本落在
`deliverables/figures-src/`（不再依赖 /tmp）。

---

## 增补（2026-11-10，线样式两旋钮）

用户定案：走线美观不靠改布局，靠**每条线可自定义**。只做两个旋钮：
`wireStyles[net].color`（`#rrggbb`）与 `wireStyles[net].dash`（`solid|dashed`）。
渲染器按 ELK edge id 解出源网 apply；文本投影同步暴露样式（AI 读得到）；
检查器校验 schema（只许这两个键、颜色格式、dash 枚举、网必须存在），
负向测试（`color:red / dash:dotted / width:3`）实测 rc=1 抓到三条违规。
fixture 演示：nD 蓝色虚线、p1 橙色实线、p2 默认色虚线。
