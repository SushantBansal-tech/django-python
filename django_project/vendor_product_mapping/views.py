from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import VendorProductMapping
from .serializers import VendorProductMappingSerializer


def get_mapping_or_404(pk):
    try:
        return VendorProductMapping.objects.get(pk=pk)
    except VendorProductMapping.DoesNotExist:
        return None


class VendorProductMappingListCreateView(APIView):
    """
    List all vendor-product mappings or create a new one.
    """

    @swagger_auto_schema(
        operation_summary="List all vendor-product mappings",
        manual_parameters=[
            openapi.Parameter('vendor_id', openapi.IN_QUERY, description="Filter by vendor ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('product_id', openapi.IN_QUERY, description="Filter by product ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('is_active', openapi.IN_QUERY, description="Filter by active status", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('primary_mapping', openapi.IN_QUERY, description="Filter by primary_mapping flag", type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: VendorProductMappingSerializer(many=True)},
        tags=['Vendor-Product Mappings'],
    )
    def get(self, request):
        queryset = VendorProductMapping.objects.select_related('vendor', 'product').all()

        vendor_id = request.query_params.get('vendor_id')
        if vendor_id:
            try:
                queryset = queryset.filter(vendor_id=int(vendor_id))
            except (ValueError, TypeError):
                return Response({'detail': 'vendor_id must be a valid integer.'}, status=status.HTTP_400_BAD_REQUEST)

        product_id = request.query_params.get('product_id')
        if product_id:
            try:
                queryset = queryset.filter(product_id=int(product_id))
            except (ValueError, TypeError):
                return Response({'detail': 'product_id must be a valid integer.'}, status=status.HTTP_400_BAD_REQUEST)

        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        primary_mapping = request.query_params.get('primary_mapping')
        if primary_mapping is not None:
            queryset = queryset.filter(primary_mapping=primary_mapping.lower() == 'true')

        serializer = VendorProductMappingSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a vendor-product mapping",
        operation_description=(
            "Create a new Vendor→Product mapping.\n\n"
            "**Validation rules:**\n"
            "- The same vendor-product pair cannot be mapped twice.\n"
            "- Only one mapping per vendor can have `primary_mapping=true`."
        ),
        request_body=VendorProductMappingSerializer,
        responses={
            201: VendorProductMappingSerializer,
            400: openapi.Response('Validation error'),
        },
        tags=['Vendor-Product Mappings'],
    )
    def post(self, request):
        serializer = VendorProductMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorProductMappingDetailView(APIView):
    """
    Retrieve, update or delete a vendor-product mapping by ID.
    """

    @swagger_auto_schema(
        operation_summary="Retrieve a vendor-product mapping",
        responses={200: VendorProductMappingSerializer, 404: openapi.Response('Mapping not found')},
        tags=['Vendor-Product Mappings'],
    )
    def get(self, request, pk):
        mapping = get_mapping_or_404(pk)
        if mapping is None:
            return Response({'detail': 'Vendor-Product mapping not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = VendorProductMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a vendor-product mapping (full)",
        request_body=VendorProductMappingSerializer,
        responses={200: VendorProductMappingSerializer, 400: openapi.Response('Validation error'), 404: openapi.Response('Mapping not found')},
        tags=['Vendor-Product Mappings'],
    )
    def put(self, request, pk):
        mapping = get_mapping_or_404(pk)
        if mapping is None:
            return Response({'detail': 'Vendor-Product mapping not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = VendorProductMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Partial update a vendor-product mapping",
        request_body=VendorProductMappingSerializer,
        responses={200: VendorProductMappingSerializer, 400: openapi.Response('Validation error'), 404: openapi.Response('Mapping not found')},
        tags=['Vendor-Product Mappings'],
    )
    def patch(self, request, pk):
        mapping = get_mapping_or_404(pk)
        if mapping is None:
            return Response({'detail': 'Vendor-Product mapping not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = VendorProductMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a vendor-product mapping",
        responses={204: openapi.Response('Mapping deleted'), 404: openapi.Response('Mapping not found')},
        tags=['Vendor-Product Mappings'],
    )
    def delete(self, request, pk):
        mapping = get_mapping_or_404(pk)
        if mapping is None:
            return Response({'detail': 'Vendor-Product mapping not found.'}, status=status.HTTP_404_NOT_FOUND)
        mapping.delete()
        return Response({'detail': 'Mapping deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
