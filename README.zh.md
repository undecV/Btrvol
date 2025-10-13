# ![icon](./resources/icon.32.png) Btrvol

溫柔地調整音量。

> 說明文件： [English](./README.md)、[正體中文](./README.zh.md)

隨時間緩緩地變化音量。

例如，當你入睡時，讓音量慢慢降低。

製作： [undecV](https://github.com/undecv)

## :eyes: 一覽

![Screenshot](./docs/Screenshot_v2.3.0.png)

## :magic_wand: 功能特色

- :snake: 使用 Python 與 Tkinter 製作。
- :level_slider: 提供四種音量變化模式：線性（Linear）、平滑（Smooth）、漸進（Gradual）、快速（Rapid）。
- :floppy_disk: 可儲存與載入設定。
- :computer: 內建 命令列（CLI）程式。
- :bar_chart: 自行繪製互動式曲線圖，減少套件體積。
- :new: 支援 亮 / 暗 主題。
- :new: 結束動作可設定為 播放 / 暫停 或 停止 媒體。

## :package: 安裝方式

請至 [發佈頁面 (Release page)](../../releases) 下載可攜式執行檔。

> 無需安裝，下載後直接執行即可。

## :question: 使用說明

- Start（起始音量）：初始音量。  
- End（目標音量）：要調整至的最終音量。  
- Duration（持續時間）：完成音量變化所需的時間。

不同的函數模式會決定音量隨時間變化的方式：

- Linear（線性）：均勻變化。  
- Smooth（平滑）：慢 → 快 → 慢。  
- Gradual（漸進）：慢 → 快。  
- Rapid（快速）：快 → 慢。

設定檔儲存在以下路徑：

```plain
%appdata%\Local\BtrVol\BtrVol\config.json
````

## 注意事項

-  由於作業系統的安全防護機制，啟動速度可能會略慢，屬於正常現象。
