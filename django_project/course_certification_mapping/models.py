from django.db import models
from course.models import Course
from certification.models import Certification


class CourseCertificationMapping(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='coursecertificationmapping')
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE, related_name='coursecertificationmapping')
    primary_mapping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'course_certification_mapping'
        unique_together = [('course', 'certification')]

    def __str__(self):
        return f"Course({self.course_id}) → Certification({self.certification_id})"
