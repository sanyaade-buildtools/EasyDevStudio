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
from kivy.uix.checkbox import CheckBox
from kivy.uix.switch import Switch
from kivy.uix.settings import SettingItem, SettingsPanel, SettingOptions
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.config import ConfigParser
from scripts.EdsNotify import EdsNotify
import commands
import platform


config = ConfigParser()
config.read('%s/eds.ini' % Usr)

try:
    get_device = config.get("Source", "device")
except:
    get_device = "none"
    
try:
    get_branch = config.get("Source", "branch")
except:
    get_branch = "none"

try:
    make_jobs = config.get("Source", "make")
except:
    make_jobs = numprocs

try:
    sync_jobs = config.get("Source", "sync")
except:
    sync_jobs = 4

try:
    repo_path = config.get("Source", "repo_dir")
except:
    repo_path = "%s/build" % Usr

def no_os(self):
    root = BoxLayout(orientation='vertical', spacing=20)
    btn_layout = GridLayout(cols=1, row_force_default=True, row_default_height=40, spacing=25)
    cancel = Button(text='Cancel', size_hint_x=None, width=325)
    root.add_widget(Label(halign="center", text='You Must Be Running Linux to Build from source.\nCurrent Supported Distros are:\n"Ubuntu" Or "Linux Mint"'))
    root.add_widget(btn_layout)
    btn_layout.add_widget(cancel)
    popup = Popup(background='atlas://images/eds/pop', title='Unsupported OS',content=root, auto_dismiss=False,
    size_hint=(None, None), size=(350, 200))
    cancel.bind(on_release=popup.dismiss)
    popup.open()

def dismiss(self):
    self._popup.dismiss()

def build_kernel(self):
    kernel_menu(self)

# Function to check if packages are installed
def chkInstalled(arg):

    p = False

    cmd = "dpkg --get-selections " + arg
    p = commands.getoutput(cmd)
    p = p.split("\t")
    p = p[-1]
    if p == "install":
        p = True
    else:
        p = False

    return p

# Function to return and check installed packages per version. Currently Ubuntu & Mint supported.
def getPackages():
    
        # Start an array called "L" to hold the packages we find.
        L = []

        # This is just a package count, mainly to see if we return anything at the end.
        pcount = 0
    
        
        plat_list = platform.dist() # ('Ubuntu', '12.04', 'precise')
        plat_d = plat_list[0]
        plat_v = plat_list[1]
        plat_n = plat_list[2]
                
        if plat_d == "Ubuntu" or plat_d == "LinuxMint":
            pcount += 1
            P = ["git-core", "gnupg", "flex", "bison", "gperf", "libsdl1.2-dev", "libesd0-dev", "squashfs-tools", "build-essential", "zip", "curl", "libncurses5-dev", "zlib1g-dev", "openjdk-6-jdk", "pngcrush", "schedtool"]
            if plat_v == "12.10" or plat_v == "14":
                P.extend(["libwxgtk2.8-dev"])
            else:
                P.extend(["libwxgtk2.6-dev"])
            for x in P:
                i = chkInstalled(x)
                if i == False:
                    L.extend([x])
        else:
            print "Couldn't detect your os version. Please report this. Found: ( %s | %s | %s )" % (plat_d, plat_v, plat_n)
            del L[:]
            
    
        # Checks for x86_64
        check = (sys.maxsize > 2**32)
        if check is True and pcount == 1:
            if plat_d == "Ubuntu" or plat_d == "LinuxMint":
                if plat_v == "10.04" or plat_v == "9":
                    P = ["g++-multilib" "lib32z1-dev", "lib32ncurses5-dev", "lib32readline5-dev", "gcc-4.3-multilib", "g++-4.3-multilib"]
                    for x in P:
                        i = chkInstalled(x)
                        if i == False:
                            L.extend([x])
                elif plat_v == "11.04" or plat_v == "11":
                    P = ["g++-multilib" "lib32z1-dev", "lib32ncurses5-dev", "lib32readline-gplv2-dev", "gcc-4.3-multilib", "g++-4.3-multilib"]
                    for x in P:
                        i = chkInstalled(x)
                        if i == False:
                            L.extend([x])
                elif plat_v == "12.10" or plat_v == "12.04" or plat_v == "11.10" or plat_v == "14" or plat_v == "13" or plat_v == "12":
                    P = ["g++-multilib", "lib32z1-dev", "lib32ncurses5-dev", "lib32readline-gplv2-dev"]
                    for x in P:
                        i = chkInstalled(x)
                        if i == False:
                            L.extend([x])
                else:
                    print "Nothing to extend, version not matched"
    
        # If package pcount and L are zero, then there was an issue, this shouldn't happen. Either get "True" or a package list.
        if not L and pcount == 0:
            print "Empty package list", "After looking at your packages the list is empty, maybe an unsupported distro or filesystem error. Either way I am not able to help without some information. You will not be able to use most features until you install the needed packages, be warned.\n\n Thanks."
            #exit(1)
        elif not L and pcount == 1:
            pass
            return True
        else:
            return L
            

def install_packages(instance):
    root = BoxLayout(orientation='vertical', spacing=25)
    btn_layout = GridLayout(cols=3, row_force_default=True, row_default_height=50, spacing=25)
    install = Button(text='Install', size_hint_x=None, width=90)
    view = Button(text='View', size_hint_x=None, width=90)
    cancel = Button(text='Cancel', size_hint_x=None, width=90)
    root.add_widget(Label(text='Are You Sure You Want To\nInstall needed packages?'))
    root.add_widget(btn_layout)
    btn_layout.add_widget(install)
    btn_layout.add_widget(view)
    btn_layout.add_widget(cancel)
    popup = Popup(background='atlas://images/eds/pop', title='Install packages',content=root, auto_dismiss=False,
    size_hint=(None, None), size=(350, 200))
    cancel.bind(on_release=popup.dismiss)
    popup.open()
    
    def install_now(self):
        import subprocess as sp
        p = getPackages()
        packages = ",".join(p).replace(",", " ")
        print packages
        cmd = "gnome-terminal -e \"sudo apt-get install -y %s\"" % (packages)
        sp.Popen(cmd, shell=True)
        
    def view_packages(instance):
        p = getPackages()
        Box = BoxLayout(orientation="vertical", spacing=10)
        msg = GridLayout(cols=1, spacing=0, size_hint_y=None)
        btn_layout = GridLayout(cols=1)
        btn = Button(text="Done")
        btn_layout.add_widget(btn)
        msg.bind(minimum_height=msg.setter('height'))
        for x in p:
            lbl = (Label(text='%s' % x, font_size=10, size_hint_y=None, height=40))
            msg.add_widget(lbl)
        root = ScrollView(size_hint=(None, None), size=(375, 290), do_scroll_x=False)
        root.add_widget(msg)
        Box.add_widget(root)
        Box.add_widget(btn_layout)
        

        popup = Popup(background='atlas://images/eds/pop', title='Needed packages',content=Box, auto_dismiss=True,
        size_hint=(None, None), size=(400, 400))
        btn.bind(on_release=popup.dismiss)
        popup.open()
            
    install.bind(on_press=install_now)
    view.bind(on_press=view_packages)
    install.bind(on_release=popup.dismiss)
    

def kernel_base(self):
    layout = GridLayout(cols=1, size_hint=(None, 2.5), width=700)
    layout.bind(minimum_height=layout.setter('height'))
    panel = SettingsPanel(title="Kernel Base", settings=self)   
    main = BoxLayout(orientation = 'vertical')
    root = ScrollView(size_hint=(None, None),bar_margin=-11, bar_color=(47 / 255., 167 / 255., 212 / 255., 1.), do_scroll_x=False)
    root.size = (600, 400)
    root.add_widget(layout)
    main.add_widget(root)
    done = Button(text ='Download Kernel Base Now')
    main.add_widget(done)

    aria = SettingItem(panel = panel, title = "HTC Aria",disabled=False, desc = "(HTC) (WWE) (MR) (2.6.32) (v2.2)")
    aria_radio = CheckBox(group='kernel',active=True)
    aria.add_widget(aria_radio)
    layout.add_widget(aria)

    inc = SettingItem(panel = panel, title = "HTC Incredible",disabled=False, desc = "(Verizon) (WWE) (MR) (2.6.35) (v2.3)")
    inc_radio = CheckBox(group='kernel',active=False)
    inc.add_widget(inc_radio)
    layout.add_widget(inc)
    
    inc2 = SettingItem(panel = panel, title = "HTC Incredible 2",disabled=False, desc = "(Verizon) (WWE) (MR) (2.6.35) (v2.3)")
    inc2_radio = CheckBox(group='kernel',active=False)
    inc2.add_widget(inc2_radio)
    layout.add_widget(inc2)
    
    incs = SettingItem(panel = panel, title = "HTC Incredible S",disabled=False, desc = "(Htc) (WWE) (MR) (2.6.35) (v2.3)")
    incs_radio = CheckBox(group='kernel',active=False)
    incs.add_widget(incs_radio)
    layout.add_widget(incs)

    e4g = SettingItem(panel = panel, title = "HTC Evo 4G",disabled=False, desc = "(Sprint) (WWE) (MR) (2.6.35) (v2.3)")
    e4g_radio = CheckBox(group='kernel',active=False)
    e4g.add_widget(e4g_radio)
    layout.add_widget(e4g)
       
    e3d = SettingItem(panel = panel, title = "HTC Evo 3D",disabled=False, desc = "(Sprint) (WWE) (MR) (2.6.35) (v2.3)")
    e3d_radio = CheckBox(group='kernel',active=False)
    e3d.add_widget(e3d_radio)
    layout.add_widget(e3d)
    
    sen = SettingItem(panel = panel, title = "HTC Sensation",disabled=False, desc = "(T-Mobile) (USA) (CRC) (2.6.35) (2.3)")
    sen_radio = CheckBox(group='kernel',active=False)
    sen.add_widget(sen_radio)
    layout.add_widget(sen)
    
    tb = SettingItem(panel = panel, title = "HTC Thunderbolt",disabled=False, desc = "(Verizon) (WWE) (MR) (2.6.35) (v2.3)")
    tb_radio = CheckBox(group='kernel',active=False)
    tb.add_widget(tb_radio)
    layout.add_widget(tb)
    
    ama = SettingItem(panel = panel, title = "HTC Amaze",disabled=False, desc = "(T-Mobile) (USA) (CRC) (2.6.35) (v2.3)")
    ama_radio = CheckBox(group='kernel',active=False)
    ama.add_widget(ama_radio)
    layout.add_widget(ama)
    
    g2 = SettingItem(panel = panel, title = "G2",disabled=False, desc = "(T-Mobile) (USA) (MR) (2.6.35) (v2.3)")
    g2_radio = CheckBox(group='kernel',active=False)
    g2.add_widget(g2_radio)
    layout.add_widget(g2)
    
    i4g = SettingItem(panel = panel, title = "HTC Inspire 4G",disabled=False, desc = "(AT&T) (USA) (MR) (2.6.35) (v2.3)")
    i4g_radio = CheckBox(group='kernel',active=False)
    i4g.add_widget(i4g_radio)
    layout.add_widget(i4g)
    
    popup = Popup(background='atlas://images/eds/pop', title='Kernel Base', content=main, auto_dismiss=True, size_hint=(None, None), size=(630, 500))
    done.bind(on_release=popup.dismiss)
    popup.open()


def kernel_mods(self):
    Box = BoxLayout(orientation="vertical")
    layout = SettingsPanel(title="Select Mods You Want Added to Kernel", settings=self, size_hint=(1.1, None))
    btn_layout = GridLayout(cols=1)
    btn = Button(text="Continue")
    btn_layout.add_widget(btn)
    layout.bind(minimum_height=layout.setter('height'))

    oc = SettingItem(panel = layout, title = "Add Over Clocking",disabled=False, desc = "Adds Over Clocking Capabilities")
    oc_switch = Switch(active=False)
    oc.add_widget(oc_switch)
    layout.add_widget(oc)
  
    modu = SettingItem(panel = layout, title = "Add Module Support",disabled=False, desc = "Adds Module support to kernel")
    modu_switch = Switch(active=False)
    modu.add_widget(modu_switch)
    layout.add_widget(modu)
 
    wifi = SettingItem(panel = layout, title = "Compile Wifi Module",disabled=False, desc = "The wifi module may need to be recompiled")
    wifi_switch = Switch(active=False)
    wifi.add_widget(wifi_switch)
    layout.add_widget(wifi)

    sass = SettingItem(panel = layout, title = "Add Smart Ass Governor",disabled=False, desc = "Adds Smart Ass as Default Governor")
    sass_switch = Switch(active=False)
    sass.add_widget(sass_switch)
    layout.add_widget(sass)

    root = ScrollView(size_hint=(None, None), size=(600, 300), do_scroll_x=False, do_scroll_y=False)
    root.add_widget(layout)
    Box.add_widget(root)
    Box.add_widget(btn_layout)

    popup = Popup(background='atlas://images/eds/pop', title='Kernel Mods',content=Box, auto_dismiss=True,
    size_hint=(None, None), size=(630, 400))
    btn.bind(on_release=popup.dismiss)
    popup.open()

def pull_conf(self):
    print 'Pull Config file from Device'

def kernel_other(self):
    root = BoxLayout(orentation = 'vertical')
    scroll = ScrollView(size_hint=(None, 2.5), do_scroll_x=False)
    root.add_widget(scroll)
    btn_layout = GridLayout(cols=1)
    scroll.add_widget(btn_layout)

    layout = GridLayout(cols=1, size_hint=(None, 2.5), width=700)
    layout.bind(minimum_height=layout.setter('height'))
    panel = SettingsPanel(title="Advanced Kernel Options", settings=self)   
    main = BoxLayout(orientation = 'vertical')
    root = ScrollView(size_hint=(None, None),bar_margin=-11, bar_color=(47 / 255., 167 / 255., 212 / 255., 1.), do_scroll_x=False)
    root.size = (600, 400)
    root.add_widget(layout)
    main.add_widget(root)
    layout.add_widget(panel)
    done = Button(text ='Done')
    main.add_widget(done)
 
    popup = Popup(background='atlas://images/eds/pop', title='Advanced Kernel Options', content=main, auto_dismiss=True, size_hint=(None, None), size=(630, 500))
    done.bind(on_release=popup.dismiss)
    popup.open()


def branch_select(self):
    Box = BoxLayout(orientation="vertical", spacing=10)
    base = BoxLayout(orientation="vertical", spacing=15, padding=15)
    btn_layout = GridLayout(cols=2, spacing=10)
    cancel = Button(text='Cancel')
    btn_layout.add_widget(cancel)
    
    aosp = CustomButton(text='AOSP')
    cm = CustomButton(text='Cyanogenmod')
    base.add_widget(aosp)
    base.add_widget(cm)
    
    # for root widget do_scroll_y=True to enable scrolling 
    root = ScrollView(size_hint=(None, None), size=(525, 150), do_scroll_x=False, do_scroll_y=True)
    root.add_widget(base)
    Box.add_widget(root)
    Box.add_widget(btn_layout)

    popup = Popup(background='atlas://images/eds/pop', title='Branch Selection',content=Box, auto_dismiss=True,
    size_hint=(None, None), size=(550, 260))
    cancel.bind(on_release=popup.dismiss)
    aosp.bind(on_release=aosp_branch)
    aosp.bind(on_release=popup.dismiss)
    cm.bind(on_release=cm_branch)
    cm.bind(on_release=popup.dismiss)
    popup.open()
    
def aosp_branch(self):
    config.read('%s/eds.ini' % Usr)
    Box = BoxLayout(orientation="vertical", spacing=10)
    base = SettingsPanel(title="", settings=self)
    btn_layout = GridLayout(cols=2, spacing=10)
    select = Button(text="Select")
    btn_layout.add_widget(select)
    cancel = Button(text='Cancel')
    btn_layout.add_widget(cancel)
    base.bind(minimum_height=base.setter('height'))

#################################################
# Removed branch type selection menu because I think it was useless
# Should be the same for Aosp and CM 
# If not I can redo it.
#################################################
    
    GB = SettingItem(panel = base, title = "Gingerbread",disabled=False, desc = "Android 2.3,  kernel 2.6.35,  Api 9-10 ")
    GB_radio = CheckBox(group='base',active=False)
    GB.add_widget(GB_radio)
    base.add_widget(GB)

    ICS = SettingItem(panel = base, title = "Ice Cream Sandwitch",disabled=False, desc = "Android 4.0,  kernel 3.0.1,  Api 14-15")
    ICS_radio = CheckBox(group='base',active=False)
    ICS.add_widget(ICS_radio)
    base.add_widget(ICS)

    JB = SettingItem(panel = base, title = "Jellybean",disabled=False, desc = "Android 4.1,  kernel 3.1.10,  Api 16-?")
    JB_radio = CheckBox(group='base',active=False)
    JB.add_widget(JB_radio)
    base.add_widget(JB)    
    
    # for root widget do_scroll_y=True to enable scrolling 
    root = ScrollView(size_hint=(None, None), size=(525, 240), do_scroll_x=False, do_scroll_y=False)
    root.add_widget(base)
    Box.add_widget(root)
    Box.add_widget(btn_layout)

########################################
# This should be working fine 
# Not sure if there is a better way to do this
#########################################

    def on_checkbox(checkbox, value):
        title = GB.title
        if value:
            config.set("Source", "branch", "aosp-gb")
        else:
            print 'The checkbox',title, 'is inactive'

    GB_radio.bind(active=on_checkbox)
    
    def checkbox_active(checkbox, value):
        title = ICS.title
        if value:
            config.set("Source", "branch", "aosp-ics")
        else:
            print 'The checkbox',title, 'is inactive'
    
    ICS_radio.bind(active=checkbox_active)
    
    def on_active(checkbox, value):
        title = JB.title
        if value:
            config.set("Source", "branch", "aosp-jb")
        else:
            print 'The checkbox',title, 'is inactive'
                        
    JB_radio.bind(active=on_active)
    
    def set_branch(self):
        config.write()
    select.bind(on_release=set_branch)
    
    popup = Popup(background='atlas://images/eds/pop', title='Branch Selection',content=Box, auto_dismiss=True,
    size_hint=(None, None), size=(550, 350))
    select.bind(on_release=popup.dismiss)
    cancel.bind(on_release=popup.dismiss)
    cancel.bind(on_release=branch_select(self))
    popup.open()

def cm_branch(self):
    config.read('%s/eds.ini' % Usr)
    Box = BoxLayout(orientation="vertical", spacing=10)
    base = SettingsPanel(title="", settings=self)
    btn_layout = GridLayout(cols=2, spacing=10)
    select = Button(text="Select")
    btn_layout.add_widget(select)
    cancel = Button(text='Cancel')
    btn_layout.add_widget(cancel)
    base.bind(minimum_height=base.setter('height'))

#################################################
# Removed branch type selection menu because I think it was useless
# Should be the same for Aosp and CM 
# If not I can redo it.
#################################################
    
    Cm7 = SettingItem(panel = base, title = "Cyanogenmod 7",disabled=False, desc = "Android 2.3,  kernel 2.6.35,  Api 9-10 ")
    Cm7_radio = CheckBox(group='base',active=False)
    Cm7.add_widget(Cm7_radio)
    base.add_widget(Cm7)

    Cm9 = SettingItem(panel = base, title = "Cyanogenmod 9",disabled=False, desc = "Android 4.0,  kernel 3.0.1,  Api 14-15")
    Cm9_radio = CheckBox(group='base',active=False)
    Cm9.add_widget(Cm9_radio)
    base.add_widget(Cm9)

    Cm10 = SettingItem(panel = base, title = "Cyanogenmod 10",disabled=False, desc = "Android 4.1,  kernel 3.1.10,  Api 16-?")
    Cm10_radio = CheckBox(group='base',active=False)
    Cm10.add_widget(Cm10_radio)
    base.add_widget(Cm10)    
    
    # for root widget do_scroll_y=True to enable scrolling 
    root = ScrollView(size_hint=(None, None), size=(525, 240), do_scroll_x=False, do_scroll_y=False)
    root.add_widget(base)
    Box.add_widget(root)
    Box.add_widget(btn_layout)

########################################
# This should be working fine 
# Not sure if there is a better way to do this
#########################################

    def on_checkbox(checkbox, value):
        title = Cm7.title
        if value:
            config.set("Source", "branch", "cm-gb")
        else:
            print 'The checkbox',title, 'is inactive'

    Cm7_radio.bind(active=on_checkbox)
    
    def checkbox_active(checkbox, value):
        title = Cm9.title
        if value:
            config.set("Source", "branch", "cm-ics")
        else:
            print 'The checkbox',title, 'is inactive'
    
    Cm9_radio.bind(active=checkbox_active)
    
    def on_active(checkbox, value):
        title = Cm10.title
        if value:
            config.set("Source", "branch", "cm-jb")
        else:
            print 'The checkbox',title, 'is inactive'
                        
    Cm10_radio.bind(active=on_active)
    
    def set_branch(self):
        config.write()
    select.bind(on_release=set_branch)
    
    popup = Popup(background='atlas://images/eds/pop', title='Branch Selection',content=Box, auto_dismiss=True,
    size_hint=(None, None), size=(550, 350))
    select.bind(on_release=popup.dismiss)
    cancel.bind(on_release=popup.dismiss)
    cancel.bind(on_release=branch_select(self))
    popup.open()
    
def device_select(self):
    layout = GridLayout(cols=1, size_hint=(None, 0.5), width=700)
    layout.bind(minimum_height=layout.setter('height'))
    panel = SettingsPanel(title="Select Device", settings=self)   
    main = BoxLayout(orientation = 'vertical')
    root = ScrollView(size_hint=(None, None),bar_margin=-11, bar_color=(47 / 255., 167 / 255., 212 / 255., 1.), do_scroll_x=False)
    root.size = (600, 400)
    root.add_widget(layout)
    main.add_widget(root)
    btn_layout = GridLayout(cols=2, spacing=10)
    main.add_widget(btn_layout)
    done = Button(text ='Select')
    btn_layout.add_widget(done)
    cancel = Button(text='Cancel')
    btn_layout.add_widget(cancel)
    
#################################################
# I think function for pulling device list should go here
# If you can also pull some info for the device it would be nice to have it 
# set as desc =  
# If not no worries (I just think it would be cool)
#################################################
 
    device = SettingItem(panel = panel, title = "Some Device", disabled=False, desc="")
    device_radio = CheckBox(group='device',active=False)
    device.add_widget(device_radio)
    layout.add_widget(device)
    
    def set_device(self):
        config.set("Source", "device", device.title)
        config.write()
    done.bind(on_release=set_device)

    
    popup = Popup(background='atlas://images/eds/pop', title='Device Selection', content=main, auto_dismiss=True, size_hint=(None, None), size=(630, 500))
    cancel.bind(on_release=popup.dismiss)
    done.bind(on_release=popup.dismiss)
    popup.open()

    
def kernel_menu(self):
    try:
        if (os.name == "posix"):
            self.panel_layout.clear_widgets()
            title = Label(text='[b][color=#22A0D6][size=20]Kernel Building[/size][/color][/b]', markup = True, pos_hint={'x':-.05, 'y':.20})
            p = getPackages()
            package_count = 0
            if p == True:
                package_count = 0
            else:
                for x in p:
                    package_count += 1
            
            grid_layout = GridLayout(cols=1, row_force_default=True, row_default_height=40, spacing=10, pos_hint={'x':-.05, 'y':-.50})
            k_base = CustomButton(text='2. Select Kernel Base', pos_hint={'x':.0, 'y':.550}, size_hint=(.90, .06))
            k_conf = CustomButton(text='3. Pull Config from Device', pos_hint={'x':.0, 'y':.300}, size_hint=(.90, .06))
            k_mods = CustomButton(text='4. Select Kernel Mods', pos_hint={'x':.0, 'y':.550}, size_hint=(.90, .06))
            k_build = CustomButton(text='5. Build Kernel', pos_hint={'x':.0, 'y':.550}, size_hint=(.90, .06))
            k_other = CustomButton(text='Other Kernel Options', pos_hint={'x':.0, 'y':.550}, size_hint=(.90, .06))
            self.panel_layout.add_widget(title)
            if package_count == 0:
                pass
            else:
                i_packages = Button(text='Install needed packages: %s' % package_count, pos_hint={'x':.0, 'y':.550}, size_hint=(.90, .06), background_color=(1.4, 0, 0, 0.6))

            if package_count == 0:
                pass
            else:
                self.panel_layout.add_widget(i_packages)
            self.panel_layout.add_widget(grid_layout)
            grid_layout.add_widget(k_base)
            grid_layout.add_widget(k_conf)
            grid_layout.add_widget(k_mods)
            grid_layout.add_widget(k_build)
            grid_layout.add_widget(k_other)
            
            def ker_base(instance):
                kernel_base(self)
            k_base.bind(on_release=ker_base)
    
            def ker_conf(instance):
                pull_conf(self)
            k_conf.bind(on_release=ker_conf)
    
            def ker_mods(instance):
                kernel_mods(self)
            k_mods.bind(on_release=ker_mods)
            
            def ker_build(instance):
                print "build kernel"
            k_build.bind(on_release=ker_build)
    
            def ker_other(instance):
                kernel_other(self)
            k_other.bind(on_release=ker_other)
            
        else:
            self.panel_layout.clear_widgets()
            title = Label(text='[b][color=ff2222][size=20]Kernel Building[/size][/color][/b]', markup = True, pos_hint={'x':-.05, 'y':.20})
            lin = Label(text='[b][color=ffffff][size=15]You Must Be Using Linux to Build Kernels[/size][/color][/b]', markup = True, pos_hint={'x':-.05, 'y':.100})
            self.panel_layout.add_widget(title)
            self.panel_layout.add_widget(lin)
            
        if package_count == 0:
            pass
        else:
            i_packages.bind(on_release=install_packages)
    except:
        no_os(self)
        

def source_menu(self):
    try:  
        self.panel_layout.clear_widgets()
        title = Label(text='[b][color=#22A0D6][size=20]Source Rom Building[/size][/color][/b]', markup = True, pos_hint={'x':-.05, 'y':.20})
        p = getPackages()
        package_count = 0
        if p == True:
            package_count = 0
        else:
            for x in p:
                package_count += 1
    except:
        no_os(self)
            
    branch = CustomButton(text='Select Branch', pos_hint={'x':.5, 'y':.375}, size_hint=(.40, .06))
    device = CustomButton(text='Select Device', pos_hint={'x':.0, 'y':.375}, size_hint=(.40, .06))
    jobs = BoxLayout(orientation='vertical', spacing=5, size_hint=(0.9, .20), pos_hint={'x':.02, 'y':.05})
    
    stitle = Label(text='How Many [b]Sync[/b] Jobs, Default = %s' % sync_jobs, markup=True)
    f = float(sync_jobs)
    sslide = Slider(min=0, max=16, value=f)
    s_value = Label(text='%s' % sync_jobs, pos_hint={'x':-.50, 'y':-.325})
    
    mtitle = Label(text='How Many [b]Make[/b] Jobs, Default = %s' % make_jobs, markup=True)
    m = float(make_jobs)
    mslide = Slider(min=-0, max=m, value=m)
    m_value = Label(text='%s' % make_jobs, pos_hint={'x':-.50, 'y':-.425})


    dev = Label(markup=True, text="[b][color=#adadad]Current Device =[/color][/b] %s" % get_device, pos_hint={'x':-.300, 'y':-.15})
    bra = Label(markup=True, text="[b][color=#adadad]Current Branch =[/color][/b] %s" % get_branch, pos_hint={'x':.20, 'y':-.15})
    repo = Label(markup=True, text="[b][color=#adadad]Repo Path =[/color][/b] %s" % repo_path, pos_hint={'x':-.05, 'y':-.0})

    jobs.add_widget(stitle)
    self.panel_layout.add_widget(s_value)
    jobs.add_widget(sslide)
    jobs.add_widget(mtitle)
    self.panel_layout.add_widget(m_value)
    jobs.add_widget(mslide)
    sync = CustomButton(text='Sync', pos_hint={'x':.0, 'y':-.05}, size_hint=(.40, .06))
    make = CustomButton(text='Make', pos_hint={'x':.5, 'y':-.05}, size_hint=(.40, .06))

    if package_count == 0:
        pass
    else:
        i_packages = Button(text='Install needed packages: %s' % package_count, pos_hint={'x':.0, 'y':.550}, size_hint=(.90, .06), background_color=(1.4, 0, 0, 0.6))
    self.panel_layout.add_widget(title)
    if package_count == 0:
        pass
    else:
        self.panel_layout.add_widget(i_packages)
    self.panel_layout.add_widget(branch)
    self.panel_layout.add_widget(device)
    self.panel_layout.add_widget(jobs)
    self.panel_layout.add_widget(sync)
    self.panel_layout.add_widget(make)
    self.panel_layout.add_widget(bra)
    self.panel_layout.add_widget(dev)
    self.panel_layout.add_widget(repo)

    def show_branch(instance):
        branch_select(self)
    branch.bind(on_release=show_branch) 
    
    def show_device(instance):
        device_select(self)
    device.bind(on_release=show_device)


    def sync_slider(self, value):
        f = int(float(value))
        print f
    sslide.bind(value=sync_slider)

    
    def make_slider(self, value):
        m = int(float(value))
        print m
    mslide.bind(value=make_slider)

########################################
# Sync and Make Functions  
# Not Sure Exactly what needs to be done here
#########################################

    def sync_now(self):
        import subprocess as sp
        cmd = "gnome-terminal -e \"sudo apt-get install -y %s\""
        sp.Popen(cmd, shell=True)
    sync.bind(on_release=sync_now)

    
    def make_now(self):
        import subprocess as sp
        cmd = "gnome-terminal -e \"sudo apt-get install -y %s\""
        sp.Popen(cmd, shell=True)
    make.bind(on_release=make_now)
    
    if package_count == 0:
        pass
    else:
        i_packages.bind(on_release=install_packages)
