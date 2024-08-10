# import matplotlib.pyplot as plt
# import pandas as pd

# df = pd.read_csv("test.txt", header=None) # header=None <-- assuming you have no header row
# df.columns = ["time", "pagecreation", "professions"]  # give names to columns

# plt.scatter(df["time"], df["pagecreation"])
# # plt.plot(df["time"], df["col2"], label="Col 2")
# # plt.plot(df["time"], df["col3"], label="Col 3")

# plt.xlabel("Time")
# plt.ylabel("Value")
# plt.title("My Graph")

# plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('alldatawebscraper.csv', on_bad_lines='skip')

# Create a plot
plt.figure(figsize=(80, 20))

# Plot each point with a label
for index, row in df.iterrows():
    plt.plot(row['Year'], row['PageCreation'], 'o', label=row['Occupation'])
    plt.annotate(row['Occupation'], (row['Year'], row['PageCreation']), textcoords="offset points", xytext=(0,5), ha='center')

# Add labels and title
plt.xlabel('Year 1')
plt.ylabel('Year 2')
plt.title('Plot of Points from CSV')

# Show legend
plt.legend(loc='best')

# Display the plot
plt.grid(True)
plt.show()
