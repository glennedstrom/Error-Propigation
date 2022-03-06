
if [ -d 'data' ]; then
    files=`ls data`
else
    echo directory not specified
fi

python3 parse.py $files
