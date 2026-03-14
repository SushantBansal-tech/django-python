from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Course
from .serializers import CourseSerializer


def get_course_or_404(pk):
    try:
        return Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return None


class CourseListCreateView(APIView):
    """
    List all courses or create a new course.
    """

    @swagger_auto_schema(
        operation_summary="List all courses",
        operation_description="Returns a list of all courses. Supports filtering by product_id (via mapping) and is_active.",
        manual_parameters=[
            openapi.Parameter('is_active', openapi.IN_QUERY, description="Filter by active status", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('product_id', openapi.IN_QUERY, description="Filter courses mapped to a specific product", type=openapi.TYPE_INTEGER),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search by name or code", type=openapi.TYPE_STRING),
        ],
        responses={200: CourseSerializer(many=True)},
        tags=['Courses'],
    )
    def get(self, request):
        queryset = Course.objects.all()

        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        product_id = request.query_params.get('product_id')
        if product_id:
            try:
                product_id = int(product_id)
                queryset = queryset.filter(
                    productcoursemapping__product_id=product_id,
                    productcoursemapping__is_active=True
                ).distinct()
            except (ValueError, TypeError):
                return Response({'detail': 'product_id must be a valid integer.'}, status=status.HTTP_400_BAD_REQUEST)

        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(code__icontains=search)

        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a course",
        request_body=CourseSerializer,
        responses={
            201: CourseSerializer,
            400: openapi.Response('Validation error'),
        },
        tags=['Courses'],
    )
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    """
    Retrieve, update or delete a course by ID.
    """

    @swagger_auto_schema(
        operation_summary="Retrieve a course",
        responses={200: CourseSerializer, 404: openapi.Response('Course not found')},
        tags=['Courses'],
    )
    def get(self, request, pk):
        course = get_course_or_404(pk)
        if course is None:
            return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a course (full)",
        request_body=CourseSerializer,
        responses={200: CourseSerializer, 400: openapi.Response('Validation error'), 404: openapi.Response('Course not found')},
        tags=['Courses'],
    )
    def put(self, request, pk):
        course = get_course_or_404(pk)
        if course is None:
            return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Partial update a course",
        request_body=CourseSerializer,
        responses={200: CourseSerializer, 400: openapi.Response('Validation error'), 404: openapi.Response('Course not found')},
        tags=['Courses'],
    )
    def patch(self, request, pk):
        course = get_course_or_404(pk)
        if course is None:
            return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a course",
        responses={204: openapi.Response('Course deleted'), 404: openapi.Response('Course not found')},
        tags=['Courses'],
    )
    def delete(self, request, pk):
        course = get_course_or_404(pk)
        if course is None:
            return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
        course.delete()
        return Response({'detail': 'Course deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
