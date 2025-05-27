from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import  MinValueValidator


class Category(models.Model):
    title = models.CharField(_("title"), max_length=100)
    description = models.CharField(_("description"), max_length=250, blank=True)

    class Meta:
        ordering = ["title"]
        verbose_name = _("category")  
        verbose_name_plural = _("category")

    def __str__(self):
        return self.title


class Mobile(models.Model):
    name = models.CharField(_("name"), max_length=100)
    category = models.ForeignKey(Category, verbose_name=_("category"), on_delete=models.SET_NULL,related_name='products', blank=True, null=True )
    short_description = models.TextField(_("short description"), max_length=250)
    description = models.TextField(_("description for mobile"))
    inventory = models.IntegerField(_("inventory"), validators=[MinValueValidator(1)])
    price_main = models.PositiveIntegerField(_("price"))
    price_with_discount = models.PositiveIntegerField(_("price with discount"), blank=True, null=True)
    image = models.ImageField(_("image"), upload_to='cover/',)
    is_active = models.BooleanField(_("active?"))
    date_time_added = models.DateTimeField(_("date time added"), auto_now_add=True)

    class Meta:
        ordering = ["-date_time_added"]
        verbose_name = _("mobile")  
        verbose_name_plural = _("mobile")

    def __str__(self):
        return self.name
    
    def percent_discount(self):
        if self.price_with_discount:
            return (self.price_main - self.price_with_discount) / self.price_main * 100
        return 0

    

    