#Copyright 2012 EasyDevStdio , wes342
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.


#!/usr/bin/env python
from scripts.GI import *
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.switch import Switch
from kivy.uix.settings import SettingItem, SettingsPanel, SettingOptions

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    
def dismiss(self):
    self._popup.dismiss()

def show_base_browse(self):
    content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
    self._popup = Popup(background='atlas://images/eds/pop',title="EDS File Browser", content=content, size_hint=(0.9, 0.9))
    self._popup.open()


def select_base_file(self, path, filename):
    try:
        shutil.rmtree(Rom)
        os.mkdir(Rom)
        global fileb
        fileb = os.path.join(path, filename[0])
        self.dismiss_popup()
        destpath = '%s/' % (Rom)
        z = zipfile.ZipFile(fileb)
        z.extractall(destpath)
        try:
            import pynotify
            if pynotify.init(NAME):
                n = pynotify.Notification("Base Rom Extracted Successfully", 'Selected file was:\n' + fileb)
                n.set_urgency(pynotify.URGENCY_NORMAL)
                n.show()
            else:
                print "there was a problem initializing the 'pynotify' module"
        except:
            print "you don't seem to have 'pynotify' installed" 
    except: 
        print 'no file selected'   
        self.dismiss_popup()


def select_base(self):   
    self.panel_layout.clear_widgets()
    title = Label(text='[b][color=ff2222][size=20]Base Rom Selection[/size][/color][/b]', markup = True, pos_hint={'x':-.05, 'y':.20})
    browse = CustomButton(text='BROWSE', pos_hint={'x':.0, 'y':.550}, size_hint=(.90, .06))
    download = CustomButton(text='Download', pos_hint={'x':.0, 'y':.450}, size_hint=(.90, .06))
    extract = CustomButton(text='Extract From RUU', pos_hint={'x':.0, 'y':.250}, size_hint=(.90, .06))
    port = CustomButton(text='Rom Porting (Experimental)', pos_hint={'x':.0, 'y':.150}, size_hint=(.90, .06))
    clean = Button(text='Clean Out Old Rom Files', pos_hint={'x':.0, 'y':-.05}, size_hint=(.90, .06), background_color=(1.4, 0, 0, 0.6))
    self.panel_layout.add_widget(title)
    self.panel_layout.add_widget(browse)
    self.panel_layout.add_widget(download)
    self.panel_layout.add_widget(extract)
    self.panel_layout.add_widget(port)
    self.panel_layout.add_widget(clean)
        
    def browse_files(instance):
        show_base_browse(self)
    browse.bind(on_release=browse_files)  

    def clean_files(instance):
        root = BoxLayout(orientation='vertical', spacing=20)
        btn_layout = GridLayout(cols=2, row_force_default=True, row_default_height=50, spacing=25)
        remove = Button(text='Clean', size_hint_x=None, width=150)
        cancel = Button(text='Cancel', size_hint_x=None, width=150)
        root.add_widget(Label(text='Are You Sure You Want To\nClean Out Current Rom Files?'))
        root.add_widget(btn_layout)
        btn_layout.add_widget(remove)
        btn_layout.add_widget(cancel)
        popup = Popup(background='atlas://images/eds/pop', title='Add Option',content=root, auto_dismiss=False,
        size_hint=(None, None), size=(350, 200))
        cancel.bind(on_release=popup.dismiss)
        popup.open()
        
        def clean_now(self):
            for root, dirs, files in os.walk(Rom):
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
                    try:
                        import pynotify
                        if pynotify.init(NAME):
                            n = pynotify.Notification("Clean Successful", 'Rom Files Have Been Removed')
                            n.set_urgency(pynotify.URGENCY_NORMAL)
                            n.show()
                        else:
                            print "there was a problem initializing the 'pynotify' module"
                    except:
                        print "you don't seem to have 'pynotify' installed" 
        remove.bind(on_press=clean_now)
        remove.bind(on_release=popup.dismiss)
    clean.bind(on_release=clean_files)

    
def boot_scripts(self):
    self.panel_layout.clear_widgets()
    title = Label(text='[b][color=ff2222][size=20]Init.d Scripts[/size][/color][/b]', markup = True, pos_hint={'x':-.05, 'y':.20})
    grid_layout = GridLayout(cols=3, row_force_default=True, row_default_height=40, spacing=10, pos_hint={'x':-.05, 'y':-.35})
    ext = CustomButton(text='Ext4 Tweak', pos_hint={'x':.0, 'y':.550}, size_hint=(.90, .06))
    sd = CustomButton(text='Sd Card Speed Fix', pos_hint={'x':.0, 'y':.550}, size_hint=(.90, .06))
    zip = CustomButton(text='Zipalign', pos_hint={'x':.0, 'y':.550}, size_hint=(.90, .06))
    bravia = CustomButton(text='Bravia Engine', pos_hint={'x':.0, 'y':.550}, size_hint=(.90, .06))
    self.panel_layout.add_widget(title)
    self.panel_layout.add_widget(grid_layout)
    grid_layout.add_widget(ext)
    grid_layout.add_widget(sd)
    grid_layout.add_widget(zip)
    grid_layout.add_widget(bravia)
    
    def cp_ext(self):
        shutil.copy('%s/00ext4'% (Initd), (Rom_Initd))
    ext.bind(on_release=cp_ext)
    
    def cp_sd(self):
        shutil.copy('%s/05sdcardspeedfix'% (Initd), (Rom_Initd))
    sd.bind(on_release=cp_sd)
    
    def cp_zip(self):
        shutil.copy('%s/06zipalign'% (Initd), (Rom_Initd))
    zip.bind(on_release=cp_zip)
    
    def cp_bravia(self):
        shutil.copy('%s/80bravia'% (Initd), (Rom_Initd))
    bravia.bind(on_release=cp_bravia)
    
    
def trans_scripts(self):
    print 'Hello Transitions'
    
def boot_anims(self):
    print 'Doing boot animations'


    
