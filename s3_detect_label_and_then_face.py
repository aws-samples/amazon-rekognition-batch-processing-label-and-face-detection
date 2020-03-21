# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#
# This program will take three inputs. 1) input csv containing image url 2) temporary S3 bucket name 3) final output csv file name.
# Program will also write individual outputs against each image in text format
# min_confidence is set to 60%. This can be changed based on the accuracy requirements.
# This is currently set for us-west-2 region
#

import os
import csv
import json
import requests
import sys
import boto3
from botocore.exceptions import ClientError, ConnectionError, ParamValidationError

# execute the code using command like "python2.7 s3_detect_label_and_then_face.py input-image-urls.csv temp03312020-s3-bucket rekognition-output.csv"
# Inputs

input=sys.argv[1]   			#input csv file conataining list of image urls
bucket_name=sys.argv[2] 		#temporary S3 bucket name.  This will be created and dropped at runtime 	
final_output=sys.argv[3]		#output csv file name. The analysis will be in the next column of the input file. e.g. col1 image url and col2 analysis


def detect_labels(bucket_name, outfile_name, min_confidence=60, region="us-west-2"):
        rekognition = boto3.client("rekognition", region)
        response = rekognition.detect_labels(
                Image={
                        "S3Object": {
                                "Bucket": bucket_name,
                                "Name": outfile_name,
                        }
                },
                MinConfidence=min_confidence,
        )
        return response['Labels']


def detect_faces(bucket_name, outfile_name, attributes=['ALL'], region="us-west-2"):
        rekognition = boto3.client("rekognition", region)
        response = rekognition.detect_faces(
            Image={
                        "S3Object": {
                                "Bucket": bucket_name,
                                "Name": outfile_name,
                        }
                },
            Attributes=attributes,
        )
        return response['FaceDetails']

s3 = boto3.resource('s3')

s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
    'LocationConstraint': 'us-west-2'})



file_reader=open(input)
read = csv.reader(file_reader)
count = 1
for row in read :
	image_url = row[0]
	outfile_name = 'image_input_' + str(count) + '.png'
	rekog_output = 'rekog_detect_personface_output_' + str(count) + '.txt'
	# URL of the image to be downloaded is defined as image_url
	r = requests.get(image_url) # create HTTP response object

	# send a HTTP request to the server and save
	# the HTTP response in a response object called r

	open(outfile_name,'wb').write(r.content)
	print ("Processing started for " + outfile_name)
	print ("Input Image: " + image_url)
	print ('Temporarily Copying the file to S3 ' )
	s3 = boto3.resource('s3')
	s3.Bucket(bucket_name).upload_file(outfile_name,outfile_name)
	

	if __name__ == "__main__":

    		imageFile=outfile_name
    		client=boto3.client('rekognition')

		try:
			print ("Starting Label Detection for image " + image_url)
			with open(rekog_output,'w') as f:
        			f.write('Detected labels in ' + image_url + '\n')
        			for label in detect_labels(bucket_name,imageFile):
                			f.write(label['Name'] + ' : ' + str(label['Confidence']) + '\n')
        			f.write('Done with detect labels...' + '\n')
		except (RuntimeError, TypeError, NameError, KeyError, AttributeError, ParamValidationError):
			pass

                except ClientError as e1:
                        print(e1)


        	except ConnectionError as e2:
			print(e2)

			f.close()
		

		with open(rekog_output) as f1:
    			contents = f1.read()

			if 'Person' in contents:
				print ("Person found in image " + image_url)	
				print ("Starting Face Detection for image " + image_url)
				try:
      		  	        	with open(rekog_output,'a') as f:
		
        		                	f.write('Detecting faces for ' + image_url + '\n')
                		        	for faceDetail in detect_faces(bucket_name,imageFile):
                        		        	f.write('The detected face is between ' + str(faceDetail['AgeRange']['Low'])
                                			+ ' and ' + str(faceDetail['AgeRange']['High']) + ' years old' + '\n')
                              		  		f.write('Here are the other attributes:' + '\n')
                                			f.write(json.dumps(faceDetail, indent=4, sort_keys=True) + '\n')
		
        		                	print('Done writing ' + rekog_output + '\n')
	
				except (RuntimeError, TypeError, NameError, KeyError, AttributeError, ParamValidationError):
					pass
		
        			except ClientError as e1:
                		        print(e1)
	
        	       	 	except ConnectionError as e2:
               			        print(e2)
			else:
				print('Done writing ' + rekog_output + '\n')	
			
		os.remove(outfile_name)                

		f.close()

                lines = [line.rstrip('\n') for line in open(rekog_output)]

                RESULTS=lines
                with open(final_output,"ab") as Output_csv:
                        CSVWriter = csv.writer(Output_csv, delimiter='\t')
                        CSVWriter.writerow(RESULTS)


	count = count + 1

bucket = s3.Bucket(bucket_name)

for key in bucket.objects.all():
    key.delete()
bucket.delete()

print ("Please find the final results in the file " + final_output + '\n' )

sys.exit()
