import csv

input_file = 'champions_irl_stats.csv'
output_file = 'cleaned_output_file.csv'


with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
 
    header = next(reader)
    writer.writerow(header)
    
  
    for row in reader:
        row[2] = row[2].replace(',', '')  # Remove commas from "matches" column
        row[3] = str(float(row[3].replace('%', '')) / 100)  # Convert "win_rate" to decimal
        row[4] = str(float(row[4].replace('%', '')) / 100)  # Convert "pick_rate" to decimal
        row[5] = str(float(row[5].replace('%', '')) / 100)  # Convert "ban_rate" to decimal
        writer.writerow(row)
