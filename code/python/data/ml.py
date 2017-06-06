import sys
import os
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import average_precision_score
from sklearn.metrics import precision_recall_fscore_support
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing as pp


def size(dataframe):
    rows, cols = dataframe.shape
    return rows


# Training directory is assumed to be a root folder
# Every 'label' is a sub directory, containing one csv file per sample
# Samples need to be of equal length
def training_data(trainingdir, colsToDrop):
    x = []
    y = []
    path = os.path.dirname(__file__)
    fp = "%s" % (trainingdir)
    labels = os.listdir(fp)
    for label in labels:
        #print('-- %s' %label)
        if label == '_img':
            continue
        samples = os.listdir('%s/%s/'%(trainingdir,label))
        #print('++ %s' % label)
        for sample in samples:
            df = pd.read_csv('%s/%s/%s'%(trainingdir,label,sample), header=None)
            df = df.drop(df.columns[colsToDrop],axis=1)
            df = df.values
            if( len(df) != 360):
                continue
            x.append(np.array(df).flatten())
            y.append(label)
            #print(y)

    return x, y


# Test directory is assumed to be a root folder
# Every 'label' is a sub directory, containing one csv file per test
# tests need to be of equal length as the trained data
def test_data(testsdir, colsToDrop):
    s = []
    expected = []
    labels = os.listdir(testsdir)
    for label in labels:
        if label == '_img':
            continue
        #go through each label
        d_labels = os.listdir('%s/%s'%(testsdir,label))
        for test in d_labels:
            df = pd.read_csv('%s/%s/%s'%(testsdir,label,test), header=None)
            df = df.drop(df.columns[colsToDrop],axis=1)
            df = df.values
            if len(df) != 360:
                continue
            s.append(np.array(df).flatten())
            expected.append(label)

    return s, np.array(expected).flatten()


def printerr():
    print('Need more arguments, expects training directory')


def preprocessors():
    def mms(X):
        prep = pp.MinMaxScaler(feature_range=(0, 1))
        return prep.fit_transform(X)
    def ss(X):
        prep = pp.StandardScaler().fit(X)
        return prep.fit_transform(X)
    def nrm(X):
        norm = pp.Normalizer().fit(X)
        return norm.transform(X)
    return ('MinMaxScaler',mms),('StandardScaler',ss),('Normalizer',nrm)


def testClassifiers(train, test, sizes, ls, pp):
    clfs = [MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=sizes, random_state=1)]
    (Xtrain,ytrain) = train
    (Xtest,ytest) = test

    nm,f = pp
    # Preprocess both Training and Test data
    Xpptrain = f(Xtrain)
    Xpptest = f(Xtest)
    # train classifier with test data
    for clf in clfs:
        clf.fit(Xpptrain,ytrain)
        predict = clf.predict(Xpptest)
        #report = classification_report(ytest,predict)
        clf_rep = precision_recall_fscore_support(ytest, predict)
        out_dict = {
             "precision" :clf_rep[0].round(4)
#            ,"recall" : clf_rep[1].round(2)
 #           ,"f1-score" : clf_rep[2].round(2)
 #           ,"support" : clf_rep[3]
            }
        out_df = pd.DataFrame(out_dict, index = clf.classes_)
        r = '%i     ' % ls
        pr = []
        for v in out_df.icol(0):
            pr.append(v)
            r = '%s     %s' % (r, v)
        avg = accuracy_score(ytest,predict)
        r = '%s     %s' % (r, avg)
        return r #out_df.to_string(header=False)
        #return out_df


def writeout(layer_nb, con, train, test, pp, dir):
        nm, prp = pp
        result = '%s/2L_%s_var%i_static%i.csv' % (dir,nm,layer_nb,con)
        original = sys.stdout
        sys.stdout = open(result, 'w')

        print('#layers     EAST     NORTH       SOUTH       WEST       avg')
        for i in range (12,101,12):
            if layer_nb == 1:
                tp = (i,con)
            else:
                if layer_nb == 2:
                    tp = (con,i)
                else:
                    tp = (con,con)
            print('# Layers %s %s' % tp)
            print(testClassifiers(train, test, tp, i, pp))
        sys.stdout = original
        print('%s Done' % result)


def main(args):
    if len(args) > 2:
        directory = os.path.dirname('mlstats/')
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except Exception as e:
                print('Directory not created, something went wrong\n%s'%str(e))
                sys.exit()

        t = args[1]
        testfolder = args[2]
        drop = [0,2,3]
        train = training_data(t, drop)
        test = test_data(testfolder, drop)
        # setup stats dir

        pps = preprocessors()
        for pp in pps:
            for l in range(1,3):
                for con in range(32,101,32):
                    writeout(l,con,train,test, pp, directory)
    else:
        printerr()


if __name__ == '__main__':main(sys.argv)