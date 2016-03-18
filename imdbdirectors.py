# coding=utf-8
import csv
import operator
import pygal
import unidecode
import re
from pygal.style import NeonStyle
STARTYEAR = 1941
CURRENTYEAR = 2016
dic = {}
gen = {}
myrat = [0]*10
irat = [0]*10
diffrat = [0]*10
years = [[0 for i in range(20)] for i in range(CURRENTYEAR-STARTYEAR+1)]
musicpos = 0
musicalpos = 0

with open('ratings.csv','rb') as csvfile:
    imdbreader = csv.reader(csvfile)
    for row in imdbreader:
        if row[6]!="Feature Film":
            continue
        if row[7] in dic:
            dic[row[7]] += 1
        else:
            dic[row[7]] = 1
        for genre in re.split(', ',row[12]):
            if genre in gen:
                gen[genre] += 1
            else:
                gen[genre] = 1
        myrat[int(row[8])-1] += 1
        irat[int(round(float(row[9])))-1] += 1
        diffrat[abs((int(row[8])-1)-(int(round(float(row[9])))-1))] += 1

print myrat
print irat

sortedgen = sorted(gen.items(), key=operator.itemgetter(1))
sortedgen.reverse()
for gentuple in sortedgen:
    if gentuple[0] == "music":
        musicpos = sortedgen.index(gentuple)
    if gentuple[0] == "musical":
        musicalpos = sortedgen.index(gentuple)
    
with open('ratings.csv','rb') as csvfile:    
    imdbreader = csv.reader(csvfile)
    for row in imdbreader:
        if row[6]!="Feature Film":
            continue
        for i in range(len(sortedgen)):
            if sortedgen[i][0] in row[12]:
                years[int(row[11])-STARTYEAR][i] += 1
                #bloody music-musical problem
                if i == musicpos and ("musical," in row[12] or ", musical" in row[12]):
                    years[int(row[11])-STARTYEAR][i] -= 1

sorted_dir = sorted(dic.items(), key=operator.itemgetter(1))
sorted_dir.reverse()
direc = [sorted_dir[i][0] for i in range(len(sorted_dir))]
mov = [sorted_dir[i][1] for i in range(len(sorted_dir))]

###Screw 1-movie directors
##for i in range(len(direc)):
##    if mov[i] == 1:
##        direc=direc[:i]
##        mov=mov[:i]
##        break

#Unicode conversion problems with Linux. Need to work on fixing that.
try:
	for i in range(len(direc)):
            if direc[i] == "Alfonso Cuarón":
                direc[i] = "Alfonso Cuaron"
            if direc[i] == "Stéphane Aubier, Vincent Patar":
                direc[i] = "Stephane Aubier, Vincent Patar"
            if direc[i] == "Alejandro G. Iñárritu":
                direc[i] = "Alejandro G. Inarritu"
            if direc[i] == "Mikael Håfström":
                direc[i] = "Mikael Hafstrom"
            if direc[i] == "Alejandro Amenábar":
                direc[i] = "Alejandro Amenabar"
            if direc[i] == "José Padilha":
                direc[i] = "Jose Padilha"
            if direc[i] == "Fernando Meirelles, Kátia Lund":
                direc[i] = "Fernando Meirelles, Katia Lund"
            if direc[i] == "René Cardona":
                direc[i] = "Rene Cardona"
#	    direc[i] = unidecode.unidecode(direc[i])
except:
	print direc[i]

bar_chart = pygal.Bar()
bar_chart.title = "Number of movies watched by Director"
bar_chart.x_labels = map(str, direc)
bar_chart.add('Movies', mov)
bar_chart.render_to_file('directors.svg')  

bar_chart = pygal.StackedBar(x_title='<--1941 to 2015-->',show_minor_x_labels=False,x_label_rotation=0.05,human_readable=True,legend_at_right=True,style=NeonStyle)
bar_chart.title = "Dom's Movies by Year and Genre"
bar_chart.x_labels = map(str, range(STARTYEAR,CURRENTYEAR+1))
bar_chart.x_labels_major = [str(i) for i in range(1945,CURRENTYEAR+1,5)]
for i in range(len(sortedgen)):
    bar_chart.add(sortedgen[i][0],[row[i] for row in years])
bar_chart.render_to_file('moviesstacked.svg')

bar_chart = pygal.Bar()
bar_chart.title = "Dom's Movies by Year and Genre"
bar_chart.x_labels = map(str, range(STARTYEAR,CURRENTYEAR+1))
for i in range(len(sortedgen)):
    bar_chart.add(sortedgen[i][0],[row[i] for row in years])
bar_chart.render_to_file('moviesunstacked.svg')

radar_chart = pygal.Line()
radar_chart.title = 'Dom\'s Ratings vs IMDB\'s Ratings'
radar_chart.x_labels = [str(i) for i in range(1,11)]
radar_chart.add('Dominic', myrat)
radar_chart.add('IMDB', irat)
radar_chart.render_to_file('rateline.svg')

radar_chart = pygal.Line()
radar_chart.title = 'Differences - Dom\'s Ratings vs IMDB\'s Ratings'
radar_chart.x_labels = [str(i) for i in range(1,11)]
radar_chart.add('Differences', diffrat)
radar_chart.render_to_file('diffrateline.svg')
