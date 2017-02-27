import numpy as np
np.random.seed(42)   # For reproducing tests purposes

import argparse
from util import *
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import classification_report, accuracy_score

from sklearn.datasets import fetch_20newsgroups
import sys
import sqlite3 as lite


parser = argparse.ArgumentParser(description="*** User Behaviour Analysis using Executed shell commands ***")
parser.add_argument('-kf', '--kfold', help='Number of ways to split Training/Validation data sets', type=int)
parser.add_argument('-s_c','--session_cmds', required=False, help='session commands to predict the User', type=str)
args = parser.parse_args()

def insert_data():
    con = lite.connect('test.db')

    cur = con.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS VM_User_map;
        CREATE TABLE VM_User_map(Id INT, VM_IP TEXT, User_name TEXT, User_ID INT);
        INSERT INTO VM_User_map VALUES(1, '10.2.1.14', 'xxx', 7);
        INSERT INTO VM_User_map VALUES(2, '10.2.1.17', 'yyy', 5);
    """)

    con.commit()

    if con:
        con.close()

def get_user_ID_for_VM(ORIG_VM_IP):
    VM_IP=ORIG_VM_IP.strip()
    con = lite.connect('/var/ossec/test.db')
    cur = con.cursor()
    cur.execute('''SELECT User_ID FROM VM_User_map WHERE VM_IP=?''', (VM_IP,))
    #cur.execute("SELECT User_ID FROM VM_User_map WHERE VM_IP='10.2.1.14'")
    #print("Has to get something")
    row = cur.fetchone()
    #print("Row fetched: "+str(row[0]))
    if con:
        con.close()

    return row[0]


def naiveBayes(X_train, X_test, Y_train, Y_test=None):

    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(X_train)

    # TRANSFORM OCCURRENCES TO FREQUENCIES
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    # FIT MODEL
    clf = MultinomialNB().fit(X_train_tfidf, Y_train)

    X_test_counts = count_vect.transform(X_test)
    X_test_tfidf = tfidf_transformer.transform(X_test_counts)

    predicted = clf.predict(X_test_tfidf)

    if Y_test is None:
        return predicted
    else:
        expected = Y_test

        acc = accuracy_score(expected, predicted)
        return predicted, acc

def run_test_validation(kfold=None, session_cmds=None):

    train_features, train_labels = load_train_data()
    scores = []

    if kfold:
        #print("Starting kfold validation...")
        if kfold > 0:
            kf = KFold(n_splits=kfold, shuffle=True, random_state=42)
            for train_index, test_index in kf.split(train_features):
                X_train, X_test = train_features[train_index], train_features[test_index]
                Y_train, Y_test = train_labels[train_index], train_labels[test_index]
                predicted, acc = naiveBayes(X_train, X_test, Y_train, Y_test)
                expected = Y_test

                scores.append(round(acc,3))
                print(classification_report(expected, predicted))
            print("Accuracy Scores are: %s",scores)
            print("Average Accuracy: "+str(round(sum(scores)/len(scores),3)*100)+" %")
        else:
            X_train, X_test, Y_train, Y_test = train_test_split( train_features, train_labels, test_size=0.2, random_state=0)
            predicted, acc = naiveBayes(X_train, X_test, Y_train, Y_test)
            expected = Y_test

            acc = accuracy_score(expected, predicted)

            print(classification_report(expected, predicted))
            print("Accuracy: "+str(round(acc,3)*100)+" %")
    else:
        #print("Predicting User by session commands...")
        #print(str(session_cmds))
        session_cmds = session_cmds.strip()[1:-1]
        VM_IP = session_cmds.split("->")[0]
        #print ("VM IP is: "+str(VM_IP))
        session_cmds = session_cmds.split("COMMAND: ")[1]
        #print ("session_cmds is: "+str(session_cmds))
        #session_cmds =  [s.strip() for s in session_cmds[1:-1].split(',')]
        session_cmds =  [s.strip() for s in session_cmds.split(',')]
        predicted = naiveBayes(train_features,session_cmds, train_labels)
        #print("model predicts: "+str(predicted[0]))
	expected_user_id = get_user_ID_for_VM(VM_IP)
	#print(expected_user_id)
	#print(predicted[0])
        if predicted[0] != expected_user_id:
            print "Intruder"
        else:
            print "Owner"


def main():

    #insert_data()

    if args.kfold is None and args.session_cmds is None:
        print("Wrong Usage. Please use -h or --help flag for proper arguments")
    else:
        run_test_validation(args.kfold, args.session_cmds)

if __name__=="__main__":
    main()
