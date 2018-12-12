def dose(pitch_x, pitch_y, passes, current, dwell_time):
    dose = (dwell_time * passes * current)/(pitch_x * pitch_y)
    # nC/µm^2
    return dose