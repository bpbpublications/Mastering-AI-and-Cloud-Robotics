import boto3


def detect_objects(img_bytes):
    # Detect object using Rekognition
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_labels(Image={'Bytes': img_bytes})
    return response['Labels']


if __name__ == '__main__':
    # Read image from file
    with open('cat.jpg', 'rb') as f:
        img = f.read()
        objects_detected = detect_objects(img)
        print("Detected Objects:", objects_detected)