"""A simple volume control."""

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class VolumeControl:
    """Controls the volume and mute state of the default speaker device.

    This class provides a Pythonic interface to manage the volume and mute
    state of the default speaker device on your system. It relies on the Windows
    Multimedia Device API (MMDeviceAPI) to achieve this.

    Raises:
        RuntimeError: If the default speaker device could not be found or accessed.

    Examples:
        >>> volume_control = VolumeControl()
        >>> print(volume_control.mute)  # Check if the speaker is muted
        >>> volume_control.mute = True  # Mute the speaker
        >>> volume_control.volume = 0.5  # Set the volume to 50%
    """

    def __init__(self) -> None:
        self._devices = AudioUtilities.GetSpeakers()
        self._interface = self._devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self._volume = self._interface.QueryInterface(IAudioEndpointVolume)

    @property
    def mute(self) -> bool:
        """True if the speaker is muted, False otherwise."""
        return bool(self._volume.GetMute())

    @mute.setter
    def mute(self, mute: bool) -> None:
        self._volume.SetMute(mute, None)

    @property
    def volume(self) -> float:
        """The current volume level of the speaker between 0.0 (silent) and 1.0 (full volume)."""
        return self._volume.GetMasterVolumeLevelScalar()

    @volume.setter
    def volume(self, scalar: float) -> None:
        assert 0.0 <= scalar <= 1.0, ValueError("Volume scalar out of range.")
        self._volume.SetMasterVolumeLevelScalar(scalar, None)
