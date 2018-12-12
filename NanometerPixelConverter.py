class NanometerPixelConverter:
    def __init__(self, pitch_nm: float):
        self._pitch_nm = pitch_nm

    def to_pixel(self, value_nm: float) -> int:
        return int(value_nm / self._pitch_nm)

    def to_nm(self, value_pixel: int) -> float:
        return value_pixel * self._pitch_nm
        