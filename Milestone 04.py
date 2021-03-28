import boto3
import os
import time
import img2pdf

s3_client = boto3.client('s3')
count = 0
print("Monitoring the change in Bucket of Images...")
while True:
    images = []
    
    bucket = boto3.resource('s3').Bucket('scrappedimages')
    for file in bucket.objects.all():
        images.append(file.key)
    
    if len(images) == count:
        print("<---- Monitor No Change ---->")
        continue
    print("<---- Monitor Some Change ---->")
    print("\nDownloading the Images.........")
    try:
        os.mkdir(os.path.join(os.getcwd(), 'DownloadedImages'))
    except:
        pass
    for image in images:
        s3_client.download_file("scrappedimages", image, "DownloadedImages/" + image)
    print("Process of Downloading Images has been successfully completed!")
    print("------")
    print("Converting the Downloaded Images into PDF...")
    with open("jpd2pdf.pdf", "wb") as f:
        f.write(img2pdf.convert(["DownloadedImages/" + i for i in os.listdir("./DownloadedImages") if i.endswith(".jpg")]))
    print("Conversion Completed!\n\nUploading PDF to S3 Bucket...")
    s3_client.upload_file('jpd2pdf.pdf', 'scrappedimages', 'jpd2pdf.pdf')
    print("Uploading completed!")
    count = len(images)
    time.sleep(5)

