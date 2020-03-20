## Batch Processing of images using Amazon Rekognition API

Amazon Rekognition makes it easy to add image and video analysis to your applications using proven, highly scalable, deep learning technology that requires no machine learning expertise to use. With Amazon Rekognition, you can identify objects, people, text, scenes, and activities in images and videos, as well as detect any inappropriate content. Amazon Rekognition also provides highly accurate facial analysis and facial search capabilities that you can use to detect, analyze, and compare faces for a wide variety of user verification, people counting, and public safety use cases.
There are possible scenarios where a customer might want to process a large batch of images using Rekognition to process the backfills. This package provides a easy solution where you can copy the image URLs in a csv file and use that file as input to Amazon Rekognition for analyzing and finally writing the output to another CSV file containing analysis of all the input images.
This program will take three inputs.
1.	Input csv containing image URLs
2.	Temporary S3 bucket name. This bucket will be deleted once the job is complete
3.	Final output csv file name
 
The Program will also write individual outputs against each image in text format. Currently the parameter min_confidence is set to 60%. This can be changed based on the accuracy requirements of the analysis. The AWS region is set to us-west-2 and if you want to run this program anywhere else, please change the region variable in the program.


## License

This library is licensed under the MIT-0 License. See the LICENSE file.
