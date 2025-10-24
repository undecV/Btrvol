"""A simple volume control."""

from comtypes import CLSCTX_ALL  # type: ignore
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume  # type: ignore


class VolumeControl:
    """
    A simple volume control class for managing speaker volume and mute state.
    """

    def __init__(self) -> None:
        self._devices = AudioUtilities.GetSpeakers()
        self._volume = self._devices.EndpointVolume

    def get_mute(self) -> bool:
        """Gets the current mute state of the speaker.
        Returns:
            bool: True if muted, False otherwise.
        """
        return bool(self._volume.GetMute())

    def set_mute(self, mute: bool) -> None:
        """Sets the mute state of the speaker.
        Args:
            mute (bool): True to mute, False to un-mute.
        """
        self._volume.SetMute(mute, None)

    def get_volume(self) -> float:
        """Gets the current volume level of the speaker.
        Returns:
            float: The current volume level (0.0 to 1.0).
        """
        return self._volume.GetMasterVolumeLevelScalar()

    def set_volume(self, scalar: float) -> None:
        """Sets the volume level of the speaker.
        Args:
            scalar (float): The volume level (0.0 to 1.0).
        """
        if not 0.0 <= scalar <= 1.0:
            raise ValueError("Volume scalar out of range.")
        self._volume.SetMasterVolumeLevelScalar(scalar, None)
