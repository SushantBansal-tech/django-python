from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import ProductCourseMapping
from .serializers import ProductCourseMappingSerializer


def get_mapping_or_404(pk):
    try:
        return ProductCourseMapping.objects.get(pk=pk)
    except ProductCourseMapping.DoesNotExist:
        return None


class ProductCourseMappingListCreateView(APIView):
    """
    List all product-course mappings or create a new one.
    """

    @swagger_auto_schema(
        operation_summary="List all product-course mappings",
        manual_parameters=[
            openapi.Parameter('product_id', openapi.IN_QUERY, description="Filter by product ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('course_id', openapi.IN_QUERY, description="Filter by course ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('is_active', openapi.IN_QUERY, description="Filter by active status", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('primary_mapping', openapi.IN_QUERY, description="Filter by primary_mapping flag", type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: ProductCourseMappingSerializer(many=True)},
        tags=['Product-Course Mappings'],
    )
    def get(self, request):
        queryset = ProductCourseMapping.objects.select_related('product', 'course').all()

        product_id = request.query_params.get('product_id')
        if product_id:
            try:
                queryset = queryset.filter(product_id=int(product_id))
            except (ValueError, TypeError):
                return Response({'detail': 'product_id must be a valid integer.'}, status=status.HTTP_400_BAD_REQUEST)

        course_id = request.query_params.get('course_id')
        if course_id:
            try:
                queryset = queryset.filter(course_id=int(course_id))
            except (ValueError, TypeError):
                return Response({'detail': 'course_id must be a valid integer.'}, status=status.HTTP_400_BAD_REQUEST)

        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        primary_mapping = request.query_params.get('primary_mapping')
        if primary_mapping is not None:
            queryset = queryset.filter(primary_mapping=primary_mapping.lower() == 'true')

        serializer = ProductCourseMappingSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a product-course mapping",
        operation_description=(
            "Create a new Product→Course mapping.\n\n"
            "**Validation rules:**\n"
            "- The same product-course pair cannot be mapped twice.\n"
            "- Only one mapping per product can have `primary_mapping=true`."
        ),
        request_body=ProductCourseMappingSerializer,
        responses={
            201: ProductCourseMappingSerializer,
            400: openapi.Response('Validation error'),
        },
        tags=['Product-Course Mappings'],
    )
    def post(self, request):
        serializer = ProductCourseMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCourseMappingDetailView(APIView):
    """
    Retrieve, update or delete a product-course mapping by ID.
    """

    @swagger_auto_schema(
        operation_summary="Retrieve a product-course mapping",
        responses={200: ProductCourseMappingSerializer, 404: openapi.Response('Mapping not found')},
        tags=['Product-Course Mappings'],
    )
    def get(self, request, pk):
        mapping = get_mapping_or_404(pk)
        if mapping is None:
            return Response({'detail': 'Product-Course mapping not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductCourseMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a product-course mapping (full)",
        request_body=ProductCourseMappingSerializer,
        responses={200: ProductCourseMappingSerializer, 400: openapi.Response('Validation error'), 404: openapi.Response('Mapping not found')},
        tags=['Product-Course Mappings'],
    )
    def put(self, request, pk):
        mapping = get_mapping_or_404(pk)
        if mapping is None:
            return Response({'detail': 'Product-Course mapping not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductCourseMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Partial update a product-course mapping",
        request_body=ProductCourseMappingSerializer,
        responses={200: ProductCourseMappingSerializer, 400: openapi.Response('Validation error'), 404: openapi.Response('Mapping not found')},
        tags=['Product-Course Mappings'],
    )
    def patch(self, request, pk):
        mapping = get_mapping_or_404(pk)
        if mapping is None:
            return Response({'detail': 'Product-Course mapping not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductCourseMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a product-course mapping",
        responses={204: openapi.Response('Mapping deleted'), 404: openapi.Response('Mapping not found')},
        tags=['Product-Course Mappings'],
    )
    def delete(self, request, pk):
        mapping = get_mapping_or_404(pk)
        if mapping is None:
            return Response({'detail': 'Product-Course mapping not found.'}, status=status.HTTP_404_NOT_FOUND)
        mapping.delete()
        return Response({'detail': 'Mapping deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
