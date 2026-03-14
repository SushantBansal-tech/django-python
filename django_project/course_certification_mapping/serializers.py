from rest_framework import serializers
from .models import CourseCertificationMapping
from course.models import Course
from certification.models import Certification


class CourseCertificationMappingSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField(read_only=True)
    certification_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CourseCertificationMapping
        fields = [
            'id', 'course', 'course_name', 'certification', 'certification_name',
            'primary_mapping', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_course_name(self, obj):
        return obj.course.name if obj.course_id else None

    def get_certification_name(self, obj):
        return obj.certification.name if obj.certification_id else None

    def validate_course(self, value):
        if not Course.objects.filter(pk=value.pk, is_active=True).exists():
            raise serializers.ValidationError("Course does not exist or is inactive.")
        return value

    def validate_certification(self, value):
        if not Certification.objects.filter(pk=value.pk, is_active=True).exists():
            raise serializers.ValidationError("Certification does not exist or is inactive.")
        return value

    def validate(self, attrs):
        instance = self.instance
        course = attrs.get('course', instance.course if instance else None)
        certification = attrs.get('certification', instance.certification if instance else None)
        primary_mapping = attrs.get('primary_mapping', instance.primary_mapping if instance else False)

        if course and certification:
            qs = CourseCertificationMapping.objects.filter(course=course, certification=certification)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {'non_field_errors': f"A mapping between Course({course.id}) and Certification({certification.id}) already exists."}
                )

        if primary_mapping and course:
            qs = CourseCertificationMapping.objects.filter(course=course, primary_mapping=True)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {'primary_mapping': f"Course({course.id}) already has a primary certification mapping. Only one primary mapping is allowed per course."}
                )

        return attrs
