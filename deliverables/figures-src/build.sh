#!/bin/sh
# Rebuild ALL delivered figures. Run from this directory.
# Each source has an explicit output name+dir; no implicit discovery, no stale copies.
set -eu
echo "== t804grid -> ../figures-batch1/fig-8-04"
pdflatex -interaction=nonstopmode -halt-on-error t804grid.tex >t804grid.build.log 2>&1 || { tail -20 t804grid.build.log >&2; exit 1; }
pdftocairo -png -r 300 -singlefile t804grid.pdf ../figures-batch1/fig-8-04
dvisvgm --pdf --exact --font-format=woff2 t804grid.pdf -o ../figures-batch1/fig-8-04.svg >/dev/null
echo "== t805 -> ../figures-batch1/fig-8-05"
pdflatex -interaction=nonstopmode -halt-on-error t805.tex >t805.build.log 2>&1 || { tail -20 t805.build.log >&2; exit 1; }
pdftocairo -png -r 300 -singlefile t805.pdf ../figures-batch1/fig-8-05
dvisvgm --pdf --exact --font-format=woff2 t805.pdf -o ../figures-batch1/fig-8-05.svg >/dev/null
echo "== t812c -> ../figures-batch1/fig-8-12"
pdflatex -interaction=nonstopmode -halt-on-error t812c.tex >t812c.build.log 2>&1 || { tail -20 t812c.build.log >&2; exit 1; }
pdftocairo -png -r 300 -singlefile t812c.pdf ../figures-batch1/fig-8-12
dvisvgm --pdf --exact --font-format=woff2 t812c.pdf -o ../figures-batch1/fig-8-12.svg >/dev/null
echo "== t813b -> ../figures-batch1/fig-8-13"
pdflatex -interaction=nonstopmode -halt-on-error t813b.tex >t813b.build.log 2>&1 || { tail -20 t813b.build.log >&2; exit 1; }
pdftocairo -png -r 300 -singlefile t813b.pdf ../figures-batch1/fig-8-13
dvisvgm --pdf --exact --font-format=woff2 t813b.pdf -o ../figures-batch1/fig-8-13.svg >/dev/null
echo "== t807 -> ../figures-batch1/fig-8-07"
pdflatex -interaction=nonstopmode -halt-on-error t807.tex >t807.build.log 2>&1 || { tail -20 t807.build.log >&2; exit 1; }
pdftocairo -png -r 300 -singlefile t807.pdf ../figures-batch1/fig-8-07
dvisvgm --pdf --exact --font-format=woff2 t807.pdf -o ../figures-batch1/fig-8-07.svg >/dev/null
echo "== t802 -> ../figures-batch1/fig-8-02"
pdflatex -interaction=nonstopmode -halt-on-error t802.tex >t802.build.log 2>&1 || { tail -20 t802.build.log >&2; exit 1; }
pdftocairo -png -r 300 -singlefile t802.pdf ../figures-batch1/fig-8-02
dvisvgm --pdf --exact --font-format=woff2 t802.pdf -o ../figures-batch1/fig-8-02.svg >/dev/null
echo "== t806 -> ../figures-batch3/fig-8-06"
pdflatex -interaction=nonstopmode -halt-on-error t806.tex >t806.build.log 2>&1 || { tail -20 t806.build.log >&2; exit 1; }
pdftocairo -png -r 300 -singlefile t806.pdf ../figures-batch3/fig-8-06
dvisvgm --pdf --exact --font-format=woff2 t806.pdf -o ../figures-batch3/fig-8-06.svg >/dev/null
echo "== t705 -> ../figures-batch3/fig-7-05"
pdflatex -interaction=nonstopmode -halt-on-error t705.tex >t705.build.log 2>&1 || { tail -20 t705.build.log >&2; exit 1; }
pdftocairo -png -r 300 -singlefile t705.pdf ../figures-batch3/fig-7-05
dvisvgm --pdf --exact --font-format=woff2 t705.pdf -o ../figures-batch3/fig-7-05.svg >/dev/null
echo "== t714 -> ../figures-batch3/fig-7-14"
pdflatex -interaction=nonstopmode -halt-on-error t714.tex >t714.build.log 2>&1 || { tail -20 t714.build.log >&2; exit 1; }
pdftocairo -png -r 300 -singlefile t714.pdf ../figures-batch3/fig-7-14
dvisvgm --pdf --exact --font-format=woff2 t714.pdf -o ../figures-batch3/fig-7-14.svg >/dev/null
echo "== t716 -> ../figures-batch3/fig-7-16"
pdflatex -interaction=nonstopmode -halt-on-error t716.tex >t716.build.log 2>&1 || { tail -20 t716.build.log >&2; exit 1; }
pdftocairo -png -r 300 -singlefile t716.pdf ../figures-batch3/fig-7-16
dvisvgm --pdf --exact --font-format=woff2 t716.pdf -o ../figures-batch3/fig-7-16.svg >/dev/null
echo "== t801 -> ../figures-batch3/fig-8-01"
pdflatex -interaction=nonstopmode -halt-on-error t801.tex >t801.build.log 2>&1 || { tail -20 t801.build.log >&2; exit 1; }
pdftocairo -png -r 300 -singlefile t801.pdf ../figures-batch3/fig-8-01
dvisvgm --pdf --exact --font-format=woff2 t801.pdf -o ../figures-batch3/fig-8-01.svg >/dev/null
echo "== t802b -> ../figures-batch3/fig-8-02-3row"
pdflatex -interaction=nonstopmode -halt-on-error t802b.tex >t802b.build.log 2>&1 || { tail -20 t802b.build.log >&2; exit 1; }
pdftocairo -png -r 300 -singlefile t802b.pdf ../figures-batch3/fig-8-02-3row
dvisvgm --pdf --exact --font-format=woff2 t802b.pdf -o ../figures-batch3/fig-8-02-3row.svg >/dev/null
echo "== t806ans -> ../figures-batch3/fig-8-06-answers"
pdflatex -interaction=nonstopmode -halt-on-error t806ans.tex >t806ans.build.log 2>&1 || { tail -20 t806ans.build.log >&2; exit 1; }
pdftocairo -png -r 300 -singlefile t806ans.pdf ../figures-batch3/fig-8-06-answers
dvisvgm --pdf --exact --font-format=woff2 t806ans.pdf -o ../figures-batch3/fig-8-06-answers.svg >/dev/null
echo "== t807ans -> ../figures-batch3/fig-8-07-ans"
pdflatex -interaction=nonstopmode -halt-on-error t807ans.tex >t807ans.build.log 2>&1 || { tail -20 t807ans.build.log >&2; exit 1; }
pdftocairo -png -r 300 -singlefile t807ans.pdf ../figures-batch3/fig-8-07-ans
dvisvgm --pdf --exact --font-format=woff2 t807ans.pdf -o ../figures-batch3/fig-8-07-ans.svg >/dev/null
echo "== t808ans -> ../figures-batch3/fig-8-08-ans"
pdflatex -interaction=nonstopmode -halt-on-error t808ans.tex >t808ans.build.log 2>&1 || { tail -20 t808ans.build.log >&2; exit 1; }
pdftocairo -png -r 300 -singlefile t808ans.pdf ../figures-batch3/fig-8-08-ans
dvisvgm --pdf --exact --font-format=woff2 t808ans.pdf -o ../figures-batch3/fig-8-08-ans.svg >/dev/null
echo "== t809ans -> ../figures-batch3/fig-8-09-ans"
pdflatex -interaction=nonstopmode -halt-on-error t809ans.tex >t809ans.build.log 2>&1 || { tail -20 t809ans.build.log >&2; exit 1; }
pdftocairo -png -r 300 -singlefile t809ans.pdf ../figures-batch3/fig-8-09-ans
dvisvgm --pdf --exact --font-format=woff2 t809ans.pdf -o ../figures-batch3/fig-8-09-ans.svg >/dev/null
echo "== t801out -> ../figures-batch3/fig-8-01-out"
pdflatex -interaction=nonstopmode -halt-on-error t801out.tex >t801out.build.log 2>&1 || { tail -20 t801out.build.log >&2; exit 1; }
pdftocairo -png -r 300 -singlefile t801out.pdf ../figures-batch3/fig-8-01-out
dvisvgm --pdf --exact --font-format=woff2 t801out.pdf -o ../figures-batch3/fig-8-01-out.svg >/dev/null
echo "== t802out -> ../figures-batch3/fig-8-02-out"
pdflatex -interaction=nonstopmode -halt-on-error t802out.tex >t802out.build.log 2>&1 || { tail -20 t802out.build.log >&2; exit 1; }
pdftocairo -png -r 300 -singlefile t802out.pdf ../figures-batch3/fig-8-02-out
dvisvgm --pdf --exact --font-format=woff2 t802out.pdf -o ../figures-batch3/fig-8-02-out.svg >/dev/null
# ── batch4：通用电气概念图 ──
# 中文字体链路：xelatex + ctex（图内文字全中文，只保留变量符号与单位）
build_zh() { # $1 tex 名  $2 输出名
  echo "== $1 -> ../figures-batch4/$2"
  xelatex -interaction=nonstopmode -halt-on-error "$1.tex" >"$1.build.log" 2>&1 || { tail -20 "$1.build.log" >&2; exit 1; }
  pdftocairo -png -r 300 -singlefile "$1.pdf" "../figures-batch4/$2"
  dvisvgm --pdf --exact --font-format=woff2 "$1.pdf" -o "../figures-batch4/$2.svg" >/dev/null
}
build_one() { # $1 tex 名  $2 输出名
  echo "== $1 -> ../figures-batch4/$2"
  pdflatex -interaction=nonstopmode -halt-on-error "$1.tex" >"$1.build.log" 2>&1 || { tail -20 "$1.build.log" >&2; exit 1; }
  pdftocairo -png -r 300 -singlefile "$1.pdf" "../figures-batch4/$2"
  dvisvgm --pdf --exact --font-format=woff2 "$1.pdf" -o "../figures-batch4/$2.svg" >/dev/null
}
build_zh tge01 fig-ge-01
build_zh tge02 fig-ge-02
build_zh tge03 fig-ge-03
build_zh tge04 fig-ge-04
build_zh tge05 fig-ge-05
build_zh tge06 fig-ge-06
build_zh tge07 fig-ge-07
build_zh tge08 fig-ge-08
echo "build ok: 18 homework figures + 8 concept figures (batch4)"
