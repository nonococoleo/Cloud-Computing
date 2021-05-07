import base64
import boto3
import json


def detect_faces(bucket, photo):
    client = boto3.client('rekognition',
                          region_name='us-east-2',
                          aws_access_key_id='AKIARAQKMHEBYCZBBY5R',
                          aws_secret_access_key='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'
                          )
    response = client.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':photo}},Attributes=['ALL'])
    # print(response)
    ar = [];
    res = dict();
    for faceDetail in response['FaceDetails']:
        tempDict = dict();
        ## getting the age
        tempDict['AgeRange'] = (faceDetail['AgeRange']['Low'] + faceDetail['AgeRange']['High']) /2
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
        ar.append(tempDict);
        # a valid tempDict looks like {'AgeRange': 20.0, 'Gender': 'Female', 'Emotions': 'Negtive'}

    res['faceDetail'] = ar
    return json.dumps(res)


def main(request):
    # image_data = base64.b64decode(request["image_data"])
    # 记得调换对应的参数
    return detect_faces('facebuckt','final.JPG')


if __name__ == "__main__":
    # file = "ident.JPG"
    # with open(file, 'rb') as image:
    #     x1 = image.read()

    # base64_bytes = base64.b64encode(x1)
    # base64_string = base64_bytes.decode('utf-8')

    res = main({"image_data": base64_string})
    print(res)
