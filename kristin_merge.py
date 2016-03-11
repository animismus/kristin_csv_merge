# -*- coding: utf-8 -*-
# Kristin B. csv merge with pure py
# JF    070316
# Final script has to always be on kristin_merge.bat (embedded)

from os import getcwd
from os import listdir
from os.path import join
import csv
import time

# TODO
# CLEAN BEFORE EMBEDDING


# What cols to use for matching, if you want to align on anything more than the name, 
# add that columns name to list, e.g., aligning on Name + RT: index_on = [0, 1] 
# at the moment it's jus the name
# Name   R.T. (s)    Quant Masses    Area
#  0        1           2              3
index_on = [0]#,1]
# Name of the output file, a timestamp is added for control only.
outfn = "concated"







kd_dir =  getcwd()
# get current working directory for easy copy pasting of the script wherever it's necessary.
# REMOVE WHEN USING FOR REAL 
#^^^^^^^^^^^^^^^^^^^^<-------------------------------------------------------------
kd_dir = "C:/Users/jofi0012.AD/Desktop/kb_merge_2"

def idxer(line, index_on=index_on):
    return tuple([line[idx] for idx in index_on])

def main(dk_dir = kd_dir, index_on = index_on):
    # start the cmpd index dict
    cmpd_idx = {}
    # keep a log list to print in the end
    log = []
    # list of csv files
    csvs = [x for x in listdir(kd_dir) if ".csv" in x and not outfn in x]
    # holder for the actual final data 
    holder = []
    # holder for the file names to insert in the output file, since there might empty files
    header_holder = []
    header_idxs = []
    # non empty file idx
    fidx = 0
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
        # file header information
        fn_header = item.replace(".csv", "")
        header_holder.append(fn_header)

        # going through the lines
        for line in lines[1:]:
            # check if the compound name (line[0]) is in the cmpd_index
            # if it's there, just add to that like in the holder
            if idxer(line) in cmpd_idx.keys():
                holder[cmpd_idx[idxer(line)]] += line[1:]
            else:
                # the new compound will ocupy a new place in the holder at the end
                # so the current length of the holder is new idx for that compound
                cmpd_idx[idxer(line)] = len(holder)
                # append the new compound at the end of the holder with the necessary padding
                # the padding is because previous files did not have it
                holder.append([line[0], ] + ["" for i in range(4 * fidx)] + line[1:])
        log.append("File {} processed, ({} compounds)".format(fn_header, len(lines) - 1))

        # increase the file index, for the new compounds positioning.
        fidx += 1
        # idx list for the headers
        header_idxs.append(max([len(l) for l in holder]))

        # each time a file is processed, pad the lines to same length
        _max = max([len(l) for l in holder])
        for line in holder:
            line += ["" for _ in range(_max - len(line))]
            
    # making the col headers
    final_l = len(holder[0])
    cols = ['R.T. (s)', 'Quant Masses', 'Area', 'Peak S/N']
    holder[0] = ["Name", ] + cols * ((final_l) // len(cols))
    # making the file name headers
    file_headers = ["" for _ in range(final_l)]
    for fn_h, fn_i in zip(header_holder, [1,] + header_idxs[:-1]):
        file_headers[fn_i] = fn_h
        # file_headers += [fn_h, ] + ["" for _ in range(len(cols) - 1)]
    holder.insert(0, file_headers)
    return holder, log


if __name__ == "__main__":
    start = time.clock()
    # get the list with the actual data
    concated, log = main()
    # save the list to csv
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    with open(kd_dir + "/{}_{}.csv".format(timestamp, outfn), 'wb') as fh:
        csv.writer(fh, dialect="excel").writerows(concated)
    # save the log file
    log.append("Merging took {:.2f} seconds.".format(time.clock() - start))
    log = "\n".join(log)
    with open(kd_dir + "/{}_{}_log.txt".format(timestamp, outfn), 'wb') as fh:
        fh.write(log)



# DEBUG STUFF
# print "\n".join(log)
# print concated
# print "\n".join([";".join(line) for line in concated])
