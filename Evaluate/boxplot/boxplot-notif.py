#!/opt/local/bin/python2.6
 
from pylab import *
import numpy as na
import matplotlib.font_manager
import csv
import sys
import itertools
 
elapsed = {}
temp = []

labels = ["Overall Notifications Elapsed", "Notification Range Differential per 10 Followers"]
 
# Parse the CSV files
for file in sys.argv[1:]:
  threads = int(file.split('-')[0])
  for label in labels :
    if not label in elapsed :
        elapsed[label] = {}
    if not threads in elapsed[label] :
      elapsed[label][threads] = []

    if label is labels[0] :
      for row in csv.reader(open(file), delimiter=' '):
        elapsed[label][threads].append(int(row[1]))

    if label is labels[1] :
      reader = csv.reader(open(file), delimiter=' ')
      rows = sorted(reader, key=lambda d: d[0])
      groups = itertools.groupby(rows, lambda d: d[0])
      for group in groups:
        row = [int(x[1]) for x in list(group[1])]
        range_number = max(row) - min(row)
        elapsed[label][threads].append(int(range_number))


# Draw a separate figure for each label found in the results.
for label in elapsed:
  # Transform the lists for plotting
  plot_data = []
  plot_labels = []
  for thread_count in sort(elapsed[label].keys()):
    plot_data.append(elapsed[label][thread_count])
    plot_labels.append(thread_count)

  # Start a new figure
  fig = figure(figsize=(9, 6))

  # Pick some colors
  palegreen = matplotlib.colors.colorConverter.to_rgb('#8CFF6F')
  paleblue = matplotlib.colors.colorConverter.to_rgb('#708DFF')
  palered = matplotlib.colors.colorConverter.to_rgb('#ff7070')

  # Plot response time
  ax1 = fig.add_subplot(111)
  ax1.set_yscale('log')
  bp = boxplot(plot_data, notch=0, sym='', vert=1, whis=0.75)

  # Tweak colors on the boxplot
  plt.setp(bp['boxes'], color='g')
  plt.setp(bp['whiskers'], color='g')
  plt.setp(bp['medians'], color='black')
  plt.setp(bp['fliers'], color=palegreen, marker='+')

  # Now fill the boxes with desired colors
  numBoxes = len(plot_data)
  medians = range(numBoxes)
  for i in range(numBoxes):
    box = bp['boxes'][i]
    boxX = []
    boxY = []
    for j in range(5):
      boxX.append(box.get_xdata()[j])
      boxY.append(box.get_ydata()[j])
    boxCoords = zip(boxX,boxY)
    boxPolygon = Polygon(boxCoords, facecolor=palegreen)
    ax1.add_patch(boxPolygon)

  # Label the axis
  ax1.set_title(label)
  ax1.set_xlabel('Number of concurrent users')
  ax1.set_ylabel('Milliseconds')
  ax1.set_xticks(range(1, len(plot_labels) + 1, 1))
  ax1.set_xticklabels(plot_labels[0::1])
  fig.subplots_adjust(top=0.9, bottom=0.15, right=0.85, left=0.15)

  # Turn off scientific notation for Y axis
  ax1.yaxis.set_major_formatter(ScalarFormatter(False))

  # Set the lower y limit to the match the first column
  ax1.set_ylim(ymin=bp['boxes'][0].get_ydata()[0])

  # Draw some tick lines
  ax1.yaxis.grid(True, linestyle='-', which='major', color='grey')
  ax1.yaxis.grid(True, linestyle='-', which='minor', color='lightgrey')
  # Hide these grid behind plot objects
  ax1.set_axisbelow(True)

  # Add a legend
  line1 = Line2D([], [], marker='s', color=palegreen, markersize=10, linewidth=0)
  prop = matplotlib.font_manager.FontProperties(size='small')
  figlegend((line1,), ('Elapsed Time',),
    'lower center', prop=prop, ncol=1)

  # Write the PNG file
  savefig(label)