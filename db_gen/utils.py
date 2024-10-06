import properties

class Utils:
    def __init__(self, tables, table_strings):
        self.table_strings = table_strings
        self.tables = tables
        self.log_errors = []

    def log(self, msg):
        if msg not in self.log_errors:
            self.log_errors.append(msg)

    def get_item_types_list(self, types):
        ret = []
        for item_type in self.tables.item_types_table:
            for t in types:
                if t == item_type["Code"]:
                    ret.append(item_type["Code"] + " = " + item_type["ItemType"])
        return ret
            
    def is_in_gamble_table(self, code):
        for row in self.tables.gamble_table:
            if row["code"] == code:
                return True
        return False

    def get_gamble_item_from_code(self, code):
        for row in self.tables.armor_table:
            if row["code"] == code and row["spawnable"] == str(1):
                for row_again in self.tables.armor_table:
                    if row_again["code"] != "" and row_again["code"] == row["normcode"] and self.is_in_gamble_table(row_again["code"]):
                        return self.get_item_name_from_code(row_again["code"]) + " (" + row_again["code"] + ")"
        for row in self.tables.weapons_table:
            if row["code"] == code and row["spawnable"] == str(1):
                for row_again in self.tables.weapons_table:
                    if row_again["code"] != "" and row_again["code"] == row["normcode"] and self.is_in_gamble_table(row_again["code"]):
                        return self.get_item_name_from_code(row_again["code"]) + " (" + row_again["code"] + ")"
        for row in self.tables.misc_table:
            if row["code"] != "" and row["code"] == code and row["spawnable"] == str(1) and self.is_in_gamble_table(row["code"]):
                return self.get_item_name_from_code(row["code"]) + " (" + row["code"] + ")"
        return "N/A"

    def get_all_equivalent_types(self, types):
        while True:
            keep_going = False
            for item_type in self.tables.item_types_table:
                if item_type["Code"] in types:
                    if item_type["Equiv1"] not in types:
                        types.append(item_type["Equiv1"])
                        keep_going = True
                    if item_type["Equiv2"] not in types:
                        types.append(item_type["Equiv2"])
                        keep_going = True
            if not keep_going:
                types.remove("")
                return types

    def is_of_item_type(self, types, include_types):
        # Build up a list of all types, then check if any of them are in include_types
        all_types = self.get_all_equivalent_types(types)
        return set(all_types) & set(include_types)

    def get_item_name_from_code(self, code, debug=True):
        for row in self.tables.armor_table + self.tables.weapons_table + self.tables.misc_table:
            if row["code"] == code:
                if self.table_strings.get(row["namestr"]) is not None:
                    return self.table_strings[row["namestr"]]
        if debug:
            self.log("No name found for code: " + code)
        return code
    
    def get_level_req_from_code(self, code):
        for row in self.tables.armor_table + self.tables.weapons_table + self.tables.misc_table:
            if row["code"] == code:
                return row["levelreq"]
        self.log("Could not get level req for code: " + code)
        return 0
    
    def get_bg_color_from_code(self, code):
        for item in self.tables.weapons_table + self.tables.armor_table:
            if code == item["ultracode"]:
                return 303030
            if code == item["ubercode"]:
                return 202020
        return 101010


    def get_automods(self, group, type1, type2):
        automods = []
        if group == "":
            return
        for autos in self.tables.automagic_table:
            if group == autos["group"] and self.is_of_item_type([type1, type2], [autos["itype1"], autos["itype2"], autos["itype3"], autos["itype4"], autos["itype5"], autos["itype6"], autos["itype7"]]) and not self.is_of_item_type([type1, type2], [autos["etype1"], autos["etype2"], autos["etype3"]]):
                props = []
                for i in range(3):
                    if autos["mod" + str(i+1) + "code"] != "":
                        props.append(properties.Property(self,
                                                         autos["mod" + str(i+1) + "code"],
                                                         autos["mod" + str(i+1) + "param"],
                                                         autos["mod" + str(i+1) + "min"],
                                                         autos["mod" + str(i+1) + "max"]))
                automods.append(props)
        return automods

    def short_to_long_class(self, class_code):
        for c in self.tables.player_class_table:
            if c["Code"] == class_code:
                return c["Player Class"]
        self.log("Unknown class: " + class_code)
        return "Unknown"

    def get_staffmod(self, code):
        for item in self.tables.armor_table + self.tables.weapons_table + self.tables.misc_table:
            if item["code"] == code:
                for item_type in self.tables.item_types_table:
                    if item_type["Code"] == item["type"] and item_type["StaffMods"] != "":
                        return self.short_to_long_class(item_type["StaffMods"])
        return ""

    def get_spelldesc(self, code):
        for row in self.tables.misc_table:
            if row["code"] == code:
                return self.table_strings.get(row["spelldescstr"], "")

    def get_monster_from_id(self, mon_id):
        for mon_stat_row in self.tables.mon_stats_table:
            if mon_stat_row["hcIdx"] == mon_id:
                return self.table_strings[mon_stat_row["NameStr"]]

    def get_base_url(self, code):
        for weapon in self.tables.weapons_table:
            if weapon["code"] == code:
                return "weapons.htm#" + code
        for armor in self.tables.armor_table:
            if armor["code"] == code:
                return "armors.htm#" + code
        return ""

    def get_item_type_name_from_code(self, code, debug=True):
        # Hard code "tors" because "Armor" is confusing
        if code == "tors":
            return "Body Armor"

        for row in self.tables.item_types_table:
            if row["Code"] == code:
                return row["ItemType"]

        for row in self.tables.misc_table:
            if row["code"] == code:
                return row["name"]

        if debug:
            print("Could not get item type name for: " + code)
        return code

    def get_all_parent_types(self, types):
        ret = list(types)
        for t in types:
            if t == "":
                continue
            for pt in self.tables.parent_types[t]:
                if pt == "":
                    continue
                ret.append(pt)
        return set(ret)
    
    def get_all_sub_types(self, types):
        ret = list(types)
        for t in types:
            if t == "":
                continue
            for st in self.tables.sub_types[t]:
                if st == "":
                    continue
                ret.append(st)
        return set(ret)

    def handle_hardcoded():
        # Handle the hard-coded stuff
        if stat.stat == "firemindam" and any(s.stat == "firemaxdam" for s in self.stats):
            for s in self.stats:
                if s.stat == "firemaxdam":
                    return True, self.utils.table_strings["strModFireDamageRange"].replace("%d", self.min, 1).replace("%d", s.max, 1) 
        if stat.stat == "firemaxdam":
            for s in self.stats:
                if s.stat == "firemindam":
                    return True, self.utils.table_strings["strModFireDamageRange"].replace("%d", s.min, 1).replace("%d", self.max, 1) 
        return False, None
        if stat.stat == "lightmindam" and any(s.stat == "lightmaxdam"):
            return True
        if stat.stat == "magicmindam" and any(s.stat == "magicmaxdam"):
            return True
        if stat.stat == "coldmindam" and any(s.stat == "coldmaxdam"):
            return True
        if stat.stat == "poisonmindam" and any(s.stat == "poisonmaxdam"):
            return True
        if stat.stat == "mindamage" and any(s.stat == "maxdamage"):
            return True
        return False, None
    

    def get_stat_string(self, properties):
        ret = ""
        all_stats = []
        for prop in properties:
            for stat in prop.stats:
                all_stats.append(stat)
        
        # Replace stats with group stats
        for stat in list(all_stats):
            if stat.isc is not None and stat.isc["dgrp"] != "":
                item_stats = set()
                isc_stats = set()
                # Gather all the stats on the item with the same dgrp as stat
                for s in list(all_stats):
                    if s.isc is not None and s.isc["dgrp"] == stat.isc["dgrp"]:
                        item_stats.add(s)
                # Gather all the isc stats with the same dgrp as stat
                for isc in self.tables.item_stat_cost_table:
                    if isc["dgrp"] == stat.isc["dgrp"]:
                        isc_stats.add(isc["Stat"])
                # Make sure each stat in isc is on item
                found_all = True
                for isc_item in isc_stats:
                    if not any(item.stat == isc_item for item in item_stats):
                        found_all = False
                if not found_all:
                    continue
                # Make sure that each entry in isc has a corresponding entry on the item with the same property value
                for isc in isc_stats:
                    found = False
                    for item_stat in item_stats:
                        if isc == item_stat.stat and item_stat.property_value_string == stat.property_value_string:
                            found = True
                    if found == False:
                        found_all = False
                if not found_all:
                    continue
                # Remove the stats from the item
                for item in item_stats:
                    all_stats.remove(item)
                # Change the stat to use the group stats
                stat.descfunc = stat.isc["dgrpfunc"]
                stat.descval = stat.isc["dgrpval"]
                stat.descstr2 = stat.property.get_descstr(stat.isc["dgrpstr2"])
                stat.descstr = stat.property.get_descstr(stat.isc["dgrpstrpos"])
                if stat.property.is_always_negative():
                    stat.descstr = stat.property.get_descstr(stat.isc["dgrpstrneg"])
                stat.stat_string = stat.property.get_stat_string(stat)
                all_stats.append(stat)
       
        # Sort the remaining stats based on priority
        for stat in sorted(all_stats, key=lambda x: int(x.priority), reverse=True):
            if stat.stat_string != "":
                ret = ret + stat.stat_string + "<br>"
            if stat.stat_string == "" and stat.stat not in ["poisonlength", "coldlength", "state"]:
                self.log("Could not get stat string for stat: " + stat.stat + " property: " + stat.property.code)
        return ret
