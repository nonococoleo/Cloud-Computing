import base64
import boto3
import json


def detect_faces(photo):
    client = boto3.client('rekognition',
                          region_name='us-east-2',
                          aws_access_key_id='AKIARAQKMHEBYCZBBY5R',
                          aws_secret_access_key='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'
                          )
    response = client.detect_faces(Image={'Bytes': photo}, Attributes=['ALL'])
    # print(response)
    return json.dumps(response)
    for faceDetail in response['FaceDetails']:
        print(json.dumps(faceDetail, indent=4, sort_keys=True))
    print(len(response['FaceDetails']))


def main(request):
    image_data = base64.b64decode(request["image_data"])
    return detect_faces(image_data)


if __name__ == "__main__":
    file = "ident.JPG"
    with open(file, 'rb') as image:
        x1 = image.read()

    base64_bytes = base64.b64encode(x1)
    base64_string = base64_bytes.decode('utf-8')

    res = main({"image_data": base64_string})
    print(res)
