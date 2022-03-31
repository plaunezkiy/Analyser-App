from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineListItem, MDList
from libs.recommendations import rec_combined, bcg_rec

Builder.load_string('''
<RecLabel>:
    halign: 'center'
    size_hint_y: None
    height: self.texture_size[1]

<ItemInfo>:
    size_hint_y: None
    height: "500dp"

<ItemCard>:
''')


class RecLabel(MDLabel):
    pass


class ItemInfo(BoxLayout):
    def __init__(self, item, data, **kwargs):
        super(ItemInfo, self).__init__(**kwargs)
        abc, xyz, growth, share = item[1:]
        self.spacing = 10
        # ScrollView section
        info = MDList()
        data_dict = data[1:8].to_dict()
        for key in data_dict.keys():
            info.add_widget(
                TwoLineListItem(
                    text=key.capitalize(),
                    secondary_text=str(data_dict[key])
                )
            )
        info.add_widget(TwoLineListItem())
        self.add_widget(info)

        # Recommendations section
        recs = BoxLayout(orientation='vertical', spacing=20)
        recs.add_widget(RecLabel(text='ABC-XYZ advice', font_style='H4'))
        recs.add_widget(RecLabel(text=rec_combined.loc[xyz][abc], font_style='Subtitle1'))

        recs.add_widget(RecLabel(text='BCG advice', font_style='H4'))
        recs.add_widget(RecLabel(text=bcg_rec[growth][share], font_style='Subtitle1'))
        # Заглушка
        recs.add_widget(Widget())
        self.add_widget(recs)


class ItemCard(MDDialog):
    def __init__(self, item, data, **kwargs):
        self.type = 'custom'
        self.title = f'Product: {item[0]}'
        self.content_cls = ItemInfo(item, data)
        super(ItemCard, self).__init__(**kwargs)
