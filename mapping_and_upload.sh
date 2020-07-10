echo redditAccess.py $1 $2
python redditAccess.py $1 $2

echo emojiRelationMaker.py
python emojiRelationMaker.py

echo upload_map_s3.py
python upload_map_s3.py

echo Completed

if false
then
bash mapping_and_upload.sh new 50
fi