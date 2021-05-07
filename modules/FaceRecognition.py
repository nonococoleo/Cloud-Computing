import boto3
import json


def detect_faces(bucket, photo):
    client = boto3.client('rekognition',
                          region_name='us-east-2',
                          aws_access_key_id='AKIARAQKMHEBYCZBBY5R',
                          aws_secret_access_key='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'
                          )
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
        if (emo == 'SAD' or emo == 'ANGRY' or emo == 'FEAR' or emo == 'CONFUSED' or emo == 'DISGUSTED'):
            tempDict['Emotions'] = 'Negtive'
        elif (emo == 'HAPPY'):
            tempDict['Emotions'] = 'Positive'
        else:
            tempDict['Emotions'] = 'mild'
        ar.append(tempDict)
        # a valid tempDict looks like {'AgeRange': 20.0, 'Gender': 'Female', 'Emotions': 'Negtive'}

    res = dict()
    res['faceDetail'] = ar
    return res


def main(request):
    bucket, file = request["image_file"]
    res = detect_faces(bucket, file)
    return res


if __name__ == "__main__":
    res = main({"image_file": ('ccsp21spring', '1.jpg')})
    print(res)
