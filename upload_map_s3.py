import boto3

# python upload_map_s3.py

#s3 = boto3.resource('s3')

#for bucket in s3.buckets.all():
#        print(bucket.name)

s3 = boto3.client('s3')
s3.upload_file("emoji_mapping.json", 
               "emoji-map", 
               "emoji_mapping.json",
               ExtraArgs={'ContentType': 'text/plain',
                          'ACL':'public-read'})