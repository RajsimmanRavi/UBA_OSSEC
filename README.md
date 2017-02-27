## Synopsis

This project is basically a Proof-of-Concept of implementing **User Behaviour Analysis on cloud infrastructures (i.e. IaaS model) using OSSEC**. It utilizes OSSEC HIDS for monitoring of user shell commands on virtual machines and detects intruders based on those commands. The detection engine framework is based on **Naive Bayes** supervised machine learning model. We chose this method because it is a baseline method for text-based classification. Even with this simple model, our engine can detect an intruder with an accuracy of **69%**. Of course, this can be improved by other models and better data pre-processing methods (explained further in the report). In order to train our model, we used the public data-set: https://archive.ics.uci.edu/ml/datasets/UNIX+User+Data 

## Motivation

Our primary purpose of our project is to address the issue of identity detection for users working on cloud infrastructures. If there are private companies that host cloud systems and share those
resources with other vendors, it is critical for system admins (of that cloud owner company) to know who used the system and detect any suspicious behaviour.

For example, if company A owns a private cloud and vendors B and C deploy their products onto company A’s cloud infrastructure, then system admins of company A must know the users interacting with the system.

**Note:** VMs created on the cloud will have ‘root’ user access for the vendors (for deploying products). Hence, detecting unauthorized access by utilizing usernames is superfluous.

Therefore, we characterize the identity of the users based on how they interact with the system (i.e., user(s)’ shell commands). By using this input, we can characterize the behaviour of the user and detect any malicious intent or anomalous behaviour.

## Installation

The source code the Intruder Response Script and Intruder Detection Engine (**naive_Bayes.py** and **util.py**) are provided. The local_rules.xml and local_decoders.xml are also included. 
In order to deploy this framework, you need to install OSSEC Server on an independent VM and install OSSEC agent on the monitoring VM. 

You can utilize the local_decoders.xml and local_rules.xml to configure OSSEC. However, you need to configure ossec.conf to include these rules and active responses. 
More information regarding the OSSEC setup can be found on the following links:
- http://ossec-docs.readthedocs.io/en/latest/manual/rules-decoders/create-custom.html
- http://ossec-docs.readthedocs.io/en/latest/manual/ar/ar-custom.html

Once you've configured OSSEC, you can simply place the scripts on the designated places (such as /var/ossec/active-response/bin/). You may need to edit intruder_response_script.sh to include your email address in order to send alert emails.

Aso included in the project are the pre-processed data: **train_data.npz**. The complete data-set is also included under the **UNIX_user_data** directory.

## Contact

If you have any questions or issues, please send an email: rajsimmanr@gmail.com 
