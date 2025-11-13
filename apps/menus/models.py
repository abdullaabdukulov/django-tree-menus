from django.db import models
from django.urls import NoReverseMatch, reverse

from apps.common.models import BaseModel

from .managers import MenuItemManager


class MenuItem(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Name")
    url = models.CharField(max_length=255, verbose_name="URL or Named URL")
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
        verbose_name="Parent",
    )
    menu_name = models.CharField(max_length=255, verbose_name="Menu Name")
    order = models.PositiveIntegerField(default=0, verbose_name="Order")

    objects = MenuItemManager()

    class Meta:
        ordering = ["menu_name", "order"]
        unique_together = ["menu_name", "parent", "name"]
        indexes = [
            models.Index(fields=["menu_name"]),
            models.Index(fields=["parent"]),
        ]

    def __str__(self) -> str:
        return f"{self.menu_name}:{self.name}"

    def get_absolute_url(self) -> str:
        try:
            return reverse(self.url)
        except NoReverseMatch:
            return self.url
