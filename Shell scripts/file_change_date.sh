##

offset=$1
direction=POS



if [[ $offset == -* ]]
then
  direction=NEG
  offset=${offset:1}
fi

echo "OFFSET: $direction $offset"

for i in $(find . -iname "*.jpg")
do
  mod_date=`stat $i | grep Modify | grep -Eo "2015.*?[^00000000]"`
  mod_date=${mod_date%?}
  echo "mod_date: $mod_date"
  #eg. date: 2015-11-21 19:09:18
  epoch_secs=`date +%s -d "$mod_date"`
  echo "EPOCH: $epoch_secs"
  NEXT_DATE=`date "+%Y-%m-%d %k:%M:%S" --date="@$((epoch_secs + 3600))"`
  echo "NEXT: $NEXT_DATE"
done;
