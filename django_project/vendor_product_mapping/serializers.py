from rest_framework import serializers
from .models import VendorProductMapping
from vendor.models import Vendor
from product.models import Product


class VendorProductMappingSerializer(serializers.ModelSerializer):
    vendor_name = serializers.SerializerMethodField(read_only=True)
    product_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = VendorProductMapping
        fields = [
            'id', 'vendor', 'vendor_name', 'product', 'product_name',
            'primary_mapping', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_vendor_name(self, obj):
        return obj.vendor.name if obj.vendor_id else None

    def get_product_name(self, obj):
        return obj.product.name if obj.product_id else None

    def validate_vendor(self, value):
        if not Vendor.objects.filter(pk=value.pk, is_active=True).exists():
            raise serializers.ValidationError("Vendor does not exist or is inactive.")
        return value

    def validate_product(self, value):
        if not Product.objects.filter(pk=value.pk, is_active=True).exists():
            raise serializers.ValidationError("Product does not exist or is inactive.")
        return value

    def validate(self, attrs):
        instance = self.instance
        vendor = attrs.get('vendor', instance.vendor if instance else None)
        product = attrs.get('product', instance.product if instance else None)
        primary_mapping = attrs.get('primary_mapping', instance.primary_mapping if instance else False)

        if vendor and product:
            qs = VendorProductMapping.objects.filter(vendor=vendor, product=product)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {'non_field_errors': f"A mapping between Vendor({vendor.id}) and Product({product.id}) already exists."}
                )

        if primary_mapping and vendor:
            qs = VendorProductMapping.objects.filter(vendor=vendor, primary_mapping=True)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {'primary_mapping': f"Vendor({vendor.id}) already has a primary product mapping. Only one primary mapping is allowed per vendor."}
                )

        return attrs
