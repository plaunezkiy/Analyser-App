from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import OneLineAvatarIconListItem
from kivy.lang import Builder

Builder.load_string('''
<Item>
    on_release: root.set_icon(check)
    CheckboxRightWidget:
        on_state: app.apply_filter(self.group, root.text, self.state)
        group: "check_"
        id: check

<FilterColumns>:
    spacing: "12dp"
    size_hint_y: None
    height: "155dp"

<Filter>:
    id: filter
    size_hint: (0.5, 0.5)
    title: 'Filters'
''')


class Item(OneLineAvatarIconListItem):
    def __init__(self, group, **kwargs):
        super(Item, self).__init__(**kwargs)
        self.ids.check.group += group

    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False


class FilterColumns(BoxLayout):
    def __init__(self, **kwargs):
        super(FilterColumns, self).__init__(**kwargs)
        tags = {'abc': ['A', 'B', 'C'], 'xyz': ['X', 'Y', 'Z']}
        for group in tags.keys():
            layout = BoxLayout(orientation='vertical')
            for tag in tags[group]:
                layout.add_widget(Item(text=tag, group=group))
            self.add_widget(layout)


class Filter(MDDialog):
    def __init__(self, **kwargs):
        self.type = 'custom'
        self.content_cls = FilterColumns()
        super(Filter, self).__init__(**kwargs)
