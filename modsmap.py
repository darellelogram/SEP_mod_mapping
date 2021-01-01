import csv

# extract module codes for BZA degree reqs
def getBZAmodcodes(fullModNamesFile, ModCodesFile)
    bzamodcodes = []
    with open(fullModNamesFile) as infile:
        reader = csv.reader(infile, delimiter=',')
        line_count = 0
        
        for row in reader:
            if line_count == 0:
                bzamodcodes.append(row[0][3:9])
            else:
                mod = ''
                i = 0
                while row[0][i] != ' ':
                    mod += row[0][i]
                    i += 1
                bzamodcodes.append(mod)
            line_count += 1
    print(bzamodcodes)

    with open(ModCodesFile, mode='w') as outfile:
        writer = csv.writer(outfile, delimiter=',')

        for code in bzamodcodes:
            writer.writerow([code])

getBZAmodcodes('BZAmods.csv', 'BZAmodcodes.csv')

# extract overseas university names
f = open('overseasmods.txt', mode='r')
if f.mode == 'r':
    contents = f.read()
    
    print(len(contents))
    i = 0
    unis = []
    all_mods = dict()
    while i+3 < len(contents):
        if contents[i:i+4] == '<h2>':
            entry = []
            uni = ''
            j = i+4

            # get name of uni
            while contents[j:j+5] != '</h2>':
                uni += contents[j]
                j += 1
                
            entry.append(uni)

            k = j+5
            SOCmodcount = 0 # number of mappable SOC mods
            BZAmodcount = 0 # number of mappable BZA mods
            uni_BZAmods = []

            # read through all mods offered by uni
            while contents[k:k+5] != '</ul>':
                # read name of module
                if contents[k:k+3] == '<b>':
                    mod = ''
                    k = k+3
                    while contents[k:k+4] != '</b>':
                        mod += contents[k]
                        k += 1
##                    print(mod)

                    SOCmodcount += 1
                    if mod in bzamodcodes and mod not in uni_mods:
                    # make sure there are no repeats, because some universities
                    # have more than 1 mod than maps to the same NUS mod
                        BZAmodcount += 1
                        uni_BZAmods.append(mod)
                        
                k += 1
            entry.append(BZAmodcount)
            entry.append(uni_BZAmods)
            entry.append(int(SOCmodcount/2)) # divide by 2 to get rid of foreign mods

            entry2['NUS mods'] = NUS_mods
            entry2['PU mods'] = PU_mods

            i = k+5
            
            unis.append(entry)
            unis2[uni] = entry2
            
                
        i += 1
        
with open('overseasunis.csv', mode='w') as unifile:
    writer = csv.writer(unifile, delimiter=',')
    writer.writerow(['University','no. of mappable BZA mods',\
                     'mappable BZA mods','no. of mappable Computing mods'])
    for uni in unis:
        writer.writerow(uni)

with open("mods_by_n_unis_offering.csv", mode = 'w') as mfile:
    writer = csv.writer(mfile, delimiter=",")
    writer.writerow(['Module', 'no. of unis offering it', 'Is it a BZA mod?', "Universities that offer it"])
    for mod, stats in all_mods.items():
        writer.writerow([mod, stats['count'], stats['BZA mod?']] + stats['Unis offering it'])

'''
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


        
