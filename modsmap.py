'''
Format of HTML:
<h2> Name of Uni </h2>
<ul>
<table class="newtab">
<tbody>
<tr><th>NUS Module</th><th>PU Module</th></tr>
<tr>
<td><b>CS2010</b> Data Structures and Algorithms II</td>    - NUS mod
<td><b>CSCI2720</b> Data Structures</td>                    - overseas mod
</tr>
... more rows in the same format ...
</tbody>
</table>
</ul>
... more tables in the same format ...

'''

import csv

# extract module codes for BZA degree reqs
def getBZAmodcodes(fullModNamesFile, ModCodesFile):
    bzamodcodes = dict()
    with open(fullModNamesFile) as infile:
        reader = csv.reader(infile, delimiter=',')
        line_count = 0
        for row in reader:
            if line_count == 0:

                modcode = row[0][3:9]
                modname = row[0][10:]
                bzamodcodes[modcode] = modname
            else:
                modcode = ''
                modname = ''
                i = 0
                while row[0][i] != ' ':
                    modcode += row[0][i]
                    i += 1
                i += 1
                modname += row[0][i:]
                bzamodcodes[modcode] = modname
            line_count += 1
    with open(ModCodesFile, mode='w') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        for code in bzamodcodes:
            writer.writerow([code])
    return bzamodcodes

bzamodcodes = getBZAmodcodes('BZAmods.csv', 'BZAmodcodes.csv')

f = open('overseasmods.txt', mode='r')
if f.mode == 'r':
    contents = f.read()
    
    print(len(contents))
    i = 0
    unis2 = dict()
    while i+3 < len(contents):
        if contents[i:i+4] == '<h2>':
            entry2 = dict();
            uni = ''
            j = i+4

            # get name of uni
            while contents[j:j+5] != '</h2>':
                uni += contents[j]
                j += 1
                
            unis2[uni] = dict()
            NUS_mods = dict()
            PU_mods = dict()
            isNUSmod = True

            k = j+5
            
            # read through all mods offered by uni
            while contents[k:k+5] != '</ul>':
                # read name of module
                if contents[k:k+3] == '<b>':
                    modcode = ''
                    k = k+3 # start reading after <b>
                    while contents[k:k+4] != '</b>':
                        modcode += contents[k]
                        k += 1
                    k += 4
                    modname = ''
                    while contents[k:k+5] != '</td>':
                        modname += contents[k]
                        k += 1
                    if isNUSmod:
                        NUS_mods[modcode] = modname
                    else:
                        PU_mods[modcode] = modname
                    isNUSmod = not isNUSmod
                k += 1
            # after extracting all the modules offered by this particular uni...
            SOCmodcount = 0 # number of mappable SOC mods
            BZAmodcount = 0 # number of mappable BZA mods
            uni_BZAmods = [] # list of BZA mods offered by this uni

            # collate the stats for the number of SOC and BZA mods respectively
            for modcode, modname in NUS_mods.items():
                SOCmodcount += 1
                if modcode in bzamodcodes:
                    BZAmodcount += 1
                    uni_BZAmods.append(modcode+' '+modname)
            
            entry2['NUS mods'] = NUS_mods
            entry2['PU mods'] = PU_mods
            entry2['stats'] = {"SOCmodcount": SOCmodcount, \
                                   "BZAmodcount": BZAmodcount, \
                               "ListBZAmods": uni_BZAmods}

            # i starts after the '</ul>'
            i = k+5
            unis2[uni] = entry2
            
        i += 1

all_mods2 = dict()
for uni, mod_dict in unis2.items():
    for modcode, modname in mod_dict['NUS mods'].items():
        if modcode in all_mods2:
            # some unis map multiple mods to the same NUS mod.
            if uni not in all_mods2[modcode]["Unis offering it"]:
                all_mods2[modcode]["count"] += 1
                all_mods2[modcode]["Unis offering it"].append(uni)
            if modcode in bzamodcodes:
                all_mods2[modcode]["BZA mod?"] = True
        else:
            all_mods2[modcode] = {"modname": modname, "count": 0, \
                                  "BZA mod?": False, "Unis offering it": []}
            if modcode in bzamodcodes:
                all_mods2[modcode]['BZA mod?'] = True  

with open("mods_by_n_unis_offering2.csv", mode = 'w') as mfile2:
    writer = csv.writer(mfile2, delimiter=",")
    writer.writerow(['Module code', 'Module name', 'no. of unis offering it', 'Is it a BZA mod?', "Universities that offer it"])
    for modcode, stats in all_mods2.items():
        writer.writerow([modcode, stats['modname'], stats['count'], stats['BZA mod?']] \
                        + stats['Unis offering it'])
        
with open('overseasunis2.csv', mode='w') as unifile:
    writer = csv.writer(unifile, delimiter=',')
    writer.writerow(['University', 'Number of mappable Computing mods', \
                     'Number of mappable BZA mods','List of mappable BZA mods'])
    for uni, details in unis2.items():
        writer.writerow([uni, details['stats']['SOCmodcount'], details['stats']['BZAmodcount']] \
                        + details['stats']['ListBZAmods'])



        
