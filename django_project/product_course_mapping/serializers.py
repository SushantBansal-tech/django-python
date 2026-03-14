from rest_framework import serializers
from .models import ProductCourseMapping
from product.models import Product
from course.models import Course


class ProductCourseMappingSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField(read_only=True)
    course_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductCourseMapping
        fields = [
            'id', 'product', 'product_name', 'course', 'course_name',
            'primary_mapping', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_product_name(self, obj):
        return obj.product.name if obj.product_id else None

    def get_course_name(self, obj):
        return obj.course.name if obj.course_id else None

    def validate_product(self, value):
        if not Product.objects.filter(pk=value.pk, is_active=True).exists():
            raise serializers.ValidationError("Product does not exist or is inactive.")
        return value

    def validate_course(self, value):
        if not Course.objects.filter(pk=value.pk, is_active=True).exists():
            raise serializers.ValidationError("Course does not exist or is inactive.")
        return value

    def validate(self, attrs):
        instance = self.instance
        product = attrs.get('product', instance.product if instance else None)
        course = attrs.get('course', instance.course if instance else None)
        primary_mapping = attrs.get('primary_mapping', instance.primary_mapping if instance else False)

        if product and course:
            qs = ProductCourseMapping.objects.filter(product=product, course=course)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {'non_field_errors': f"A mapping between Product({product.id}) and Course({course.id}) already exists."}
                )

        if primary_mapping and product:
            qs = ProductCourseMapping.objects.filter(product=product, primary_mapping=True)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {'primary_mapping': f"Product({product.id}) already has a primary course mapping. Only one primary mapping is allowed per product."}
                )

        return attrs
