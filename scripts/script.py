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

from GI import *
import webbrowser
import subprocess
from scripts.EdsNotify import EdsNotify

def show_note(self):
    root = BoxLayout(orientation='vertical',padding=25, spacing=60)
    btn_layout = GridLayout(cols=2, row_force_default=True, row_default_height=40, spacing=10)
    agree = Button(text='I Understand The Risks', width=150)
    root.add_widget(Label(markup=True, halign="center", text="""Modifying Scripts can cause device not to boot.\nEdit only if you know what you are doing."""))
    root.add_widget(btn_layout)
    btn_layout.add_widget(agree)
    popup = Popup(background='atlas://images/eds/pop', title='Disclaimer',content=root, auto_dismiss=False,
    size_hint=(None, None), size=(425, 250))
    agree.bind(on_release=popup.dismiss)
    popup.open()
        
def initd(self):
    Box = BoxLayout(orientation="vertical", spacing=10)
    msg = GridLayout(cols=2, padding=15, spacing=10, size_hint_y=None)
    btn_layout = GridLayout(cols=1)
    done = Button(text="Done")
    btn_layout.add_widget(done)
    msg.bind(minimum_height=msg.setter('height'))
    try:
        file_listing = os.listdir(Rom_Initd)
        file_listing.sort()
        for item in file_listing:
            btnname = (CustomButton(text='%s' % item, font_size=10, size_hint_y=None, height=40))
            msg.add_widget(btnname)
            btnname.bind(on_release=do_button)
        root = ScrollView(size_hint=(None, None), size=(375, 290), do_scroll_x=False)
        root.add_widget(msg)
        Box.add_widget(root)
        Box.add_widget(btn_layout)
    
        popup = Popup(background='atlas://images/eds/pop', title='Init.d Scripts',content=Box, auto_dismiss=True,
        size_hint=(None, None), size=(400, 400))
        done.bind(on_release=popup.dismiss)
        popup.open()
    except:
        EdsNotify().run("'Init.d Directory Not Found", 'Cant Find:\n' + Rom_Initd)

def do_button(self):

    filepath = "%s/%s" % (Rom_Initd, self.text)

    if sys.platform.startswith('darwin'):
        subprocess.call(('open', filepath))
    elif os.name == 'nt':
        os.startfile(filepath)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', filepath))

def buildprop(self):
    try:
        filepath = "%s/" % (BuildProp)
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', filepath))
        elif os.name == 'nt':
            os.startfile(filepath)
        elif os.name == 'posix':
            subprocess.call(('xdg-open', filepath))
    except: 
        EdsNotify().run("'build.prop Not Found", 'Cant Find:\n' + BuildProp)
            
            
def uscript(self):
    try:
        webbrowser.open(UScript)
    except:
        EdsNotify()().run("'updater-script Not Found", 'Cant Find:\n' + UScript)          

def changes(self):
    try:
        webbrowser.open(Changelog)
    except:
        EdsNotify().run("'change.txt Not Found", 'Cant Find:\n' + Changelog)
            
def aroma_config(self):
    try:
        webbrowser.open(Aroma)
    except:
        EdsNotify().run("'aroma-confg Not Found", 'Cant Find:\n' + Aroma)
            
def rom_terms(self):
    try:
        webbrowser.open(Terms)
    except:
        EdsNotify().run("'terms.txt Not Found", 'Cant Find:\n' + Terms)
    
