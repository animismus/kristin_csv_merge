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
outfn = "concated"

def main(dk_dir = kd_dir):
    # keep a log list to print in the end
    log = []
    # list of csv files
    csvs = [x for x in listdir(kd_dir) if ".csv" in x and not outfn in x]
    # holder for the actual final data 
    holder = []
    # holder for the file names to insert in the output file, since there might empty files
    header_holder = []
    # start going through them
    for item in csvs:
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
        
        # if the file is not empty, then starting taking care of stuff
        # add the file name to a header_holder
        fn_header = item.replace(".csv", "")
        header_holder.append(fn_header)
        # check if the holder is still empty and if so, 
        if len(holder) == 0:
            # populate it for the first time
            holder = lines
            # and create a compound index that will allow for easy tracking what line to append to
            cmpd_idx = {(line[0], line[1]): idx for idx, line in enumerate(holder)}
            log.append("File {} processed, ({} compounds)".format(fn_header, len(lines) - 1))
            continue
            
        # if the holder is not empty then start adding stuff
        else:
            # lines[0] is the header
            for line in lines[1:]:
                # check if the compound name (line[0]) is in the cmpd_index
                # if it's there, just add to that like in the holder
                if (line[0], line[1]) in cmpd_idx.keys():
                    holder[cmpd_idx[(line[0], line[1])]] += line[1:]
                else:
                    # the new compound will ocupy a new place in the holder at the end
                    # so the current length of the holder is new idx for that compound
                    cmpd_idx[(line[0], line[1])] = len(holder)
                    # append the new compound at the end of the holder with the necessary padding
                    # the padding is because previous files did not have it
                    holder.append([line[0], ] + ["" for i in range(4)] + line[1:])
                
            log.append("File {} processed, ({} compounds)".format(fn_header, len(lines) - 1))

        # each time a file is processed, pad the lines to same length
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
    
    return holder, log


if __name__ == "__main__":
    # get the list with the actual data
    concated, log = main()
    # save the list to csv
    with open(kd_dir + "/{}.csv".format(outfn), 'wb') as fh:
        csv.writer(fh, dialect="excel").writerows(concated)
    # save the log file
    log = "\n".join(log)
    with open(kd_dir + "/{}_log.txt".format(outfn), 'wb') as fh:
        fh.write(log)



# DEBUG STUFF
# print "\n".join(log)
# print concated
# print "\n".join([";".join(line) for line in concated])
