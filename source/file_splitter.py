import csv
import os

input_filename = 'ApidaeYellow_first10.csv'
lines_per_file = 3  # Change this to your desired chunk size

with open(input_filename, newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = next(reader)
    rows = list(reader)

    total_rows = len(rows)
    num_files = (total_rows + lines_per_file - 1) // lines_per_file

    base, ext = os.path.splitext(input_filename)

    for i in range(num_files):
        start = i * lines_per_file
        end = start + lines_per_file
        chunk = rows[start:end]
        output_filename = f"{base}{i+1}{ext}"
        with open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)
            writer.writerows(chunk)

print(f"Split {input_filename} into {num_files} files with up to {lines_per_file} lines each.")