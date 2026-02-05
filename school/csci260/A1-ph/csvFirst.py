"""
Program for calculating the average, standard deviation,
min, and max values from a CSV-file for USGS water gauge ph
values at the Colorado-Utah border for Calendar Year 2025.

Original Program by: Karl Castleton
Updated and Annotated by: Jake Dodd
Course: CSCI260-001
Date: 02/03/26
"""
# added some useful modules/features to the original code
import csv
import math
import datetime
from rich.table import Table
from rich.console import Console
console = Console()


def main() -> None:
    # read csv file, deliminating at every tab
    with open('ph_data/colorado_ph.txt', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t')

        i=0
        total=0.0
        totalSq=0.0
        count=0
        maxValue=0.0
        minValue=0.0
        # set max and min starting values to 0.0 for decimals in the data
        # (usually pH is measured to the hundredths decimal place but the
        # collected data never passes the tenths decimal place so we use that)
        first=True
        for row in spamreader:
            if row[0]=="USGS" and i<100:
                value=float(row[4])
                total+=value
                totalSq+=value*value
                if first:
                    maxValue=value
                    minValue=value
                    first=False
                else:
                    if maxValue<value:
                        maxValue=value
                    if minValue>value:
                        minValue=value
                count+=1
    # implemented a 'with open' style file write for data with access timestamp
    with (open("ph_data/calculated_ph_values", 'a')as calculated_file):
        data_info = ("Average, Standard Deviation, Minimum, and Maximum Values for\n"
                     "pH levels in Colorado water, at USGS Site-09163500, for the\n"
                     "Calendar Year 2025 —> ")
        calculated_file.write(data_info)

        current_date = datetime.date.today() #date and time stamp for file write
        current_time = datetime.datetime.now().time().replace(microsecond=0)
        calculated_file.write(f"Data accessed on [{current_date}] "
                              f"at [{current_time}]:\n\n")

        # Adjusted the decimal output to (10)**-1 for all floats
        calc_average = f'{total/count:>.1f}' # calculate average
        calculated_file.write(f"\tAverage:{calc_average:^8}\n")

        std_dev = math.sqrt((totalSq-(total*total/count))/(count-1)) # calculate std_dev
        calc_std_dev = f'{std_dev:>.1f}'
        calculated_file.write(f"\tStd Dev:{calc_std_dev:^8}\n")

        calc_min = f'{minValue:>.1f}' # calculate min
        calculated_file.write(f"\tMin:\t{calc_min:^8}\n")

        calc_max = f'{maxValue:>.1f}' #calculate max
        calculated_file.write(f"\tMax:\t{calc_max:^8}\n\n")

        # Used Python rich module to add a nice visual table with colored labels to the data
        ph_stats_table = Table(style='purple4', title="\n[bright_white on purple4]Average, Standard Deviation, "
                      "Minimum, and Maximum Values for pH levels in Colorado water,"
                      " at USGS Site-09163500 for the Calendar Year 2025:")
        # table columns
        ph_stats_table.add_column(f'[green]Average:', justify='center')
        ph_stats_table.add_column('[blue]Standard Deviation:', justify='center')
        ph_stats_table.add_column('[plum1]Minimum:', justify='center')
        ph_stats_table.add_column('[red3]Maximum:', justify='center')
        # table row
        ph_stats_table.add_row(calc_average, calc_std_dev, calc_min, calc_max)
        # rich Console() handles console output
        console.print(ph_stats_table)


if __name__ == '__main__':
    main()

