#!/bin/bash
# Reference: http://www.zedwood.com/article/bash-linux-sendmail-script

function fappend {
    echo "$2">>$1;
}

ACTION=$1
USER=$2
IP=$3
ALERTID=$4
RULEID=$5

LOCAL=`dirname $0`;
cd $LOCAL
cd ../
PWD=`pwd`


# Logging the call
echo "`date` $0 $1 $2 $3 $4 $5 $6 $7 $8" >> ${PWD}/../logs/active-responses.log

IP=`echo "$7" | cut -d "-" -f1`
echo $IP >> /var/ossec/logs/check.log

# Getting alert time
ALERTTIME=`echo "$ALERTID" | cut -d  "." -f 1`

# Getting end of alert
ALERTLAST=`echo "$ALERTID" | cut -d  "." -f 2`

# Getting full alert
COMMAND=`grep -A 10 "$ALERTLAST" ${PWD}/../logs/alerts/alerts.log | grep "COMMAND"`
echo $COMMAND >> /var/ossec/logs/check.log

COMMAND=`echo "\"$IP -> $COMMAND\""`
echo $COMMAND >> /var/ossec/logs/check.log

PYTHON_OUTPUT=`python /var/ossec/code/naive_Bayes.py -s_c "$COMMAND"`
echo "Python output is: $PYTHON_OUTPUT" >> /var/ossec/logs/check.log
if [[ $PYTHON_OUTPUT = "Intruder" ]];
then
    YYYYMMDD=`date +%Y-%m-%d-%H:%M:%S`

    TOEMAIL="xxxx";
    FREMAIL="xxxx";
    SUBJECT="Intruder Alert! - $YYYYMMDD";

    MSG="Based on our preliminary VM User Behaviour Analysis, we detected an intruder in a system. Please start the investigation promptly and notify the owner of the system."
    IP_ADDR="VM IP Address: $IP"
    COMMAND="Shell command used: $COMMAND"

    MSGBODY=`echo -e "$MSG\n\n$IP_ADDR\n$COMMAND"`

    # DON'T CHANGE ANYTHING BELOW
    TMP=`mktemp`

    rm -rf $TMP;
    fappend $TMP "From: $FREMAIL";
    fappend $TMP "To: $TOEMAIL";
    fappend $TMP "Reply-To: $FREMAIL";
    fappend $TMP "Subject: $SUBJECT";
    fappend $TMP "";
    fappend $TMP "$MSGBODY";
    fappend $TMP "";
    fappend $TMP "";
    cat $TMP|sendmail -t;
    rm $TMP;

    echo "Notified an admin regarding this issue." >> ${PWD}/../logs/active-responses.log
else
    echo "No intruder found." >> ${PWD}/../logs/active-responses.log
fi
