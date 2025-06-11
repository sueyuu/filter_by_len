import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from collections import defaultdict

# List of dataset prefixes (without extension)
datasets = [
    'Aleppo2017',
    'Brown2019',
    'Colas2019',
    'Hall2018',
    'Lynch2022',
    'Shah2019',
    'Tamborlane2008',
    'Wadwa2023'
]

for dataset in datasets:
    print(f"Processing {dataset}...")

    try:
        cgm_zip = np.load(f'{dataset}.zip', allow_pickle=True)
        time_zip = np.load(f'{dataset}_time.zip', allow_pickle=True)
    except FileNotFoundError:
        print(f"Files for {dataset} not found, skipping.")
        continue

    segment_lengths = defaultdict(list)
    subject_flags = {}
    detailed_lengths = []

    for cgm_key in cgm_zip.files:
        try:
            subject_id, segment_id = map(int, cgm_key.split('_'))
        except ValueError:
            continue

        cgm_data = cgm_zip[cgm_key]
        length = len(cgm_data)
        segment_lengths[subject_id].append(length)
        detailed_lengths.append([subject_id, segment_id, length])

        time_key = f"{cgm_key}_time"
        if time_key in time_zip.files:
            time_range = time_zip[time_key]
            if isinstance(time_range, np.ndarray):
                duration_days = len(time_range)

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
    with open(f'{dataset}_subject_segment_summary.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['SubjectID', '>=7_days', '>=14_days', 'ShortestLength'])
        for subject_id, stats in subject_flags.items():
            writer.writerow([
                subject_id,
                int(stats['>=7_days']),
                int(stats['>=14_days']),
                stats['shortest']
            ])

    # Save detailed lengths CSV
    with open(f'{dataset}_segment_length_details.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['SubjectID', 'SegmentID', 'Length'])
        writer.writerows(detailed_lengths)

    print(f"Saved CSV files for {dataset}.")
