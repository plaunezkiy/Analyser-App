from kivymd.uix.dialog import MDDialog
from kivymd.uix.toolbar import MDToolbar
from kivy.lang import Builder
from libs.recommendations import rec_combined, xyz_rec, abc_rec


Builder.load_string('''
#: import getdir os.getcwd

<FilterInfo>:
    title: 'Filtered products have:'
    size_hint: (0.5, 0.5)

<Toolbar>:
    title: 'Analyzer'
    right_action_items: [["information-outline", lambda x: self.show_filter_info(app.xyz_filter, app.abc_filter)], ["filter-outline", lambda x: app.filter.open()]]
    left_action_items: [["folder-outline", lambda x: app.file_manager.show(getdir())]]
    elevation: 10
    md_bg_color: 0.1, 0.1, 0.1, 1
''')


class FilterInfo(MDDialog):
    def __init__(self, xyz, abc, **kwargs):
        if xyz and not abc:
            recommendation = xyz_rec[xyz]
        elif abc and not xyz:
            recommendation = abc_rec[abc]
        elif xyz and abc:
            recommendation = rec_combined.loc[xyz][abc]
        else:
            recommendation = 'Unfiltered'
        self.text = recommendation
        super(FilterInfo, self).__init__(**kwargs)


class Toolbar(MDToolbar):
    def show_filter_info(self, xyz, abc):
        fi = FilterInfo(xyz, abc)
        return fi.open()
