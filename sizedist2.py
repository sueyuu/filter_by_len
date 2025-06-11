import numpy as np
import matplotlib.pyplot as plt
import csv
from collections import defaultdict

# Load data
cgm_zip = np.load('Aleppo2017.zip', allow_pickle=True)
time_zip = np.load('Aleppo2017_time.zip', allow_pickle=True)

# Storage
segment_lengths = defaultdict(list)  # Lengths grouped by subject
subject_flags = {}  # For >=7 days, >=14 days, shortest length
detailed_lengths = []  # For full record of lengths

# Loop through CGM data keys
for cgm_key in cgm_zip.files:
    try:
        subject_id, segment_id = map(int, cgm_key.split('_'))
    except ValueError:
        continue  # Skip malformed keys

    # Load CGM data
    cgm_data = cgm_zip[cgm_key]
    length = len(cgm_data)
    segment_lengths[subject_id].append(length)
    detailed_lengths.append([subject_id, segment_id, length])

    # Time info: just use length of time range array
    time_key = f"{cgm_key}_time"
    if time_key in time_zip.files:
        time_range = time_zip[time_key]
        if isinstance(time_range, np.ndarray):
            duration_days = len(time_range)

            # Prepare per-subject duration info
            if subject_id not in subject_flags:
                subject_flags[subject_id] = {
                    '>=7_days': False,
                    '>=14_days': False,
                    'shortest': duration_days
                }

            if duration_days >= 7:
                subject_flags[subject_id]['>=7_days'] = True
            if duration_days >= 14:
                subject_flags[subject_id]['>=14_days'] = True
            if duration_days < subject_flags[subject_id]['shortest']:
                subject_flags[subject_id]['shortest'] = duration_days

# Save summary CSV
with open('subject_segment_summary.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['SubjectID', '>=7_days', '>=14_days', 'ShortestLength'])
    for subject_id, stats in subject_flags.items():
        writer.writerow([
            subject_id,
            int(stats['>=7_days']),
            int(stats['>=14_days']),
            stats['shortest']
        ])

# Save detailed segment lengths CSV
with open('segment_length_details.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['SubjectID', 'SegmentID', 'Length'])
    writer.writerows(detailed_lengths)

print("Saved 'subject_segment_summary.csv' and 'segment_length_details.csv'")

# --- Plot 1: Histogram of segment sizes (number of readings) ---
plt.figure(figsize=(10, 4))
all_lengths = [length for lengths in segment_lengths.values() for length in lengths]
plt.hist(all_lengths, bins=20, color='skyblue', edgecolor='black')
plt.title('Histogram of CGM Segment Sizes (Number of Readings)')
plt.xlabel('Segment Size (number of data points)')
plt.ylabel('Frequency')
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Plot 2: Per-subject histograms of duration (if you still want these) ---
# You can include this section if you want individual histograms for each subject's durations.
