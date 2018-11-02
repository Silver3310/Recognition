from rest_framework.response import Response
from rest_framework import viewsets

from imageai.Detection import ObjectDetection
import os

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

            detector = ObjectDetection()
            detector.setModelTypeAsRetinaNet()
            detector.setModelPath(
                os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
            detector.loadModel()
            detections = detector.detectObjectsFromImage(
                input_image=request.data['picture'],
                output_image_path=os.path.join(execution_path, "imagenew.jpg"))

            response_data = ''

            for eachObject in detections:
                response_data += str(eachObject["name"]) + ' '

            return Response(response_data)
        print(serializer.errors)
        return Response(serializer.errors)
