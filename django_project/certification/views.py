from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Certification
from .serializers import CertificationSerializer


def get_certification_or_404(pk):
    try:
        return Certification.objects.get(pk=pk)
    except Certification.DoesNotExist:
        return None


class CertificationListCreateView(APIView):
    """
    List all certifications or create a new certification.
    """

    @swagger_auto_schema(
        operation_summary="List all certifications",
        operation_description="Returns a list of all certifications. Supports filtering by course_id (via mapping) and is_active.",
        manual_parameters=[
            openapi.Parameter('is_active', openapi.IN_QUERY, description="Filter by active status", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('course_id', openapi.IN_QUERY, description="Filter certifications mapped to a specific course", type=openapi.TYPE_INTEGER),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search by name or code", type=openapi.TYPE_STRING),
        ],
        responses={200: CertificationSerializer(many=True)},
        tags=['Certifications'],
    )
    def get(self, request):
        queryset = Certification.objects.all()

        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        course_id = request.query_params.get('course_id')
        if course_id:
            try:
                course_id = int(course_id)
                queryset = queryset.filter(
                    coursecertificationmapping__course_id=course_id,
                    coursecertificationmapping__is_active=True
                ).distinct()
            except (ValueError, TypeError):
                return Response({'detail': 'course_id must be a valid integer.'}, status=status.HTTP_400_BAD_REQUEST)

        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(code__icontains=search)

        serializer = CertificationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a certification",
        request_body=CertificationSerializer,
        responses={
            201: CertificationSerializer,
            400: openapi.Response('Validation error'),
        },
        tags=['Certifications'],
    )
    def post(self, request):
        serializer = CertificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CertificationDetailView(APIView):
    """
    Retrieve, update or delete a certification by ID.
    """

    @swagger_auto_schema(
        operation_summary="Retrieve a certification",
        responses={200: CertificationSerializer, 404: openapi.Response('Certification not found')},
        tags=['Certifications'],
    )
    def get(self, request, pk):
        certification = get_certification_or_404(pk)
        if certification is None:
            return Response({'detail': 'Certification not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CertificationSerializer(certification)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a certification (full)",
        request_body=CertificationSerializer,
        responses={200: CertificationSerializer, 400: openapi.Response('Validation error'), 404: openapi.Response('Certification not found')},
        tags=['Certifications'],
    )
    def put(self, request, pk):
        certification = get_certification_or_404(pk)
        if certification is None:
            return Response({'detail': 'Certification not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CertificationSerializer(certification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Partial update a certification",
        request_body=CertificationSerializer,
        responses={200: CertificationSerializer, 400: openapi.Response('Validation error'), 404: openapi.Response('Certification not found')},
        tags=['Certifications'],
    )
    def patch(self, request, pk):
        certification = get_certification_or_404(pk)
        if certification is None:
            return Response({'detail': 'Certification not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CertificationSerializer(certification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a certification",
        responses={204: openapi.Response('Certification deleted'), 404: openapi.Response('Certification not found')},
        tags=['Certifications'],
    )
    def delete(self, request, pk):
        certification = get_certification_or_404(pk)
        if certification is None:
            return Response({'detail': 'Certification not found.'}, status=status.HTTP_404_NOT_FOUND)
        certification.delete()
        return Response({'detail': 'Certification deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
