from django.db import models


class MenuQuerySet(models.QuerySet):
    def with_items(self):
        return self.prefetch_related("items")


class MenuManager(models.Manager):
    def get_queryset(self):
        return MenuQuerySet(self.model, using=self._db)

    def with_items(self):
        return self.get_queryset().with_items()

    def get_menu_tree(self, menu_name, current_url):
        try:
            menu = self.with_items().get(name=menu_name)
        except self.model.DoesNotExist:
            return None

        all_items = list(menu.items.all())
        if not all_items:
            return None

        active_item = next(
            (item for item in all_items if item.get_url() == current_url), None
        )

        active_path = set()
        if active_item:
            current = active_item
            while current:
                active_path.add(current.id)
                current = next(
                    (i for i in all_items if i.id == current.parent_id), None
                )

        items_by_parent = {}
        root_items = []

        for item in all_items:
            if item.parent_id is None:
                root_items.append(item)
            else:
                items_by_parent.setdefault(item.parent_id, []).append(item)

        for item in all_items:
            item._children = items_by_parent.get(item.id, [])
            item._is_active = active_item and item.id == active_item.id
            item._is_in_path = item.id in active_path
            item._has_children = bool(item._children)

        return {
            "root_items": root_items,
            "active_path": active_path,
            "active_item_id": active_item.id if active_item else None,
        }
