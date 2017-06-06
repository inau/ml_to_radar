import sys
import os
import math
import pandas as pd
import util as ut
import glob

# CSV file containing sample
# length per scan in seconds
# returns [sequence of data], predicted_direction
def predict(file, scan_t):
    data = pd.read_csv(file, header=None)
    data.columns=('t','p','ph','d')
#    print('%s loaded' % file)
    t0= math.floor(data.iloc[0]['t']) # round to nearest int
    tMx = t0 + scan_t
    idx = data['p'].argmax()
#    print('%i id contains max bounds %f to %f' % (idx,t0,tMx))
    t = data.iloc[idx]['t']
#    print('%f is time stamp' % t)
    dir_q = (scan_t/4.0) #1/4 of a rotation
    dir_o = (scan_t/8.0) #1/8 of a rotation
    lb=t0+dir_o
    ub=tMx-dir_o
    def ret(dir):
        return (data, dir)

    if t <= lb or t >= ub:
        return ret('east')
    else:
        if t <= lb+dir_q:
            return ret('north')
        else:
            if t <= lb+(2*dir_q):
                return ret('west')
            else:
                return ret('south')

#	Input root dir
#	output file: if empty, defaults to stdout
def predict_stats(root, out = ''):
    # open root folder
    sourcedir = os.path.dirname(root)
    # if directory exists open sources, else open single file
    if os.path.exists(sourcedir):
        print('Source dir exists..')
        source_folders = os.listdir(sourcedir)
        print('Sources found.. %s' % (source_folders))

        results = []
        for folder_name in source_folders:
            positive = 0.0
            total = 0.0
            print('- traversing %s' % folder_name)
            dirs = glob.glob('%s%s/*.csv' % (root,folder_name))
            for csv in dirs:
                #                print('- - file %s' % csv)
                total += 1
                d,l = predict('%s'%csv, 2)
                #                print('Sample from %s predicted as %s' % (folder_name, l))
                if folder_name == l:
                    positive += 1.0
            results.append( (folder_name, positive, total) )

        old = sys.stdout
        if(out != ''):
            sys.stdout = open(out, 'w')
        print('#Label       correct     total       percentage')
        for r in results:
            l, p, t = r
            print('%s       %s      %s      %f' % (l,p,t,(p/t)))
        sys.stdout = old