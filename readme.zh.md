# ![icon](./BtrVol/resources/icon.32.png) BtrVol

溫柔地調節音量。

> Readme: [English](./readme.md), [正體中文](./readme.zh.md)

用幾個妙不可言的數學公式調整音量。

Present by: [undecV](https://github.com/undecv)

## 安裝

系統需求：`Windows`, `.NET 6.0`.

從 Release page 下載便攜執行檔。

## 壹覽無遺

![Screenshot](./Docs/Screenshot.png)

## 如何使用

- Start: 初始音量。
- End: 目標音量。
- Duration: 改變音量需要的時間的長度。
- Interval: 每時間間隔改變音量。小的間隔使得音量的變化更加的柔和，反之亦然。

函數決定音量如何隨時間變化。

- Linear: 線性，均勻地。
- Cosine: 餘弦，先緩後急再緩。
- Half-cosine: 先緩後急。
- Half-sine: 先急後緩。

## Package Reference

- [AudioSwitcher](https://github.com/xenolightning/AudioSwitcher) (MS-PL)
- [OxyPlot](https://github.com/oxyplot/oxyplot) (MIT)
- [Windows API Code Pack](https://www.nuget.org/packages/Microsoft.WindowsAPICodePack-Shell)
