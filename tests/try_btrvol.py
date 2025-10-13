import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
from btrvol_lib.btrvol import BtrVol

# 初始參數
init_start = 20
init_end = 80
init_duration = 10
init_tone = BtrVol.Tone.SMOOTH

btrvol = BtrVol(init_start, init_end, init_duration, init_tone)

# 讓 Matplotlib 自動幫你排版
fig = plt.figure(constrained_layout=True)
# 兩塊子圖區：上(曲線) / 下(控制元件)
subfigs = fig.subfigures(2, 1, height_ratios=[4, 2])
sf_top, sf_bottom = subfigs

# ---- 上面：主圖（左 y 音量、右 y 間隔）----
ax = sf_top.subplots(1, 1)
ax2 = ax.twinx()
(line1,) = ax.plot(btrvol.time_points, btrvol.volume_levels, marker='o', color='royalblue', label="Volume")
(line2,) = ax2.plot(btrvol.time_points, btrvol.time_intervals, linestyle='--', color='orange', alpha=0.6, label="Interval")

mode_text = ax.text(0.02, 0.95, f"Mode: {btrvol.mode.name}", transform=ax.transAxes, va="top")

ax.set_xlabel("Time (s)")
ax.set_ylabel("Volume (0–100)")
ax2.set_ylabel("Interval (s)")

# ---- 下面：控制元件，用 GridSpec 自動分格 ----
# 3 列 2 欄：左邊三列給三個滑桿，右邊整欄給單選鈕
gs = sf_bottom.add_gridspec(nrows=3, ncols=2, width_ratios=[3, 1])

ax_start = sf_bottom.add_subplot(gs[0, 0])
ax_end = sf_bottom.add_subplot(gs[1, 0])
ax_duration = sf_bottom.add_subplot(gs[2, 0])
ax_tone = sf_bottom.add_subplot(gs[:, 1])  # 右欄佔滿三列

# 建立 widgets（不必手寫位置矩形）
s_start = Slider(ax_start, "Start", 0, 100, valinit=init_start, valstep=1)
s_end = Slider(ax_end, "End", 0, 100, valinit=init_end, valstep=1)
s_duration = Slider(ax_duration, "Duration", 1, 60, valinit=init_duration, valstep=1)
r_tone = RadioButtons(ax_tone, ("LINEAR", "SMOOTH", "GRADUAL", "RAPID"), active=1)

def update(_):
    tone_enum = getattr(BtrVol.Tone, r_tone.value_selected)
    b = BtrVol(int(s_start.val), int(s_end.val), int(s_duration.val), tone_enum)

    line1.set_xdata(b.time_points)
    line1.set_ydata(b.volume_levels)
    line2.set_xdata(b.time_points)
    line2.set_ydata(b.time_intervals)
    mode_text.set_text(f"Mode: {b.mode.name}")

    ax.relim(); ax.autoscale_view()
    ax2.relim(); ax2.autoscale_view()
    fig.canvas.draw_idle()

s_start.on_changed(update)
s_end.on_changed(update)
s_duration.on_changed(update)
r_tone.on_clicked(update)

plt.show()
