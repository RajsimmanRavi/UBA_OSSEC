import sys
import numpy as np
import string
#import matplotlib.pyplot as plt

def read_contents(f_name):
    with open(f_name, 'r') as content_file:
        content = content_file.read()

    return content

def arr_to_list(data):
    cmd_list = []
    for row in data:
        user_cmd = ' '.join(str(e) for e in row)
        cmd_list.append(user_cmd)
    return cmd_list

def create_train_data():

    for i in range(0,10):
        print("Starting file USER"+str(i))
        file_content = read_contents("../UNIX_user_data/USER"+str(i))
        cmds = string.split(file_content,"\n")
        user_cmds_whole_string = ' '.join(str(e) for e in cmds)

        usr_cmd_sentences_list = string.split(user_cmds_whole_string, "**EOF**")
        #print("list length: %s",len(usr_cmd_sentences_list))
        usr_cmd_arr = np.array(usr_cmd_sentences_list)
        #print(usr_cmd_arr.shape)
        usr_cmd_label = np.full(len(usr_cmd_sentences_list), i, dtype=np.int)
        #print(usr_cmd_label.shape)

        if i == 0:
            train_features = usr_cmd_arr
            train_labels = usr_cmd_label
        else:
            train_features = np.concatenate((train_features, usr_cmd_arr), axis=0)
            train_labels = np.concatenate((train_labels, usr_cmd_label), axis=0)


    return train_features, train_labels

def load_train_data():
    data = np.load("/var/ossec/code/train_data.npz")
    train_features = data["train_features"]
    train_labels = data["train_labels"]

    #print train_features[-1]
    #print train_features.shape
    #print train_labels.shape
    return train_features, train_labels

def plot_labels(train_labels):
    plt.hist(train_labels, bins=10)
    plt.show()

def main():

    train_features, train_labels = load_train_data()
    plot_labels(train_labels)








if __name__=="__main__":
    main()
