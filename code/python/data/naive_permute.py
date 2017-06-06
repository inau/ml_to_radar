import sys
import os
import pandas as pd


def size(dataframe):
    rows, cols = dataframe.shape
    return rows


def processample(dataframe, n):
    extract = 0
    df = pd.DataFrame(columns=('Time','Power','Phase','Doppler'))
    sample = dataframe[extract*n:extract*n + n]
    while(extract*n < size(dataframe)):
        #update value
        a = sample[0].mean(), sample[1].mean(), sample[2].mean(), sample[3].mean()
        df.loc[extract] = [ a[i] for i in range(4)]
        #new sample
        extract = extract + 1
        sample = dataframe[extract*n:extract*n + n]
    return df


# Extract values for scan cycle
def extractScan(source, scan_time):
    print('   Extracting file %s' % source)
    list_of_scans = []
    angle_time = (scan_time/360)
    try:
        data = pd.read_csv(source, header=None)
        # determine echo number
        t = 0
        first = data.iloc[0][0]
        max = size(data)
        n = 1
        scan_t = scan_time
        print('   Data properties sz %i t %f' % (max ,first) )
        while (n < max and scan_t > t ):
            t = data.iloc[n][0]
            n=n+2
        #sample data
        scan_size = n
        print('   Scan is %i rows' % (scan_size) )
        samples_taken = 0
        while (samples_taken * scan_size + scan_size) < size(data):
            low = samples_taken*scan_size
            sample = data[low:low+scan_size]
            list_of_scans.append( procesSample(sample, scan_size/revolution_samples ) )
            samples_taken = samples_taken + 1
            print('   Sampled %i scans' % samples_taken)
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

    res = []
    if len(args) > 2:
        t = args[1]
        s = args[2]
    else:
        arg_err()

    # open file and do permutations
    sdir = os.path.dirname(s)
    # if directory exists open sources, else open single file
    if os.path.exists(sdir):
        print('Source dir exists..')
        source_folders = os.listdir(sdir)
        tmp = []
        for folder_name in source_folders:
            subdir = "%s/%s/" % ((sdir,folder_name))
            print('\n+ Traversing %s..' % subdir )
            sources = os.listdir(subdir)
            print('+ Found %i files..' % len(sources) )
            for f in sources:
                es = extractScan( '%s%s' % (subdir,f), scan_time)
                tmp = tmp + es
            res.append( (folder_name, tmp) )
            tmp = []
    else:
        res = sdir, extractScan(s, scan_time)

    # setup training dir
    directory = os.path.dirname(t)
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as e:
            print('Directory not created, something went wrong\n%s'%str(e))
            sys.exit()

    # write samples to training dir
    for n,scans in res:
        print('\n++ Processing %s with %i scans' % (n,len(scans)))
        subdir = "%s/%s/" % (directory,n)
        if not os.path.exists(subdir):
            try:
                os.makedirs(subdir)
            except Exception as e:
                print('Directory not created, something went wrong\n%s'%str(e))
                sys.exit()
        print('   created subdir %s' % subdir)

        smp = 0
        for sample in scans:
            fn = "%s/%s/%s_sample%i.csv" % (t, n,n, smp)
            sample.to_csv(fn, encoding='utf-8', index=None, header=None)
            smp += 1
        print('   Created %s samples from %s\n' % (smp, n))


if __name__ == '__main__':main(sys.argv)
