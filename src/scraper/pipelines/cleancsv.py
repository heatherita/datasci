import csv

journals = ['NY Times', 'Just the News', 'NY Post', 'CNN', 'Axios', 'Fox News', 'Daily Wire', 'Racket News']

workingdir = '/home/heather/data/scraper/'
cleandir = '/home/heather/data/scraper/cleaned/'
filename = 'headlines-20241106.csv'
filepath_dirty = workingdir+filename
filepath_clean = cleandir+filename

with open(filepath_dirty) as csvfile:
    reader = csv.DictReader(csvfile)
    newcsvlist = [['headline', 'journal', 'date']]
    for row in reader:
        newheadlinelist = []
        rowlist = list(row.values())
        jidx = 0
        didx = 0
        for i in range(len(rowlist)-1):
            if(rowlist[i] in journals):
                jidx = i
                didx = jidx + 1
        for j in range(jidx):
            newheadlinelist.append(rowlist[j])
        newjournal = rowlist[jidx]
        newdate = rowlist[didx]
        newheadline = ' '.join(newheadlinelist)
        newcsvlist.append([newheadline,newjournal,newdate])

with open(filepath_clean, mode='w',newline='\n') as file:
    writer = csv.writer(file,delimiter=';')
    writer.writerows(newcsvlist)