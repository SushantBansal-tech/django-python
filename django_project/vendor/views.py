from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Vendor
from .serializers import VendorSerializer


def get_vendor_or_404(pk):
    try:
        return Vendor.objects.get(pk=pk)
    except Vendor.DoesNotExist:
        return None


class VendorListCreateView(APIView):
    """
    List all vendors or create a new vendor.
    """

    @swagger_auto_schema(
        operation_summary="List all vendors",
        operation_description="Returns a list of all vendors. Filter by is_active status.",
        manual_parameters=[
            openapi.Parameter('is_active', openapi.IN_QUERY, description="Filter by active status (true/false)", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search by name or code", type=openapi.TYPE_STRING),
        ],
        responses={200: VendorSerializer(many=True)},
        tags=['Vendors'],
    )
    def get(self, request):
        queryset = Vendor.objects.all()

        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(code__icontains=search)

        serializer = VendorSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a vendor",
        operation_description="Create a new vendor. Code must be unique.",
        request_body=VendorSerializer,
        responses={
            201: VendorSerializer,
            400: openapi.Response('Validation error'),
        },
        tags=['Vendors'],
    )
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorDetailView(APIView):
    """
    Retrieve, update or delete a vendor by ID.
    """

    @swagger_auto_schema(
        operation_summary="Retrieve a vendor",
        responses={
            200: VendorSerializer,
            404: openapi.Response('Vendor not found'),
        },
        tags=['Vendors'],
    )
    def get(self, request, pk):
        vendor = get_vendor_or_404(pk)
        if vendor is None:
            return Response({'detail': 'Vendor not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a vendor (full)",
        request_body=VendorSerializer,
        responses={
            200: VendorSerializer,
            400: openapi.Response('Validation error'),
            404: openapi.Response('Vendor not found'),
        },
        tags=['Vendors'],
    )
    def put(self, request, pk):
        vendor = get_vendor_or_404(pk)
        if vendor is None:
            return Response({'detail': 'Vendor not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Partial update a vendor",
        request_body=VendorSerializer,
        responses={
            200: VendorSerializer,
            400: openapi.Response('Validation error'),
            404: openapi.Response('Vendor not found'),
        },
        tags=['Vendors'],
    )
    def patch(self, request, pk):
        vendor = get_vendor_or_404(pk)
        if vendor is None:
            return Response({'detail': 'Vendor not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a vendor",
        responses={
            204: openapi.Response('Vendor deleted'),
            404: openapi.Response('Vendor not found'),
        },
        tags=['Vendors'],
    )
    def delete(self, request, pk):
        vendor = get_vendor_or_404(pk)
        if vendor is None:
            return Response({'detail': 'Vendor not found.'}, status=status.HTTP_404_NOT_FOUND)
        vendor.delete()
        return Response({'detail': 'Vendor deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
