from __future__ import annotations

from typing import Dict, List

from django.db import models


class MenuItemManager(models.Manager):
    def get_tree(self, menu_name: str) -> List[Dict]:
        pass
