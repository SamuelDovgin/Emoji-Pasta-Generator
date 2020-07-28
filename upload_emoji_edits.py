import boto3

# python upload_emoji_edits.py

#s3 = boto3.resource('s3')

#for bucket in s3.buckets.all():
#        print(bucket.name)

s3 = boto3.client('s3')
s3.upload_file("emoji_edits.json", 
               "emoji-map-edits", 
               "emoji_edits.json",
               ExtraArgs={'ContentType': 'text/plain',
                          'ACL':'public-read'})