## change the image creation time (only change hours for now, so that we can manage the different timezone)

if [ $# -lt 1 ]
  then
    echo "No arguments supplied"
    echo "Usage: ./file_change_date.sh <HOUR_NUMBER>"
    echo "e.g. ./file_change_date.sh -5 or ./file_change_date.sh 7"
    exit 1
fi

offset=$1
direction=POS



if [[ $offset == -* ]]
then
  direction=NEG
  #offset=${offset:1}
fi

echo "OFFSET: $direction $offset"

for i in $(find . -iname "*.jpg")
do
  echo "$i"
  mod_date=`stat $i | grep Modif | sed 's/\.000000000.*//g' | sed 's/\(.*\)\([0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\} [0-9]\{2\}:[0-9]\{2\}:[0-9]\{2\}\)/\2/g'`
  echo "mod_date: $mod_date"
  #eg. date: 2015-11-21 19:09:18
  epoch_secs=`date +%s -d "$mod_date"`
  #echo "EPOCH: $epoch_secs"
  increment=$((offset * 3600))
  #echo "increment $increment"
  NEXT_DATE=`date "+%Y-%m-%d %k:%M:%S" --date="@$((epoch_secs + increment))"`
  echo "NEXT: $NEXT_DATE"
  touch -d "$NEXT_DATE" $i
done;
