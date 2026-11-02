def rolling_sum(values, index, hours):
    if index + 1 < hours:
        return None

    window = values[index - hours + 1:index + 1]

    if any(value is None for value in window):
        return None

    return round(sum(window), 2)


def process_rainfall(hourly):
    times = hourly["time"]
    precipitation = hourly["precipitation"]

    if len(times) != len(precipitation):
        raise ValueError("Weather data lengths do not match")

    results = []

    for i, time in enumerate(times):
        results.append({
            "time": time,
            "rain_1h_mm": rolling_sum(precipitation, i, 1),
            "rain_3h_mm": rolling_sum(precipitation, i, 3),
            "rain_6h_mm": rolling_sum(precipitation, i, 6)
        })

    return results 