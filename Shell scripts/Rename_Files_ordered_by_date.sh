#ONE LINE VERSION
#export counter=1;for i in $(ls -tr); do echo $i;echo $counter;mv $i "NewName_$counter.jpg";let counter=$counter+1;done;

if [ $# -lt 1 ]
  then
    echo "No arguments supplied"
    echo "Usage: ./Rename_files_ordered_by_date.sh <WORKING_DIR> <FILE_PREFIX (optional)>"
    echo "e.g. ./Rename_files_ordered_by_date.sh /home/test myfile_ or ./Rename_files_ordered_by_date.sh /home/test"
    exit 1
fi


if [ -z "$2" ]
then
  PREFIX=NewName
else
  PREFIX=$2
fi

echo "FIle Prefix: $PREFIX"
echo "Directory: $1"

export counter=1
for i in $(ls -tr $1)
do 
  echo $i
  echo $counter
  mv $i "$PREFIX_$counter.jpg"
  let counter=$counter+1
done
