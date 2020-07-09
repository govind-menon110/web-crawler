#Cleaning the individualmeds output given by finalspider3 (Step 4 - final)
import json
import os.path
#import xlsxwriter
import re

f = open(os.path.dirname(__file__) + '/individualmeds.json')
allmedicines = json.load(f)
Medicine = {}
for i in allmedicines:
    chem_class = ""
    habit_forming = ""
    if len(i['Chemical Class and Habit Forming']) == 2:
        chem_class = i['Chemical Class and Habit Forming'][0]
        habit_forming = i['Chemical Class and Habit Forming'][1]
    elif len(i['Chemical Class and Habit Forming']) == 1:
        if len(i['Chemical Class and Habit Forming']) > 3:
            chem_class = i['Chemical Class and Habit Forming'][0]
            habit_forming = "N/A"
        elif len(i['Chemical Class and Habit Forming']) <=3:
            habit_forming = i['Chemical Class and Habit Forming'][0]
            chem_class = "Not Listed"
    elif len(i['Chemical Class and Habit Forming']) == 0:
        habit_forming = "N/A"
        chem_class = "Not Listed"
    how_to_use = ""
    if type(i["How to Use"]) is list:
        for j in i['How to Use']:
            how_to_use += j
    else:
        how_to_use = i["How to Use"]

    alternate_meds = ""
    if type(i["Alternate Medicines"]) is list:
        for j in i['Alternate Medicines']:
            alternate_meds += j + ","
    else:
        alternate_meds = i["Alternate Medicines"]

    side_effects = ""
    if type(i["Side Effects"]) is list:
        for j in i['Side Effects']:
            side_effects += j + ","
    else:
        side_effects = i["Side Effects"]

    uses = ""
    if type(i["Uses"]) is list:
        for j in i['Uses']:
            uses += j + ","
    else:
        uses = i["Uses"]

    salt = ""
    if type(i["Salt"]) is list:
        for j in i['Salt']:
            salt += j + ","
    else:
        uses = i["Salt"]

    mrp = ""
    if type(i["MRP"]) is list:
        for j in i['MRP']:
            mrp += j
    else:
        mrp = i["MRP"]

    bp = ""
    if type(i["Best Price"]) is list:
        for j in i["Best Price"]:
            bp += j
    else:
        bp = i["Best Price"]

    Medicine[i['Name'][0]] = [i['Prescription'], i['Type of Sell'], i['Manufacturer'], salt, mrp, bp, uses, how_to_use, alternate_meds, side_effects, chem_class, habit_forming, i['Therapeutic Class'], i["Image Link"]]
        #[i['Prescription'], i['Type of Sell'], i['Manufacturer'], salt, str(i['MRP'][0]) + str(i['MRP'][1]), i['Best Price'], uses, how_to_use, alternate_meds, side_effects, chem_class, habit_forming, i['Therapeutic Class'], i["Image Link"]]

for i in Medicine.keys():
    Medicine[i][13] = "\"" + Medicine[i][13] + "\""
    Medicine[i][3] = "\"" + Medicine[i][3] + "\""
    Medicine[i][4] = "\"" + Medicine[i][4] + "\""
    Medicine[i][5] = "\"" + Medicine[i][5] + "\""
    Medicine[i][6] = "\"" + Medicine[i][6] + "\""
    Medicine[i][7] = "\"" + Medicine[i][7] + "\""
    Medicine[i][8] = "\"" + Medicine[i][8] + "\""
    Medicine[i][9] = "\"" + Medicine[i][9] + "\""
    Medicine[i][10] = "\"" + Medicine[i][10] + "\""

with open('medicine-1mg-full-updated-list.csv', 'w', encoding='utf-8') as file1:
    file1.writelines("Medicine Name,Prescription,Type of Sell,Manufacturer,Salt,MRP,Best Price,Uses,How to Use,Alternate Medicines,Side Effects,Chemical Class,Habit Forming,Therapeutic Class,Image Link\n")
    for i in Medicine.keys():
        file1.writelines(i+",")
        for j in Medicine[i]:
            if type(j) is list:
                for m in j:
                    file1.writelines(m+",")
            else:
                file1.writelines(j + ",")
        file1.writelines("\n")
