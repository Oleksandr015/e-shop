from django.db import models


class CategoryFeature(models.Model):
    """
    Charakterystyka określonej kategorii
    """
    category = models.ForeignKey('mainapp.Category', verbose_name='Categoria', on_delete=models.CASCADE)
    feature_name = models.CharField(max_length=100, verbose_name='Nazwa charakterystyki')
    feature_filter_name = models.CharField(max_length=50, verbose_name='Nazwa filtra')
    unit = models.CharField(max_length=50, verbose_name='Jednostka', null=True, blank=True)

    class Meta:
        unique_together = ('category', 'feature_name', 'feature_filter_name')

    def __str__(self):
        return f'{self.category.name} | {self.feature_name}'


class FeatureValidator(models.Model):
    """
    Walidator wartości charakterystycznych należący do określonej kategorii.
    """
    category = models.ForeignKey('mainapp.Category', verbose_name='Kategoria', on_delete=models.CASCADE)
    feature_key = models.ForeignKey(CategoryFeature, verbose_name='Klucz charakterystyki', on_delete=models.CASCADE)
    valid_feature_value = models.CharField(max_length=100, verbose_name='Ważna wartość')

    def __str__(self):
        return f'Kategoria \"{self.category.name}\' | ' \
               f'Charakterystyka \"{self.feature_key.feature_name}" | ' \
               f'Ważna wartość \"{self.valid_feature_value}"'


class ProductFeatures(models.Model):
    """
    Szczegóły produktu.
    """

    product = models.ForeignKey('mainapp.Product', verbose_name='Product', on_delete=models.CASCADE)
    feature = models.ForeignKey(CategoryFeature, verbose_name='Charakterystyka', on_delete=models.CASCADE)
    value = models.CharField(max_length=255, verbose_name='Wartość')

    def __str__(self):
        return f'Product - \"{self.product.title} | ' \
               f'Charakterystyka - \"{self.feature.feature_name}" | ' \
               f'Wartość - {self.value}'
