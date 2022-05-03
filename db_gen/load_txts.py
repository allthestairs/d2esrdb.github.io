import os
import csv
import table_strings
import stat_formats

data_path = ""
for root, dirs, files in os.walk("../"):
    if "Data" in dirs:
        data_path = os.path.join(root, "Data")

def load_table(table_name):
    table = open(data_path + "/global/excel/" + table_name, newline='')
    return list(csv.reader(table, delimiter='\t'))

weapons_table = load_table("Weapons.txt")
armor_table = load_table("Armor.txt")
skills_table = load_table("Skills.txt")
skill_desc_table = load_table("SkillDesc.txt")
unique_items_table = load_table("UniqueItems.txt")
properties_table = load_table("Properties.txt")
item_stat_cost_table = load_table("ItemStatCost.txt")
item_types = load_table("ItemTypes.txt")

#for i, armor in enumerate(armor_table):
#    if i < 5:
#        print(armor[48])
