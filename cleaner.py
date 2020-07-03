import json
import os.path
#import xlsxwriter
import re

f = open(os.path.dirname(__file__) + '/medicines.json')
allmedicines = json.load(f)
Medicine = {}
list_med = []
#pres_med = []
sell_med = []
comp_med = []
salt_med = []
cost_med = []
class_med = []
img_med = []

for i in allmedicines:
    list_med = i['Names List']
    #pres_med = i['Prescription']
    sell_med = i['Type of Sell']
    comp_med = i['Manufacturer']
    salt_med = i['Salt']
    cost_med = i['Cost']
    class_med = i['Therapeutic Class']
    img_med = i['Image Link']
    x = 0
    for j in list_med:
        Medicine[j] = [sell_med[x], comp_med[x], salt_med[x],  str(str(cost_med[2*x])+str(cost_med[2*x+1])), str(class_med[0]).title(), str(img_med[x])]
        x += 1

for i in Medicine.keys():
    Medicine[i][5] = "\""+re.findall(r'"(.*?)(?<!\\)"', Medicine[i][5])[0]+"\""

#print(Medicine)
with open('medicine-1mg.csv', 'w', encoding='utf-8') as file1:
    file1.writelines("Medicine Name,Type of Sell,Manufacturer,Salt,Cost,Therapeutic Class,Image Link\n")
    for i in Medicine.keys():
        file1.writelines(i+",")
        for j in Medicine[i]:
            file1.writelines(j+",")
        file1.writelines("\n")
