from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import CourseCertificationMapping
from .serializers import CourseCertificationMappingSerializer


def get_mapping_or_404(pk):
    try:
        return CourseCertificationMapping.objects.get(pk=pk)
    except CourseCertificationMapping.DoesNotExist:
        return None


class CourseCertificationMappingListCreateView(APIView):
    """
    List all course-certification mappings or create a new one.
    """

    @swagger_auto_schema(
        operation_summary="List all course-certification mappings",
        manual_parameters=[
            openapi.Parameter('course_id', openapi.IN_QUERY, description="Filter by course ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('certification_id', openapi.IN_QUERY, description="Filter by certification ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('is_active', openapi.IN_QUERY, description="Filter by active status", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('primary_mapping', openapi.IN_QUERY, description="Filter by primary_mapping flag", type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: CourseCertificationMappingSerializer(many=True)},
        tags=['Course-Certification Mappings'],
    )
    def get(self, request):
        queryset = CourseCertificationMapping.objects.select_related('course', 'certification').all()

        course_id = request.query_params.get('course_id')
        if course_id:
            try:
                queryset = queryset.filter(course_id=int(course_id))
            except (ValueError, TypeError):
                return Response({'detail': 'course_id must be a valid integer.'}, status=status.HTTP_400_BAD_REQUEST)

        certification_id = request.query_params.get('certification_id')
        if certification_id:
            try:
                queryset = queryset.filter(certification_id=int(certification_id))
            except (ValueError, TypeError):
                return Response({'detail': 'certification_id must be a valid integer.'}, status=status.HTTP_400_BAD_REQUEST)

        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        primary_mapping = request.query_params.get('primary_mapping')
        if primary_mapping is not None:
            queryset = queryset.filter(primary_mapping=primary_mapping.lower() == 'true')

        serializer = CourseCertificationMappingSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a course-certification mapping",
        operation_description=(
            "Create a new Course→Certification mapping.\n\n"
            "**Validation rules:**\n"
            "- The same course-certification pair cannot be mapped twice.\n"
            "- Only one mapping per course can have `primary_mapping=true`."
        ),
        request_body=CourseCertificationMappingSerializer,
        responses={
            201: CourseCertificationMappingSerializer,
            400: openapi.Response('Validation error'),
        },
        tags=['Course-Certification Mappings'],
    )
    def post(self, request):
        serializer = CourseCertificationMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseCertificationMappingDetailView(APIView):
    """
    Retrieve, update or delete a course-certification mapping by ID.
    """

    @swagger_auto_schema(
        operation_summary="Retrieve a course-certification mapping",
        responses={200: CourseCertificationMappingSerializer, 404: openapi.Response('Mapping not found')},
        tags=['Course-Certification Mappings'],
    )
    def get(self, request, pk):
        mapping = get_mapping_or_404(pk)
        if mapping is None:
            return Response({'detail': 'Course-Certification mapping not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseCertificationMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a course-certification mapping (full)",
        request_body=CourseCertificationMappingSerializer,
        responses={200: CourseCertificationMappingSerializer, 400: openapi.Response('Validation error'), 404: openapi.Response('Mapping not found')},
        tags=['Course-Certification Mappings'],
    )
    def put(self, request, pk):
        mapping = get_mapping_or_404(pk)
        if mapping is None:
            return Response({'detail': 'Course-Certification mapping not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Partial update a course-certification mapping",
        request_body=CourseCertificationMappingSerializer,
        responses={200: CourseCertificationMappingSerializer, 400: openapi.Response('Validation error'), 404: openapi.Response('Mapping not found')},
        tags=['Course-Certification Mappings'],
    )
    def patch(self, request, pk):
        mapping = get_mapping_or_404(pk)
        if mapping is None:
            return Response({'detail': 'Course-Certification mapping not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a course-certification mapping",
        responses={204: openapi.Response('Mapping deleted'), 404: openapi.Response('Mapping not found')},
        tags=['Course-Certification Mappings'],
    )
    def delete(self, request, pk):
        mapping = get_mapping_or_404(pk)
        if mapping is None:
            return Response({'detail': 'Course-Certification mapping not found.'}, status=status.HTTP_404_NOT_FOUND)
        mapping.delete()
        return Response({'detail': 'Mapping deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
