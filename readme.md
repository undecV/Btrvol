# ![icon](./BtrVol/resources/icon.32.png) BtrVol

Adjust the volume gently.

> Readme: [English](./readme.md), [正體中文](./readme.zh.md)

"Experience unparalleled sound control with our software, leveraging refined sine wave functions for free volume adjustment. Whether you're working, relaxing, or preparing for sleep, you can naturally and smoothly adjust the volume according to your needs, providing you with the most comfortable listening experience." -- ChatGPT 

Present by: [undecV](https://github.com/undecv)

## Install

The system requires: `Windows`, `.NET 6.0`.

Download the portable executable file from the release page.

## Glance

![Screenshot](./Docs/Screenshot.png)

## How to use

- Start: Initial volume.
- End: Target volume.
- Duration: The length it takes to change the volume.
- Interval: The time intervals to change the volume. Smaller intervals make volume changes softer, and vice versa.

Functions decide how the volume change with time.

- Linear: uniformly.
- Cosine: slow, then fast, then slow.
- Half-cosine: slow, then fast.
- Half-sine: fast, then slow.

## Package Reference

- [AudioSwitcher](https://github.com/xenolightning/AudioSwitcher) (MS-PL)
- [OxyPlot](https://github.com/oxyplot/oxyplot) (MIT)
- [Windows API Code Pack](https://www.nuget.org/packages/Microsoft.WindowsAPICodePack-Shell)
