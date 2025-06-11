from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt

# Load zipped files
cgm_zip = np.load('Aleppo2017.zip', allow_pickle=True)
time_zip = np.load('Aleppo2017_time.zip', allow_pickle=True)

print("Available CGM data files:", cgm_zip.files)
print("Available time data files:", time_zip.files)

# Pick a CGM/time key
cgm_key = cgm_zip.files[0]
time_key = f"{cgm_key}_time"

if time_key in time_zip.files:
    cgm_data = cgm_zip[cgm_key]        # (10, 1440, 1)
    time_data = time_zip[time_key]     # (10,) -> array of datetime.date

    print(f"CGM data shape: {cgm_data.shape}")
    print(f"Time data shape: {time_data.shape}")

    segment_index = 0
    cgm_segment = cgm_data[segment_index].squeeze()  # (1440,)
    start_date = time_data[segment_index]            # datetime.date

    # Generate timestamps (1 per minute)
    time_stamps = [datetime.combine(start_date, datetime.min.time()) + timedelta(minutes=i) for i in range(1440)]

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(time_stamps, cgm_segment, color='blue', label=f'Segment {segment_index}')
    plt.xlabel('Time')
    plt.ylabel('CGM Value')
    plt.title(f'CGM Data over Time ({cgm_key}, Segment {segment_index})')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()
else:
    print(f"No matching time data found for {cgm_key}")
