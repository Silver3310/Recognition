from rest_framework.response import Response
from rest_framework import viewsets

import os
import cv2 # OpenCV
import numpy as np # linear algebra
from tensorflow import keras
import requests
import json


from recognition.api.serializers import RequestSerializer

from recognition.models import Request


class RequestViewSet(viewsets.GenericViewSet):
    """Mixin for requests"""

    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def create(self, request):

        execution_path = os.getcwd()

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            # final result
            detections = []
            # Import multiple-test dataset
            test_fruits_img = []
            img = cv2.imdecode(np.fromstring(request.data['picture'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
            # img = cv2.imread(img_path)
            headers = {
                'Prediction-Key': '440ecae398694b92bdf7d9549c0a6aa0',
                'Content-Type': 'application/octet-stream',
            }
            data = request.data['picture']
            r = requests.post(
                url="https://southcentralus.api.cognitive.microsoft.com/customvision/v2.0/Prediction/788fa507-53bd-4bce-a0f3-3ab9bd0a26df/image?iterationId=9018e048-6361-4e42-a7c4-7ae0ced92daf",
                headers=headers, data=data)
            r = json.loads(r.text)
            for each_prediction in r['predictions']:
                if each_prediction['probability'] > 0.4:
                    crop_img = img[int(
                        img.shape[0] * each_prediction['boundingBox']['top']):
                                   int(img.shape[0] *
                                       each_prediction['boundingBox']['top'])
                                   + int(img.shape[0] *
                                         each_prediction['boundingBox'][
                                             'height']),
                               int(img.shape[1] *
                                   each_prediction['boundingBox']['left']):
                               int(img.shape[1] *
                                   each_prediction['boundingBox']['left']) +
                               int(img.shape[1] *
                                   each_prediction['boundingBox']['width'])]
                    crop_img = cv2.resize(crop_img, (64, 64))
                    crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
                    test_fruits_img.append(crop_img)
                    detections.append({
                        'percentage_probability': each_prediction['probability'],
                        'box_points':[
                            int(img.shape[1]*each_prediction['boundingBox']['left']),
                            int(img.shape[0]*each_prediction['boundingBox']['top']),
                            int(img.shape[1]*each_prediction['boundingBox']['left']) +
                            int(img.shape[1]*each_prediction['boundingBox']['width']),
                            int(img.shape[0]*each_prediction['boundingBox']['top']) +
                            int(img.shape[0]*each_prediction['boundingBox']['height'])]}
                    )
            test_fruits_img = np.array(test_fruits_img)

            model = keras.models.load_model('model6.h5')

            id_to_label = np.load('model_labels.npy').tolist()

            predictions = model.predict(test_fruits_img)

            keras.backend.clear_session()

            for i in range(len(test_fruits_img)):
                detections[i]['name'] = id_to_label[np.argmax(predictions[i])]

            return Response(detections)
        print(serializer.errors)
        return Response(serializer.errors)



