from django.db import models
from django.urls import NoReverseMatch, reverse
from menus.managers import MenuManager


class Menu(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name="Название меню"
    )

    objects = MenuManager()

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Меню",
    )
    title = models.CharField(max_length=100, verbose_name="Название")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Родительский пункт",
    )
    url = models.CharField(max_length=200, blank=True, verbose_name="URL")
    named_url = models.CharField(
        max_length=100, blank=True, verbose_name="Named URL"
    )
    order = models.IntegerField(default=0, verbose_name="Порядок сортировки")

    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    def get_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return "#"
        return self.url or "#"

    def should_show_children(self, parent_is_active=False):
        if not hasattr(self, "_is_in_path"):
            return False
        return self._is_in_path or parent_is_active

    def get_css_classes(self):
        classes = []
        if hasattr(self, "_is_active") and self._is_active:
            classes.append("active")
        if hasattr(self, "_has_children") and self._has_children:
            classes.append("has-children")
            if hasattr(self, "_is_in_path") and self._is_in_path:
                classes.append("expanded")
        return " ".join(classes)
