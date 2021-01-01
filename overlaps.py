import csv

bzamodcodes = []
bzamods = []

with open('BZAmods.csv') as infile:
    reader = csv.reader(infile, delimiter=',')
    line_count = 0
    
    for row in reader:
        if line_count == 0:
            bzamodcodes.append(row[0][3:9])
            bzamods.append(row[0][3:])
        else:
            mod = ''
            i = 0
            while row[0][i] != ' ':
                mod += row[0][i]
                i += 1
            bzamodcodes.append(mod)
            bzamods.append(row[0])
        line_count += 1
##print(bzamodcodes)
print(bzamods)

f = open('overseasmods.txt', mode='r')
if f.mode == 'r':
    contents = f.read()
    
##    print(len(contents))
    
    i = 0
    exchange_mods = []
    while i+3 < len(contents):
            j = i
            if contents[j:j+3] == '<b>':
                mod = ''
                j += 3
                while contents[j:j+4] != '</b>':
                    mod += contents[j]
                    j += 1
                if mod not in exchange_mods:
                    exchange_mods.append(mod)
            i += 1
    can_map = []
    cannot_map = []
    
    for m in bzamodcodes:
        if m in exchange_mods:
            can_map.append(m)
        else:
            cannot_map.append(m)

##    print(can_map)
##    print(cannot_map)
    can_map_titles = []
    for m1 in can_map:
        for m2 in bzamods:
            if m1 in m2:
                can_map_titles.append(m2)
                break

    cannot_map_titles = []
    for m1 in cannot_map:
        for m2 in bzamods:
            if m1 in m2:
                cannot_map_titles.append(m2)
                break

    with open('overlaps.csv', mode='w') as olfile:
        writer = csv.writer(olfile, delimiter=',')
        writer.writerow(['BZA mods that can be mapped overseas'])
        
        for m in can_map_titles:
            writer.writerow([m])
            
        writer.writerow([''])
        writer.writerow(['BZA mods that can NOT be mapped overseas'])

        for m in cannot_map_titles:
            writer.writerow([m])
        




            
