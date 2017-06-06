import sys
import os
from multiprocessing.dummy import Pool as ThreadPool

import pandas as pd


def size(dataframe):
    rows, cols = dataframe.shape
    return rows

# dataframe: values from one degree of a scan
# return: one echo object
def anglesample(dataframe):
    a = dataframe['Time'].mean(), dataframe['Power'].mean(), dataframe['Phase'].mean(), dataframe['Doppler'].mean()
    return a


# Extract values for scan cycle
def extractscan(source, scan_time, prf):
    print('   Extracting file %s' % source)
    list_of_scans = []
    angle_time = (scan_time/360.0)
    try:
        data = pd.read_csv(source, header=None)
        data.columns = ['Time','Power','Phase','Doppler']
        max = size(data)
        max_t = data.iloc[max-1][0]
        print('   Data properties sz %i MxTime %f' % (max ,max_t) )
        #go through all datapoints (using timestamps)
        s=0 #scan counter
        hi=0
        while hi < max_t:
			#time bounds for scan
            lo = (s*scan_time)
            hi = lo + scan_time
			# get rows in range
            scan = data.query('%f <= Time <= %f' %(lo,hi))
            a=0
            df = pd.DataFrame(columns=('Time','Power','Phase','Doppler'))
            while(a < 360):
				# angle lower bound
                alo = (lo+(a*angle_time))
                ascan = scan.query('%f <= Time <= %f' % (alo,(alo+angle_time)))
                df.loc[a] = anglesample(ascan)
                a=a+1
            s=s+1
            # if sample is uneven we are near the end and disgard
            if size(df) < 359 :
                        break
            list_of_scans.append(df)
        print('== File %s processed' % source)

    except IOError:
        print('No file named '.join(source))
        sys.exit()

    return list_of_scans


def arg_err():
        print('Need more arguments: expected\n')
        print('targetFolder(classifier name followed by forward slash),\n')
        print('Source filename or folder (relative or actual path),\n')
        sys.exit()


def main(args):
    t = ''
    s = ''
    scan_time = 2
    prf = 1000

    res = []
    if len(args) > 2:
        t = args[1]
        s = args[2]
    else:
        arg_err()

    # setup training dir
    directory = os.path.dirname(t)
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as e:
            print('Directory not created, something went wrong\n%s'%str(e))
            sys.exit()

    # open file and do permutations
    sdir = os.path.dirname(s)
    # if directory exists open sources, else open single file
    if os.path.exists(sdir):
        print('Source dir exists..')
        source_folders = os.listdir(sdir)
        print('Sources found.. %s' % (source_folders))

        for folder_name in source_folders:
            #worker function
            def worker(fname):
                base,_ = fname.split('.')
                es = extractscan( '%s%s' % (src_subdir, fname), scan_time, prf )
                # Target Directory
                t_subdir = "%s/%s/" % (directory,folder_name)
                if not os.path.exists(t_subdir):
                    try:
                        os.makedirs(t_subdir)
                        print('   created subdir %s' % t_subdir)
                    except Exception as e:
                        print('Directory not created, something went wrong\n%s'%str(e))
                        sys.exit()
                # Write sample files
                smp = 0
                for sample in es:
                    fn = "%s/%s/%s_%i.csv" % (t, folder_name, base, smp)
                    sample.to_csv(fn, encoding='utf-8', index=None, header=None)
                    smp += 1
                print('   Created %s samples from %s\n' % (smp, folder_name))

            src_subdir = "%s/%s/" % ((sdir, folder_name))
            print('\n+ Traversing %s..' % src_subdir )
            sources = os.listdir(src_subdir)
            print('+ Found %i files..' % len(sources) )

            pool = ThreadPool(1) #bugs when using more than 1
            print('pool created')
            pool.map(worker, sources)
            print('mapped workload')
            pool.close()
            pool.join()
    else:
        res = sdir, extractscan(s, scan_time, prf)


if __name__ == '__main__':main(sys.argv)

