from django.db import models
from vendor.models import Vendor
from product.models import Product


class VendorProductMapping(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendorproductmapping')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='vendorproductmapping')
    primary_mapping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'vendor_product_mapping'
        unique_together = [('vendor', 'product')]

    def __str__(self):
        return f"Vendor({self.vendor_id}) → Product({self.product_id})"
