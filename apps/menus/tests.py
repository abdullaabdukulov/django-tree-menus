from django.template import Context, Template
from django.test import RequestFactory, TestCase

from .models import Menu, MenuItem


class MenuModelTest(TestCase):
    def setUp(self):
        self.menu = Menu.objects.create(name="test_menu")
        self.item1 = MenuItem.objects.create(
            menu=self.menu, title="Home", url="/", order=1
        )
        self.item2 = MenuItem.objects.create(
            menu=self.menu, title="About", url="/about/", order=2
        )
        self.item3 = MenuItem.objects.create(
            menu=self.menu,
            title="Services",
            parent=self.item2,
            url="/about/services/",
            order=1,
        )

    def test_menu_creation(self):
        self.assertEqual(str(self.menu), "test_menu")
        self.assertEqual(self.menu.items.count(), 3)

    def test_menu_item_get_url(self):
        self.assertEqual(self.item1.get_url(), "/")
        self.assertEqual(self.item2.get_url(), "/about/")

    def test_menu_item_named_url(self):
        item = MenuItem.objects.create(
            menu=self.menu, title="Test", named_url="invalid_url"
        )
        self.assertEqual(item.get_url(), "#")

    def test_menu_item_hierarchy(self):
        self.assertIsNone(self.item1.parent)
        self.assertEqual(self.item3.parent, self.item2)


class MenuManagerTest(TestCase):
    def setUp(self):
        self.menu = Menu.objects.create(name="main")
        self.root = MenuItem.objects.create(
            menu=self.menu, title="Root", url="/", order=1
        )
        self.child1 = MenuItem.objects.create(
            menu=self.menu,
            title="Child1",
            url="/child1/",
            parent=self.root,
            order=1,
        )
        self.child2 = MenuItem.objects.create(
            menu=self.menu,
            title="Child2",
            url="/child2/",
            parent=self.root,
            order=2,
        )
        self.grandchild = MenuItem.objects.create(
            menu=self.menu,
            title="Grandchild",
            url="/child1/grandchild/",
            parent=self.child1,
            order=1,
        )

    def test_get_menu_tree_structure(self):
        tree = Menu.objects.get_menu_tree("main", "/child1/")

        self.assertIsNotNone(tree)
        self.assertEqual(len(tree["root_items"]), 1)
        self.assertEqual(tree["root_items"][0].id, self.root.id)

    def test_get_menu_tree_active_path(self):
        tree = Menu.objects.get_menu_tree("main", "/child1/grandchild/")

        self.assertEqual(tree["active_item_id"], self.grandchild.id)
        self.assertIn(self.root.id, tree["active_path"])
        self.assertIn(self.child1.id, tree["active_path"])
        self.assertIn(self.grandchild.id, tree["active_path"])
        self.assertNotIn(self.child2.id, tree["active_path"])

    def test_get_menu_tree_children_metadata(self):
        tree = Menu.objects.get_menu_tree("main", "/child1/")
        root_item = tree["root_items"][0]

        self.assertTrue(root_item._has_children)
        self.assertEqual(len(root_item._children), 2)
        self.assertTrue(root_item._is_in_path)

    def test_get_menu_tree_nonexistent(self):
        tree = Menu.objects.get_menu_tree("nonexistent", "/")
        self.assertIsNone(tree)


class MenuItemMethodsTest(TestCase):
    def setUp(self):
        self.menu = Menu.objects.create(name="test")
        self.parent = MenuItem.objects.create(
            menu=self.menu, title="Parent", url="/parent/"
        )
        self.child = MenuItem.objects.create(
            menu=self.menu,
            title="Child",
            url="/parent/child/",
            parent=self.parent,
        )

    def test_should_show_children_in_path(self):
        self.parent._is_in_path = True
        self.assertTrue(self.parent.should_show_children())

    def test_should_show_children_parent_active(self):
        self.parent._is_in_path = False
        self.assertTrue(
            self.parent.should_show_children(parent_is_active=True)
        )

    def test_should_not_show_children(self):
        self.parent._is_in_path = False
        self.assertFalse(self.parent.should_show_children())

    def test_get_css_classes_active(self):
        self.parent._is_active = True
        self.parent._has_children = True
        self.parent._is_in_path = False

        classes = self.parent.get_css_classes()
        self.assertIn("active", classes)
        self.assertIn("has-children", classes)

    def test_get_css_classes_expanded(self):
        self.parent._is_active = False
        self.parent._has_children = True
        self.parent._is_in_path = True

        classes = self.parent.get_css_classes()
        self.assertIn("has-children", classes)
        self.assertIn("expanded", classes)


class DrawMenuTemplateTagTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.menu = Menu.objects.create(name="main_menu")
        self.home = MenuItem.objects.create(
            menu=self.menu, title="Home", url="/", order=1
        )
        self.about = MenuItem.objects.create(
            menu=self.menu, title="About", url="/about/", order=2
        )
        self.services = MenuItem.objects.create(
            menu=self.menu,
            title="Services",
            url="/about/services/",
            parent=self.about,
            order=1,
        )

    def test_draw_menu_renders(self):
        request = self.factory.get("/")
        template = Template("{% load menu_tags %}{% draw_menu 'main_menu' %}")
        context = Context({"request": request})
        html = template.render(context)

        self.assertIn("<ul>", html)
        self.assertIn("Home", html)
        self.assertIn("About", html)

    def test_draw_menu_active_class(self):
        request = self.factory.get("/about/")
        template = Template("{% load menu_tags %}{% draw_menu 'main_menu' %}")
        context = Context({"request": request})
        html = template.render(context)

        self.assertIn('class="active', html)
        self.assertIn("About", html)

    def test_draw_menu_expanded_children(self):
        request = self.factory.get("/about/services/")
        template = Template("{% load menu_tags %}{% draw_menu 'main_menu' %}")
        context = Context({"request": request})
        html = template.render(context)

        self.assertIn("Services", html)
        self.assertIn("expanded", html)

    def test_draw_menu_nonexistent(self):
        request = self.factory.get("/")
        template = Template(
            "{% load menu_tags %}{% draw_menu 'nonexistent' %}"
        )
        context = Context({"request": request})
        html = template.render(context)

        self.assertEqual(html.strip(), "")

    def test_draw_menu_no_request(self):
        template = Template("{% load menu_tags %}{% draw_menu 'main_menu' %}")
        context = Context({})
        html = template.render(context)

        self.assertEqual(html.strip(), "")


class MenuQueryOptimizationTest(TestCase):
    def setUp(self):
        self.menu = Menu.objects.create(name="test")
        for i in range(10):
            MenuItem.objects.create(
                menu=self.menu, title=f"Item {i}", url=f"/item{i}/", order=i
            )

    def test_single_query_for_menu(self):
        with self.assertNumQueries(2):
            Menu.objects.get_menu_tree("test", "/")

    def test_with_items_prefetch(self):
        with self.assertNumQueries(2):
            menu = Menu.objects.with_items().get(name="test")
            list(menu.items.all())
