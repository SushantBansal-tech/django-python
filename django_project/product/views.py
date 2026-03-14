from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Product
from .serializers import ProductSerializer


def get_product_or_404(pk):
    try:
        return Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return None


class ProductListCreateView(APIView):
    """
    List all products or create a new product.
    """

    @swagger_auto_schema(
        operation_summary="List all products",
        operation_description="Returns a list of all products. Supports filtering by vendor_id (via mapping) and is_active.",
        manual_parameters=[
            openapi.Parameter('is_active', openapi.IN_QUERY, description="Filter by active status", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('vendor_id', openapi.IN_QUERY, description="Filter products mapped to a specific vendor", type=openapi.TYPE_INTEGER),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search by name or code", type=openapi.TYPE_STRING),
        ],
        responses={200: ProductSerializer(many=True)},
        tags=['Products'],
    )
    def get(self, request):
        queryset = Product.objects.all()

        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        vendor_id = request.query_params.get('vendor_id')
        if vendor_id:
            try:
                vendor_id = int(vendor_id)
                queryset = queryset.filter(
                    vendorproductmapping__vendor_id=vendor_id,
                    vendorproductmapping__is_active=True
                ).distinct()
            except (ValueError, TypeError):
                return Response({'detail': 'vendor_id must be a valid integer.'}, status=status.HTTP_400_BAD_REQUEST)

        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(code__icontains=search)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a product",
        request_body=ProductSerializer,
        responses={
            201: ProductSerializer,
            400: openapi.Response('Validation error'),
        },
        tags=['Products'],
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    """
    Retrieve, update or delete a product by ID.
    """

    @swagger_auto_schema(
        operation_summary="Retrieve a product",
        responses={200: ProductSerializer, 404: openapi.Response('Product not found')},
        tags=['Products'],
    )
    def get(self, request, pk):
        product = get_product_or_404(pk)
        if product is None:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a product (full)",
        request_body=ProductSerializer,
        responses={200: ProductSerializer, 400: openapi.Response('Validation error'), 404: openapi.Response('Product not found')},
        tags=['Products'],
    )
    def put(self, request, pk):
        product = get_product_or_404(pk)
        if product is None:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Partial update a product",
        request_body=ProductSerializer,
        responses={200: ProductSerializer, 400: openapi.Response('Validation error'), 404: openapi.Response('Product not found')},
        tags=['Products'],
    )
    def patch(self, request, pk):
        product = get_product_or_404(pk)
        if product is None:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a product",
        responses={204: openapi.Response('Product deleted'), 404: openapi.Response('Product not found')},
        tags=['Products'],
    )
    def delete(self, request, pk):
        product = get_product_or_404(pk)
        if product is None:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response({'detail': 'Product deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
