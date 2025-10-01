import csv
from typing import Iterable


def clean_file(input_path: str, output_path: str, journals: Iterable[str] | None = None):
    """Read an input CSV produced by the scraper and write a cleaned CSV.

    The function attempts to detect the journal column by matching known journal
    names. It constructs rows in the form [headline, journal, date].
    """
    journals = journals or ['NY Times', 'Just the News', 'NY Post', 'CNN', 'Axios', 'Fox News', 'Daily Wire', 'Racket News']

    with open(input_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        newcsvlist = [['headline', 'journal', 'date']]
        for row in reader:
            newheadlinelist = []
            rowlist = list(row.values())
            jidx = 0
            didx = 0
            for i in range(len(rowlist)-1):
                if rowlist[i] in journals:
                    jidx = i
                    didx = jidx + 1
            for j in range(jidx):
                newheadlinelist.append(rowlist[j])
            newjournal = rowlist[jidx] if jidx < len(rowlist) else ''
            newdate = rowlist[didx] if didx < len(rowlist) else ''
            newheadline = ' '.join(newheadlinelist)
            newcsvlist.append([newheadline, newjournal, newdate])

    with open(output_path, mode='w', newline='\n') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(newcsvlist)


if __name__ == '__main__':
    # Minimal CLI for convenience
    import sys
    if len(sys.argv) < 3:
        print('Usage: python cleancsv.py <input_csv> <output_csv>')
    else:
        clean_file(sys.argv[1], sys.argv[2])
