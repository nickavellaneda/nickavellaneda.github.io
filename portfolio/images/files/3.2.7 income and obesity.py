import cse
import numpy as np
import matplotlib.pyplot as plt
import os.path

reload (cse)
def make_PLTW_style(axes):
    for item in ([axes.title, axes.xaxis.label, axes.yaxis.label] +
             axes.get_xticklabels() + axes.get_yticklabels()):
        item.set_family('Georgia')
        item.set_fontsize(16)
directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(directory, 'obesity-income.csv')
datafile = open(filename, 'r')
data = datafile.readlines()
low_income_population_2000 = []
high_income_population_2000 = []
low_income_population_2010 = []
high_income_population_2010 = []
low_income_population_2014 = []
high_income_population_2014 = []
total_population_2000 = []
total_population_2010 = []
total_population_2014 = []
obesity_proportion_2000 = []
obesity_proportion_2010 = []
obesity_proportion_2014 = []

treatments = ['High Income Obese People', 'Low Income Obese People']
for column in data[2:]:
    population_2000, population_2010, population_2014, obesity_prevelence_2000, obesity_prevelence_2010, obesity_prevelence_2014, obesity_population_2000, obesity_population_2010, obesity_population_2014, average_income_2000, average_income_2010, average_income_2014  = column.split(',')
    total_population_2000.append(int(population_2000[0:-1]))
    total_population_2010.append(int(population_2010[0:-1]))
    total_population_2014.append(int(population_2014[0:-1]))
    obesity_proportion_2000.append(float(obesity_prevelence_2000[0:-1]))
    obesity_proportion_2010.append(float(obesity_prevelence_2010[0:-1]))
    obesity_proportion_2014.append(float(obesity_prevelence_2014[0:-1]))
    if int(average_income_2000) > 41774:
        high_income_population_2000.append(int(obesity_population_2000))
    if int(average_income_2000) <= 41774:
        low_income_population_2000.append(int(obesity_population_2000))
    if int(average_income_2010) > 49880:
        high_income_population_2010.append(int(obesity_population_2000))
    if int(average_income_2010) <= 49880:
        low_income_population_2010.append(int(obesity_population_2000))
    if int(average_income_2014) > 54963:
        high_income_population_2014.append(int(obesity_population_2000))
    if int(average_income_2000) <= 54963:
        low_income_population_2014.append(int(obesity_population_2000))
high2000= sum(high_income_population_2000)
low2000 = sum(low_income_population_2000)
high2010 = sum(high_income_population_2010)
low2010 = sum(low_income_population_2010)
high2014 = sum(high_income_population_2014)
low2014 = sum(low_income_population_2014)
data1 = [high2000, low2000] # use values from above
data2 = [high2010, low2010]
data3 = [high2014, low2014]
colors = ['blue', 'green']
fig, ax = plt.subplots(1, 3)
ax[0].pie(data1, labels = treatments,  colors=colors, autopct='%.0f%%')
ax[0].set_aspect(1)
ax[1].pie(data2, labels = treatments,  colors=colors, autopct='%.0f%%')
ax[1].set_aspect(1)
ax[2].pie(data3, labels = treatments,  colors=colors, autopct='%.0f%%')
ax[2].set_aspect(1)
ax[0].set_title('High Income vs Low Income 2000\n38210082 obese citizens') 
ax[1].set_title('High Income vs Low Income 2010\n38210082 obese citizens') 
ax[2].set_title('High Income vs Low Income 2014\n55435719 obese citizens') 
fig.show()


    
# Show the image data in a subplot


  

    
    
    
    