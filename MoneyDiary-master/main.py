from kivy import Config
Config.set('graphics', 'multisamples', '0')
#Config.set('graphics', 'width', '1080')
#Config.set('graphics', 'height', '2340')

n = 3

from datetime import datetime
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty, ListProperty, ObjectProperty
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.clock import Clock
import random
from functools import partial

class EditPopup(Popup):
    entry = StringProperty()
    n = NumericProperty(None)
    def edit_record(self):
        entry=''.join(map(str,[self.dateP.text+','+self.catP.text+','+self.amountP.text+','+self.accountP.text+','+self.remarksP.text+'\n']))
        
        record = app.read_record()
        record[len(record)-int(self.n)-1] = entry
        app.write_record(record)
        app.output.update_button(app.output.layout)
        
        app.output.popup1.dismiss()
        self.dismiss()

class Showcase(FloatLayout):
    pass
    
class InputWidgets(FloatLayout):
    def __init__(self, **kwargs):
        super(InputWidgets, self).__init__(**kwargs)
    def append_record(self, entry, *args):
        path = 'record.txt'
        with open(path, mode='a') as csvfile:
            csvfile.write(entry)
        btnclose = Button(text='OK', size_hint_y=None, height=100)
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='Record Added'))
        content.add_widget(btnclose)
        popup = Popup(content=content, title='Append Entry',
                      size_hint=(None, None), size=(200*n, 200*n),
                      auto_dismiss=False)
        btnclose.bind(on_release=popup.dismiss)
        self.ids['DateT'].text= datetime.now().strftime('%Y-%m-%d %H:%M')
        self.ids['CatT'].text = ""
        self.ids['AmountT'].text = ""
        self.ids['AccountT'].text = ""
        self.ids['RemarksT'].text = ""
        app.content.get_parent_window().release_keyboard()
        popup.open()
        
    def cat_on_release(self, instance, popup):
        self.ids['CatT'].text = instance.text
        popup.dismiss()
        
    def acc_on_release(self, instance, popup):
        self.ids['AccountT'].text = instance.text
        popup.dismiss()
        
    def show_cat_popup(self, *args):
        cat = ['traffic','catering','beverage','entertainment ','misc']
        content = BoxLayout(orientation='vertical')
        popup = Popup(content=content, title='Choose Category',
                      size_hint=(None, None), size=(300*n, 240+50*len(cat)*n),
                      auto_dismiss=False)
        for c in cat:
            btn = Button(text=c, size_hint_y=None, height=150)
            btn.bind(on_release=partial(self.cat_on_release,popup=popup))
            content.add_widget(btn)
        app.content.get_parent_window().release_keyboard()
        popup.open()
        
    def show_acc_popup(self, *args):
        acc = ['Octopus','Payme','Credit Card','Cash','Others']
        content = BoxLayout(orientation='vertical')
        popup = Popup(content=content, title='Choose Account',
                      size_hint=(None, None), size=(300*n, 240+50*len(acc)*n),
                      auto_dismiss=False)
        for c in acc:
            btn = Button(text=c, size_hint_y=None, height=150)
            btn.bind(on_release=partial(self.acc_on_release, popup=popup))
            content.add_widget(btn)
        
        popup.open()
        
class OutputWidgets(ScrollView):
    popup1 = ObjectProperty(None)
    popup2 = ObjectProperty(None)
    def on_del_callback(self,instance, n):
        record = app.read_record()
        record.pop(len(record)-int(n)-1)
        app.write_record(record)
        self.update_button(self.layout)
        self.popup1.dismiss()
        
    def on_edit_callback(self,instance, n):
        record = app.read_record()
        popup = EditPopup()
        popup.entry = record[len(record)-int(n)-1]
        popup.n = n
        self.popup2 = popup
        popup.open()
        
    def show_popup(self, instance):
        btndel = Button(text='Delete', size_hint_y=None, height=100)
        btnedit = Button(text='Edit', size_hint_y=None, height=100)
        btnno = Button(text='Cancel', size_hint_y=None, height=100)
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='\n\n\nModify this entry?\n\n'+instance.text))
        choice = BoxLayout(orientation='horizontal')
        choice.add_widget(btnedit)
        choice.add_widget(btndel)
        choice.add_widget(btnno)
        content.add_widget(choice)
        popup = Popup(content=content, title='Modify Entry',
                      size_hint=(None, None), size=(300*n, 300*n),
                      auto_dismiss=False)
        btndel.bind(on_release=partial(self.on_del_callback, n=instance.id))
        btnedit.bind(on_release=partial(self.on_edit_callback, n=instance.id))
        btnno.bind(on_release=popup.dismiss)
        self.popup1 = popup
        popup.open()
        
            
    def __init__(self, **kwargs):
            
        super(OutputWidgets, self).__init__(**kwargs)
        layout = GridLayout(cols=1, spacing=1, size_hint_y=None, id="layout")
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        self.layout = layout
        self.update_button()
        self.add_widget(self.layout)
        
    def update_button(self, *args):
        self.layout.clear_widgets()
        record = app.read_record()
        for i in range(len(record)):
            btn = Button(text=str(''.join(map(str, record[len(record)-i-1]))).replace(',','\n'),text_size=(int(app.settings.textX.text), int(app.settings.textY.text)), font_size=int(app.settings.fontS.text),valign = "middle", halign = "left", size_hint_y=None, height=int(app.settings.cellH.text), id=str(i))
            btn.bind(on_press=self.show_popup)
            self.layout.add_widget(btn)
        
class SettingsWidgets(FloatLayout):
    settings = ListProperty()
    def read_settings(self, *args):
        path = 'settings.txt'

        with open(path, mode='r') as csvfile:
            setting = []
            for row in csvfile:
                setting.append(row)
        return setting
        
    def save_settings(self, *args):
        path = 'settings.txt'
        setting = self.cellH.text + '\n' + self.fontS.text + '\n' +self.textX.text + '\n' +self.textY.text + '\n'
        with open(path, mode='w') as csvfile:
            for row in setting:
                csvfile.write(row)
                
    def __init__(self, **kwargs):
        super(SettingsWidgets, self).__init__(**kwargs)
        self.settings = self.read_settings()
        self.cellH.text = self.settings[0].replace('\n','')
        self.fontS.text = self.settings[1].replace('\n','')
        self.textX.text = self.settings[2].replace('\n','')
        self.textY.text = self.settings[3].replace('\n','')

class DiaryApp(App):
    record = []
    input = ObjectProperty()
    output = ObjectProperty()
    settings = ObjectProperty()
    
    def read_record(self, *args):
        path = 'record.txt'

        with open(path, mode='r') as csvfile:
            record = []
            for row in csvfile:
                record.append(row)
        return record
        
    def write_record(self, record, *args):
        path = 'record.txt'
        with open(path, mode='w') as csvfile:
            for row in record:
                csvfile.write(row)
        
    def on_select_node(self, instance):
        # ensure that any keybaord is released
        self.content.get_parent_window().release_keyboard()

        self.content.clear_widgets()
        #try:
        w = getattr(self, 'show_%s' %
        instance.text.lower().replace(' ', '_'))()
        setattr(self,instance.text.lower().replace(' ', '_'),w)
        self.content.add_widget(w)
        
        #except:
        #    print('error')

    def on_pause(self):
        return True

    def build(self):
        global app 
        app = self
        root = BoxLayout(orientation='vertical', padding=20, spacing=20)
        menu = BoxLayout(orientation='horizontal',size_hint_y=None, height=50)
        
        input_btn = Button(text='Input')
        input_btn.bind(on_press=self.on_select_node)
        menu.add_widget(input_btn)
        
        output_btn = Button(text='Output')
        output_btn.bind(on_press=self.on_select_node)
        menu.add_widget(output_btn)
        
        set_btn = Button(text='Settings')
        set_btn.bind(on_press=self.on_select_node)
        menu.add_widget(set_btn)
        
        root.add_widget(menu)
        
        self.content = content = BoxLayout()
        root.add_widget(content)
        sc = Showcase()
        sc.content.add_widget(root)
        self.settings = SettingsWidgets()
        #self.content.add_widget(self.settings)
        #self.output = OutputWidgets()
        #self.content.add_widget(self.output)
        self.input = InputWidgets()
        self.content.add_widget(self.input)
        return sc

    def show_input(self):
        return InputWidgets(id='input')
    
    def show_output(self):
        return OutputWidgets(id='output')
        
    def show_settings(self):
        return SettingsWidgets(id='settings')

    

if __name__ in ('__main__', '__android__'):
    DiaryApp().run()
