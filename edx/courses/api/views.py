from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication


from edx.courses.models import Subject, Course
from .serializers import SubjectSerializer, CourseSerializer


class CourseListView(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['post'], authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True})


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailsView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class CourseEnrollView(APIView):

    authentication_classes = (BasicAuthentication, )
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, format=None):  # pylint-ignore=unused-variables
        course = get_object_or_404(Course, pk=pk)
        if request.user in course.students.all():
            return Response({"Error": "Already enrolled"})
        course.students.add(request.user)
        return Response({
            'enrolled': True
        })
