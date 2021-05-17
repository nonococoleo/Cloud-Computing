from utilities import *


def detect_faces(bucket, photo):
    client = get_boto_client('rekognition', 'us-east-2')
    response = client.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name': photo}}, Attributes=['ALL'])
    # print(response)
    ar = []
    for faceDetail in response['FaceDetails']:
        tempDict = dict()
        ## getting the age
        tempDict['AgeRange'] = (faceDetail['AgeRange']['Low'] + faceDetail['AgeRange']['High']) / 2
        ## getting the gender
        tempDict['Gender'] = faceDetail['Gender']['Value']
        ## getting the emotion and classify as three types
        emo = faceDetail['Emotions'][0]['Type']
        if emo == 'SAD' or emo == 'ANGRY' or emo == 'FEAR' or emo == 'CONFUSED' or emo == 'DISGUSTED':
            tempDict['Emotions'] = 'Negative'
        elif emo == 'HAPPY':
            tempDict['Emotions'] = 'Positive'
        else:
            tempDict['Emotions'] = 'Mild'
        ar.append(tempDict)
        # a valid tempDict looks like {'AgeRange': 20.0, 'Gender': 'Female', 'Emotions': 'Negtive'}

    return ar


def main(request):
    bucket, file = request["image_file"]
    res = detect_faces(bucket, file)
    return {'faceDetails': res}


if __name__ == "__main__":
    file = "files/images/1.jpg"
    bucket = "CHANGE THIS"
    obj_name = upload_image("user", file, bucket)

    res = main({"image_file": (bucket, obj_name)})
    print(res)
