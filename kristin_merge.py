# Kristin B. csv merge with pure py
# JF    040316
# Will be embedded with in a bat for easy handling (kristin_merge.bat)

from os import getcwd
from os import listdir
from os.path import join
import csv

# get current working directory for easy copy pasting of the script wherever it's necessary.
kd_dir =  getcwd()
kd_dir = "C:/Users/jofi0012.AD/Desktop/kb_merge"

def main():
    # keep a log list to print in the end
    log = []
    count = 0
    # list of csv files
    csvs = [x for x in listdir(kd_dir) if ".csv" in x]
    # name for the first row naming scheme
    fn_headers = [item.replace(".csv", "") for item in csvs]
    # holder for the actual final data 
    holder = []
    header_holder = []
    # start going through them
    for item, fn_header in zip(csvs, fn_headers):
        # actual file name to scrape
        fn = join(kd_dir, item)
        
        # get file contents
        with open(fn, 'r') as csvfile:
            # decided to just get the lines, as the object from csv.reader is a generator
            lines = [line for line in csv.reader(csvfile, delimiter=',', quotechar='"')]
        # IF FILE IS EMPTY (i'm guessing file could have the headers and no compounds)
        if len(lines) <= 1:
            log.append("File {} was empty, please re-check this <----".format(fn_header))
            continue
        
        header_holder.append(fn_header)
        # check if the holder is still empty and if so, 
        if len(holder) == 0:
            # populate it for the first time
            holder = lines
            # insert is a mutator method <---------------------
#             holder.insert(0, ["", fn_header, "", "", ""])
            # and create a compound index
            cmpd_idx = {(line[0], line[1]): idx for idx, line in enumerate(holder)}
            log.append("File {} processed, ({} compounds)".format(fn_header, len(lines) - 1))
            count += 1

            continue
            
        # if the holder is not empty the, start adding stuff
        else:
            # lines[0] is the header
            for line in lines[1:]:
                # check if the compound name (line[0]) is in the cmpd_index
                # if it's there, just add to that like in the holder
                if (line[0], line[1]) in cmpd_idx.keys():
                    holder[cmpd_idx[(line[0], line[1])]] += line[1:]
                else:
                    # the new compound will ocupy a new place in the holder at the end
                    # so the current lenght of the holder is new idx for that compound
                    cmpd_idx[(line[0], line[1])] = len(holder)
                    # append the new compound at the end of the holder with the necessary padding
                    holder.append([line[0], ] + ["" for i in range(4)] + line[1:])
                
            log.append("File {} processed, ({} compounds)".format(fn_header, len(lines) - 1))
            count += 1


        # irrespective of new compound or not, add the headers
        # file id header <----------------
#         holder[0] += [fn_header, "", "", ""]
        # column headers <--------------------------
#         holder[1] += holder[1][-4:]

        # check for lens after appends done
        # pad to same lenght(if this file didn't have one or two compounds)
#         for line in holder:
#             line += ["" for _ in range(count*4 + 5 - len(line))]
        _max = max([len(l) for l in holder])
        for line in holder:
            line += ["" for _ in range(_max - len(line))]
            
    # making the col headers
    cols = ['R.T. (s)', 'Quant Masses', 'Area', 'Peak S/N']
    holder[0] = ["Name", ] + cols * (len(holder[0]) // len(cols))
    # making the file name headers
    file_headers = ["",]
    for fn_h in header_holder:
        file_headers += [fn_h, ] + ["" for _ in range(len(cols) - 1)]
    holder.insert(0, file_headers)
#     ^^^^^^^^
#     tou a usar os nomes dos ficheiros todos e alguns nao sao processados pk tao vazios
#     se calhar fazer lista de fn_headers e depois entao processar tudo
    
    
    return holder


# Num dos ficheiros há duas vezes o mm composto, mas com rts diferentes
# for line in sorted(main(), key = lambda x: x[0]):
concated = main()
for line in concated:
    print len(line), "\n", line, "\n"
#     if line[-1] != "": print "^^^^^^^^^^^^^^^^^^^^"

