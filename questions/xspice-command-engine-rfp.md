# XSPICE 命令引擎调研(已结案)

**Status:** resolved

**Settling:** 生产环境复测 `MSIM_FORCE_BACKEND=x11`,命令引擎接受 bridge 写法、
与或门真值表 0 违例 ⇒ resolved(rc=0,见文末结案附记)。

# 需求书:让 Multisim 14.3 命令文件引擎(DoCommandLine)支持数字门(XSPICE A 器件)

> 交 AI 调研用。目标:找出在 **Multisim 14.3 Windows 版(经 Wine 跑在 Linux)** 的
> `DoCommandLine` SPICE 引擎里,让数字门(XSPICE A 器件,如 2 输入与门)参与仿真
> 的正确网表写法;或确认该引擎确实不支持并给出官方出处。

## 我们的环境与已验证事实(全部实测,非猜测)

- Multisim 14.3 Educational,Wine 11.0 stable(i386 prefix),Debian,COM 自动化经
  `MultisimInterface.MultisimApp` / `MSInterface.dll`(进程内)。
- 两条仿真通路:
  1. **命令文件引擎**:`Circuit.DoCommandLine(cmdFile, logFile)`(cmd 文件内
     `source x.cir` / `tran 1u 80u` / `write x.raw`)→ 纯 SPICE raw 文件。
     模拟电路(RLC/源)完全正常。
  2. **原生交互仿真**:`SetOutputRequest` + `RunSimulation` + `GetOutputData` ——
     数字门能工作(已验证与或门真值表),但输出对象必须是**探针元件**
     (`enum_outputs` 给 `V(OutProbe*)` / 数字探针 `D(PR1)`)。
- 我们要用通路 1 的原因:`GetOutputData` 逐探针轮询、raw 文件一次拿全部波形的工程差异。

## 实测到的引擎报错(同一段网表的不同形态)

网表:`A1 in out dand` + `.model dand d_and`:

1. 引擎**认识 A 器件**(XSPICE 内核存在)。报错不是 "unknown device"。
2. `A1 in out dand`(两节点)→ `Digital and analog pins are connected on node '$in'`
   —— 引擎把 A1 输入当数字节点,而 V1(模拟 DC 源)挂同一节点被判定混连。
3. `A1 [in] [out] dand` → `Array port type required on terminal 0 of this device`
   —— 意外:第一端口**要求**数组。
4. `A1 in [out] dand` → `Array port type not allowed on terminal 1 of this device`
5. `A1 [in in] [out] dand` → 同 4。
6. `.model dand d_and(rise_delay=90n fall_delay=110n)` + 5 节点
   (in1 in2 out vdd gnd,Multisim 数据库宏形态)→ `Unable to identify XSPICE code model`
   (参数名不认识)+ `Array port type required on terminal 0`。

## 我们猜测但未证实的方向

- Multisim 数据库里的门(如 4081B_5)的 SPICE 模板可能不是标准 XSPICE `d_and`,
  而是带 `%d` 端口声明的自定义 code model,实例行必须带特定的矢量/标量混合写法;
- 或命令引擎在 `source` 时需要附带数据库导出的 `.include`/模型库文件;
- 或 `DoCommandLine` 的 SPICE 是"模拟专用"内核,数字门只能走通路 2(官方手册若
  明确这一点,也算答案)。

## 请调研的问题

1. Multisim 14.x 的 `DoCommandLine`/命令文件 SPICE 引擎是否支持 XSPICE A 器件?
   官方文档(NI Multisim User Manual「SPICE language reference」/「Command file」
   章节)怎么说?给出章节名或引文。
2. 若支持:2 输入与门(4081/74HC08 族)的**最小可运行网表**长什么样?
   `.model` 行、A 行端口顺序、是否需要 `%d` 端口声明、数字激励怎么写(模拟源 +
   接口元件?专用数字源?)。
3. Multisim 数据库中门的 SpiceTemplate(可从数据库导出或已知资料)里,4081B_5 的
   模板文本是什么?
4. 数字/模拟混连(模拟源驱动数字门输入)在 Multisim 里需要什么接口约定
   (`Digital and analog pins are connected on node` 报错的官方解法)?

## 交付

- 若找到写法:一段能被 `DoCommandLine` 跑通的 .cir(2 输入与门 + 激励),
  我们立即在环境里复测并回填结论。
- 若确认不支持:官方文档出处。

---

## 结案附记(2026-11-08,实测回填)

**Claude 给出的网表一次跑通,零报错。** 根因不是"引擎不支持 XSPICE",而是:

1. 模拟↔数字边界必须显式写 `adc_bridge`/`dac_bridge`(GUI 仿真时 Multisim 自动插入,
   命令文件网表没有这层 —— 这是 `Digital and analog pins are connected on node` 的官方解法);
2. 门实例的输入/输出是**矢量端口** `[net ...]`,且激励保持在模拟侧(PULSE 源);
3. `.model AND2 d_and (rise_delay=... fall_delay=...)` 参数名正确(NI 论坛同款);
4. 结果从 dac_bridge 之后的模拟节点读 —— raw 里是真实电压,无须碰数字流。

复测数据(生产路径,生产 multisim.exe):与门高电平窗口 [5,15]/[45,55]μs 精确;
完整 Y=(A·B)+C 稳态 97 采样 0 违例(35 个"违例"全部是 1ns 门传播延迟的边沿采样点)。

工作网表已固化在 multisim-mcp 的 docs/LINUX_WINE_BRIDGE.md 与
msre_exp/xspice_bridge/t2.cir(生产 prefix 内,可直接 source)。

**结论:命令文件引擎完整支持 XSPICE 数字门;问题从来是端口形态与桥接器,不是内核。**
