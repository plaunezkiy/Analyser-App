from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.properties import ObjectProperty, ListProperty
from kivy.lang import Builder
from kivymd.uix.filemanager import MDFileManager
from libs.analysis import read_data, get_abc_xyz_matrix, get_bcg_matrix, reorder_data
from components.toolbar import Toolbar
from components.filter import Filter
from components.itemcard import ItemCard


kv = '''
BoxLayout:
    orientation: 'vertical'
    Toolbar:
    MDScrollViewRefreshLayout:
        id: refresh_layout
        refresh_callback: app.refresh
        root_layout: content
        FloatLayout:
            id: content 
            BoxLayout:
                id: main
'''


class AnalyzerApp(MDApp):
    data_tables = ObjectProperty()
    clean_data = None
    ordered_data = None
    abcxyz_data = None
    bcg_data = None
    filter = ObjectProperty()
    abc_filter = ''
    xyz_filter = ''
    file_manager = ObjectProperty()
    file_path = 'test.xlsx'

    def build(self):
        self.filter = Filter()
        self.file_manager = MDFileManager(
            select_path=lambda path: self.update_file_path(path),
            exit_manager=lambda a: self.file_manager.close(),
            ext=['.xlsx', '.xlsm', 'xlsb', '.xltx', 'xls'],
            selector='file',
        )
        self.file_manager.select_directory_on_press_button=self.file_manager.close
        self.fetch_data()
        self.root = Builder.load_string(kv)
        self.build_table()
        return self.root

    def refresh(self, *args):
        def refresh_callback(interval):
            self.root.ids.main.clear_widgets()
            self.root.ids.refresh_layout.refresh_done()
            self.tick = 0
            self.fetch_data()
            self.build_table()
        Clock.schedule_once(refresh_callback, 1)

    def apply_filter(self, group, tag, state, *args):
        if 'abc' in group:
            self.abc_filter = tag
            if state == 'normal' and tag == self.abc_filter:
                self.abc_filter = ''
        elif 'xyz' in group:
            self.xyz_filter = tag
            if state == 'normal' and tag == self.abc_filter:
                self.xyz_filter = ''
        self.refresh()

    def update_file_path(self, path):
        self.file_path = path
        self.file_manager.close()
        self.refresh()

    def fetch_data(self):
        self.clean_data = read_data(self.file_path)
        self.abcxyz_data = get_abc_xyz_matrix(self.clean_data)
        self.bcg_data = get_bcg_matrix(self.clean_data)
        self.ordered_data = reorder_data(self.abcxyz_data, self.bcg_data)

    def build_table(self):
        data = self.ordered_data
        if self.abc_filter:
            data = data[data['abc'] == self.abc_filter]
        if self.xyz_filter:
            data = data[data['xyz'] == self.xyz_filter]
        # columns = [
        #     ('Товар', dp(30)),
        #     ('Цена', dp(30)),
        #     ('Спрос', dp(30)),
        #     ('Темп роста', dp(30)),
        #     ('Доля рынка', dp(30)),
        # ]
        columns = [
            ('Product', dp(30)),
            ('Price', dp(30)),
            ('Demand', dp(30)),
            ('Growth', dp(30)),
            ('Share', dp(30)),
        ]
        row_data = data.values.tolist()

        self.data_tables = MDDataTable(
            size_hint=(1, 1),
            column_data=columns,
            row_data=row_data,
            pagination_menu_pos='auto',
            use_pagination=True,
        )
        self.data_tables.bind(on_row_press=self.row_click_handler)

        self.root.ids.main.add_widget(self.data_tables)

    def row_click_handler(self, table, row):
        i = row.Index
        item = self.ordered_data.loc[self.ordered_data['Product'] == i].values[0]
        data = self.clean_data.loc[self.clean_data['Product'] == i].set_index('Product').iloc[0]
        pu = ItemCard(item, data)
        return pu.open()


if __name__ == '__main__':
    AnalyzerApp().run()
