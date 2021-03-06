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
import urllib

kernels = []
htc = []

# Checks For Supported Kernels from EDSLive
try:
    filehandle = urllib.urlopen(Ker)
except IOError:
    print "Failed to grab url: %s" % Ker

for lines in filehandle.readlines():
    
    x = lines.strip()
    kernels.extend([x])

filehandle.close()

try:
    filehandle = urllib.urlopen(Htc_Ker)
except IOError:
    print "Failed to grab url: %s" % Htc_Ker

for lines in filehandle.readlines():
    
    x = lines.strip()
    htc.extend([x])

filehandle.close()

# Popup To display that detected os is not supported for source building (windows, mac)
def no_os(self):
    root = BoxLayout(orientation='vertical', spacing=20)
    btn_layout = GridLayout(cols=1, row_force_default=True, row_default_height=40, spacing=25)
    cancel = Button(text='Cancel', size_hint_x=None, width=355)
    root.add_widget(Label(halign="center", text='You Must Be Running 64bit Linux to Build Kernels.\nCurrent Supported Distros are:\n"Ubuntu" Or "Linux Mint"'))
    root.add_widget(btn_layout)
    btn_layout.add_widget(cancel)
    popup = Popup(background='atlas://images/eds/pop', title='Unsupported OS',content=root, auto_dismiss=False,
    size_hint=(None, None), size=(375, 200))
    cancel.bind(on_release=popup.dismiss)
    popup.open()

def dismiss(self):
    self._popup.dismiss()

# Function to check if packages that are needed to build source are installed
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
    
        
        plat_list = platform.dist() # ('Ubuntu', '12.04', 'precise') or ('LinuxMint', '13', 'Maya')
        plat_d = plat_list[0]
        plat_v = plat_list[1]
        plat_n = plat_list[2]
                
        if plat_d == "Ubuntu" or plat_d == "LinuxMint":
            pcount += 1
            P = ["git-core"]
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
                    P = ["ia32-libs", "gcc-multilib", "g++-multilib", "automake"]
                    for x in P:
                        i = chkInstalled(x)
                        if i == False:
                            L.extend([x])
                elif plat_v == "11.04" or plat_v == "11":
                    P = ["ia32-libs", "gcc-multilib", "g++-multilib", "automake"]
                    for x in P:
                        i = chkInstalled(x)
                        if i == False:
                            L.extend([x])
                elif plat_v == "12.10" or plat_v == "12.04" or plat_v == "11.10" or plat_v == "14" or plat_v == "13" or plat_v == "12":
                    P = ["ia32-libs", "gcc-multilib", "g++-multilib", "automake"]
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
            
# Popup to ask if user wants to install needed packages
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
    
    # Actual install function
    def install_now(self):
        import subprocess as sp
        p = getPackages()
        packages = ",".join(p).replace(",", " ")
        print packages
        cmd = "gnome-terminal -e \"sudo apt-get install -y %s\"" % (packages)
        sp.Popen(cmd, shell=True)
        
# Allows users to view needed packages before installing them 
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

def kernel_type(self):
    Box = BoxLayout(orientation="vertical", spacing=10)
    msg = GridLayout(cols=1, padding=15, spacing=10, size_hint_y=None)
    btn_layout = GridLayout(cols=1)
    done = Button(text="Done")
    btn_layout.add_widget(done)
    msg.bind(minimum_height=msg.setter('height'))
    
    over = CustomButton(text='HTC Kernels', size=(475, 40), size_hint=(None, None))
    over.bind(on_release=load_ker)
    
    msg.add_widget(over)
    
    root = ScrollView(size_hint=(None, None),bar_margin=-22, size=(475, 390), do_scroll_x=False)
    root.add_widget(msg)
    Box.add_widget(root)
    Box.add_widget(btn_layout)
    
    popup = Popup(background='atlas://images/eds/pop', title='Kernel Mods',content=Box, auto_dismiss=True,
    size_hint=(None, None), size=(520, 500))
    done.bind(on_release=popup.dismiss)
    popup.open()

def load_ker(self):
    Box = BoxLayout(orientation="vertical", spacing=10)
    panel = SettingsPanel(title="Stock HTC Kernels", settings=self)  
    msg = GridLayout(cols=1, size_hint=(None, 0.8), width=700)
    btn_layout = GridLayout(cols=1)
    done = Button(text="Done")
    adv = Button(text='Show Custom Kernels',size_hint_y=(None), height=25)
    btn_layout.add_widget(done)
    msg.bind(minimum_height=msg.setter('height'))
    try:
        for name in htc:
            item = SettingItem(panel = panel, title = "%s" % name, disabled=False, desc = "https://github.com/wes342/%s" % name)
            item_btn = CustomButton(text="Clone:  %s" % name ,size_hint=(None, None),width=290, height=40)
            item.add_widget(item_btn)
            msg.add_widget(item)
        item_btn.bind(on_release=get_kernel) 
            
        root = ScrollView(size_hint=(None, None), size=(675, 350), do_scroll_x=False)
        root.add_widget(msg)
        Box.add_widget(adv)
        Box.add_widget(root)
        Box.add_widget(btn_layout)
        adv.bind(on_release=load_custom_ker)
        
        popup = Popup(background='atlas://images/eds/pop', title='Stock HTC Kernels',content=Box, auto_dismiss=True,
        size_hint=(None, None), size=(700, 500))
        done.bind(on_release=popup.dismiss)
        adv.bind(on_release=popup.dismiss)
        popup.open()
        
    except:
        EdsNotify().run("'system/app Directory Not Found", 'Cant Find:\n' + SystemApp)
        
def load_custom_ker(self):
    Box = BoxLayout(orientation="vertical", spacing=10)
    panel = SettingsPanel(title="Custom HTC Kernels", settings=self)  
    msg = GridLayout(cols=1, size_hint=(None, 0.8), width=700)
    btn_layout = GridLayout(cols=1)
    done = Button(text="Done")
    easy = Button(text='Show Stock Kernels',size_hint_y=(None), height=25)
    btn_layout.add_widget(done)
    msg.bind(minimum_height=msg.setter('height'))
    try:
        for name in kernels:
            item = SettingItem(panel = panel, title = "%s" % name, disabled=False, desc = "https://github.com/wes342/%s" % name)
            item_btn = CustomButton(text="Clone:  %s" % name ,size_hint=(None, None),width=250, height=40)
            item.add_widget(item_btn)
            msg.add_widget(item)
        item_btn.bind(on_release=get_kernel) 
            
        root = ScrollView(size_hint=(None, None), size=(675, 350), do_scroll_x=False)
        root.add_widget(msg)
        Box.add_widget(easy)
        Box.add_widget(root)
        Box.add_widget(btn_layout)
        easy.bind(on_release=load_ker)
        
        popup = Popup(background='atlas://images/eds/pop', title='Custom HTC Kernels',content=Box, auto_dismiss=True,
        size_hint=(None, None), size=(700, 500))
        done.bind(on_release=popup.dismiss)
        easy.bind(on_release=popup.dismiss)
        popup.open()
        
    except:
        EdsNotify().run("'system/app Directory Not Found", 'Cant Find:\n' + SystemApp)   

def get_kernel(self):
    kname = self.text.strip("Clone:  ")
    if os.path.exists("%s/Kernel" % EdsWorking):
        root = BoxLayout(orientation='vertical', spacing=20)
        btn_layout = GridLayout(cols=2, row_force_default=True, row_default_height=50, spacing=25)
        remove = Button(text='Continue', size_hint_x=None, width=150)
        cancel = Button(text='Cancel', size_hint_x=None, width=150)
        root.add_widget(Label(text='Kernel Files already Exist\nThis will overwrite old kernel files?'))
        root.add_widget(btn_layout)
        btn_layout.add_widget(remove)
        btn_layout.add_widget(cancel)
        popup = Popup(background='atlas://images/eds/pop', title='Notice',content=root, auto_dismiss=False,
        size_hint=(None, None), size=(350, 200))
        cancel.bind(on_release=popup.dismiss)
        def delete_ker(self):
            try:
                shutil.rmtree("%s/Kernel" % EdsWorking)
            except:
                print "kernel not found"
            try:
                shutil.rmtree("%s/Toolchain" % EdsWorking)
            except:
                print "Toolchain not found"
            import subprocess as sp
            os.chdir(Home)
            cmd = "gnome-terminal -t EDS-Shell -e \"git clone https://github.com/wes342/%s EDS_WORKING/Kernel\"" % kname
            sp.Popen(cmd, shell=True).wait()
            tool = "gnome-terminal -t EDS-Shell -e \"git clone https://github.com/wes342/android_prebuilt_toolchains EDS_WORKING/Toolchain\"" 
            sp.Popen(tool, shell=True).wait()
            mysource =  "%s/Toolchain" % EdsWorking
            mydest = "%s/Kernel" % EdsWorking
            try:
                for name in os.listdir(mysource):
                    src_file = os.path.join(mysource, name)
                    dst_file = os.path.join(mydest, name)
                    shutil.move(src_file, dst_file)
                try:
                    shutil.rmtree("%s/Toolchain" % EdsWorking)
                except:
                    print "Toolchain dir not found"
            except:
                print mysource + " or " + mydest + " Not Found "
        remove.bind(on_release=delete_ker)
        remove.bind(on_press=popup.dismiss)
        popup.open()
    else:
        import subprocess as sp
        os.chdir(Home)
        cmd = "gnome-terminal -t EDS-Shell -e \"git clone https://github.com/wes342/%s EDS_WORKING/Kernel\"" % kname
        sp.Popen(cmd, shell=True).wait()
        tool = "gnome-terminal -t EDS-Shell -e \"git clone https://github.com/wes342/android_prebuilt_toolchains EDS_WORKING/Toolchain\"" 
        sp.Popen(tool, shell=True).wait()
        mysource =  "%s/Toolchain" % EdsWorking
        mydest = "%s/Kernel" % EdsWorking
        try:
            for name in os.listdir(mysource):
                src_file = os.path.join(mysource, name)
                dst_file = os.path.join(mydest, name)
                shutil.move(src_file, dst_file)
            try:
                shutil.rmtree("%s/Toolchain" % EdsWorking)
            except:
                print "Toolchain dir not found"
        except:
            print mysource + " or " + mydest + " Not Found "


# Kernel Mods Selection popup
def kernel_mods(self):
    Box = BoxLayout(orientation="vertical", spacing=10)
    msg = GridLayout(cols=1, padding=15, spacing=10, size_hint_y=None)
    btn_layout = GridLayout(cols=1)
    done = Button(text="Done")
    btn_layout.add_widget(done)
    msg.bind(minimum_height=msg.setter('height'))
    
    over = CustomButton(text='OverClocking', size=(475, 40), size_hint=(None, None))
    over.bind(on_release=overclock)
    
    gpu = CustomButton(text='Gpu Overclock', size=(475, 40), size_hint=(None, None))
    gpu.bind(on_release=gpu_overclock)
    
    gov = CustomButton(text='Governors', size=(475, 40), size_hint=(None, None))
    gov.bind(on_release=gov_select)
    
    mhl = CustomButton(text='MHL Refresh Hack', size=(475, 40), size_hint=(None, None))
    mhl.bind(on_release=msl_options)
    
    msg.add_widget(over)
    msg.add_widget(gpu)
    msg.add_widget(gov)
    msg.add_widget(mhl)
    
    root = ScrollView(size_hint=(None, None),bar_margin=-22, size=(475, 390), do_scroll_x=False)
    root.add_widget(msg)
    Box.add_widget(root)
    Box.add_widget(btn_layout)
    
    popup = Popup(background='atlas://images/eds/pop', title='Kernel Mods',content=Box, auto_dismiss=True,
    size_hint=(None, None), size=(520, 500))
    done.bind(on_release=popup.dismiss)
    popup.open()

# Overclocking options for kernels
def overclock(self):
    layout = GridLayout(cols=1, size_hint=(None, 1.0), width=700)
    layout.bind(minimum_height=layout.setter('height'))
    panel = SettingsPanel(title="Kernel Base", settings=self)   
    main = BoxLayout(orientation = 'vertical')
    root = ScrollView(size_hint=(None, None),bar_margin=-11, bar_color=(47 / 255., 167 / 255., 212 / 255., 1.), do_scroll_x=False)
    root.size = (600, 400)
    root.add_widget(layout)
    main.add_widget(root)
    done = Button(text ='Done')
    main.add_widget(done)

    ghz15 = SettingItem(panel = panel, title = "1.5ghz", disabled=False, desc = "CONFIG_MSM_CPU_MAX_CLK_1DOT5GHZ")
    ghz15_radio = CheckBox(group="overclock", active=False)
    ghz15.add_widget(ghz15_radio)
    layout.add_widget(ghz15)
    
    ghz17 = SettingItem(panel = panel, title = "1.7ghz", disabled=False, desc = "CONFIG_MSM_CPU_MAX_CLK_1DOT7GHZ")
    ghz17_radio = CheckBox(group="overclock",active=False)
    ghz17.add_widget(ghz17_radio)
    layout.add_widget(ghz17)
    
    ghz18 = SettingItem(panel = panel, title = "1.8ghz", disabled=False, desc = "CONFIG_MSM_CPU_MAX_CLK_1DOT8GHZ")
    ghz18_radio = CheckBox(group="overclock",active=False)
    ghz18.add_widget(ghz18_radio)
    layout.add_widget(ghz18)
    
    ghz21 = SettingItem(panel = panel, title = "2.1ghz", disabled=False, desc = "CONFIG_MSM_CPU_MAX_CLK_2DOT1GHZ")
    ghz21_radio = CheckBox(group="overclock",active=False)
    ghz21.add_widget(ghz21_radio)
    layout.add_widget(ghz21)
            
    popup = Popup(background='atlas://images/eds/pop', title='Overclocking', content=main, auto_dismiss=True, size_hint=(None, None), size=(630, 500))
    done.bind(on_release=popup.dismiss)
    popup.open()

    def on_ghz15_active(checkbox, value):
        if value:
            print 'The checkbox', checkbox, 'is active'
        else:
            print 'The checkbox', checkbox, 'is inactive'
    ghz15_radio.bind(active=on_ghz15_active)
    
    def on_ghz17_active(checkbox, value):
        if value:
            print 'The checkbox', checkbox, 'is active'
        else:
            print 'The checkbox', checkbox, 'is inactive'
    ghz17_radio.bind(active=on_ghz17_active)
    
    def on_ghz18_active(checkbox, value):
        if value:
            print 'The checkbox', checkbox, 'is active'
        else:
            print 'The checkbox', checkbox, 'is inactive'
    ghz18_radio.bind(active=on_ghz18_active)
    
    def on_ghz21_active(checkbox, value):
        if value:
            print 'The checkbox', checkbox, 'is active'
        else:
            print 'The checkbox', checkbox, 'is inactive'
    ghz21_radio.bind(active=on_ghz21_active)

# Gpu Overclocking options
def gpu_overclock(self):
    layout = GridLayout(cols=1, size_hint=(None, 1.0), width=700)
    layout.bind(minimum_height=layout.setter('height'))
    panel = SettingsPanel(title="Gpu Overclocking", settings=self)   
    main = BoxLayout(orientation = 'vertical')
    root = ScrollView(size_hint=(None, None),bar_margin=-11, bar_color=(47 / 255., 167 / 255., 212 / 255., 1.), do_scroll_x=False)
    root.size = (600, 400)
    root.add_widget(layout)
    main.add_widget(root)
    done = Button(text ='Done')
    main.add_widget(done)

    sio = SettingItem(panel = panel, title = "Sio", disabled=False, desc = "CONFIG_IOSCHED_SIO")
    sio_radio = CheckBox(active=False)
    sio.add_widget(sio_radio)
    layout.add_widget(sio)
    
    vr = SettingItem(panel = panel, title = "VR", disabled=False, desc = "CONFIG_IOSCHED_VR")
    vr_radio = CheckBox(active=False)
    vr.add_widget(vr_radio)
    layout.add_widget(vr)
            
    popup = Popup(background='atlas://images/eds/pop', title='GPU Overclocking', content=main, auto_dismiss=True, size_hint=(None, None), size=(630, 500))
    done.bind(on_release=popup.dismiss)
    popup.open()
    
    def on_sio_active(checkbox, value):
        if value:
            print 'The checkbox', checkbox, 'is active'
        else:
            print 'The checkbox', checkbox, 'is inactive'
    sio_radio.bind(active=on_sio_active)
    
    def on_vr_active(checkbox, value):
        if value:
            print 'The checkbox', checkbox, 'is active'
        else:
            print 'The checkbox', checkbox, 'is inactive'
    vr_radio.bind(active=on_vr_active)

# Governors Selection menu
def gov_select(self):
    layout = GridLayout(cols=1, size_hint=(None, 1.0), width=700)
    layout.bind(minimum_height=layout.setter('height'))
    panel = SettingsPanel(title="Governors", settings=self)   
    main = BoxLayout(orientation = 'vertical')
    root = ScrollView(size_hint=(None, None),bar_margin=-11, bar_color=(47 / 255., 167 / 255., 212 / 255., 1.), do_scroll_x=False)
    root.size = (600, 400)
    root.add_widget(layout)
    main.add_widget(root)
    done = Button(text ='Done')
    main.add_widget(done)

    lion = SettingItem(panel = panel, title = "Lionhart", disabled=False, desc = "CONFIG_CPU_FREQ_GOV_LIONHEART")
    lion_radio = CheckBox(active=False)
    lion.add_widget(lion_radio)
    layout.add_widget(lion)
    
    inte = SettingItem(panel = panel, title = "Intellidemand", disabled=False, desc = "CONFIG_CPU_FREQ_GOV_INTELLIDEMAND")
    inte_radio = CheckBox(active=False)
    inte.add_widget(inte_radio)
    layout.add_widget(inte)
    
    zen = SettingItem(panel = panel, title = "Savanged Zen", disabled=False, desc = "CONFIG_CPU_FREQ_GOV_SAVAGEDZEN")
    zen_radio = CheckBox(active=False)
    zen.add_widget(zen_radio)
    layout.add_widget(zen)
    
    wax = SettingItem(panel = panel, title = "Brazillian Wax", disabled=False, desc = "CONFIG_CPU_FREQ_GOV_BRAZILLIANWAX")
    wax_radio = CheckBox(active=False)
    wax.add_widget(wax_radio)
    layout.add_widget(wax)
            
    popup = Popup(background='atlas://images/eds/pop', title='Governors', content=main, auto_dismiss=True, size_hint=(None, None), size=(630, 500))
    done.bind(on_release=popup.dismiss)
    popup.open()
    
    def on_lion_active(checkbox, value):
        if value:
            print 'The checkbox', checkbox, 'is active'
        else:
            print 'The checkbox', checkbox, 'is inactive'
    lion_radio.bind(active=on_lion_active)
    
    def on_inte_active(checkbox, value):
        if value:
            print 'The checkbox', checkbox, 'is active'
        else:
            print 'The checkbox', checkbox, 'is inactive'
    inte_radio.bind(active=on_inte_active)
    
    def on_zen_active(checkbox, value):
        if value:
            print 'The checkbox', checkbox, 'is active'
        else:
            print 'The checkbox', checkbox, 'is inactive'
    zen_radio.bind(active=on_zen_active)
    
    def on_wax_active(checkbox, value):
        if value:
            print 'The checkbox', checkbox, 'is active'
        else:
            print 'The checkbox', checkbox, 'is inactive'
    wax_radio.bind(active=on_wax_active)

# MSL Options (Not Sure What this is at this point)
def msl_options(self):
    pass

# Other Kernel options popup (Not Sure if we will need this its empty for now)
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

# Function to pull boot.img 
def pull_boot(self):
    root = BoxLayout(orientation='vertical', spacing=20)
    btn_layout = GridLayout(cols=1, row_force_default=True, row_default_height=50, spacing=15, padding=20)
    rom = Button(text='From imported rom', size_hint_x=None, width=300)
    device = Button(text='From your Device', size_hint_x=None, width=300)
    cancel = Button(text='Cancel', size_hint_x=None, width=300)
    root.add_widget(btn_layout)
    btn_layout.add_widget(rom)
    btn_layout.add_widget(device)
    btn_layout.add_widget(cancel)
    popup = Popup(background='atlas://images/eds/pop', title='Pull boot.img',content=root, auto_dismiss=False,
    size_hint=(None, None), size=(360, 275))
    cancel.bind(on_release=popup.dismiss)
    popup.open()
    
    def pull_boot_rom(self):
        from_rom(self)
    rom.bind(on_release=pull_boot_rom)
    rom.bind(on_release=popup.dismiss)
    
    def pull_boot_device(self):
        from_device(self)
    device.bind(on_release=pull_boot_device)
    device.bind(on_release=popup.dismiss)

def from_rom(self):
    print "pull from rom"
    
def from_device(self):
    print "pull from device"

# Main Kernel Menu
def kernel_menu(self):
    try:
        if (os.name == "posix" and platform.machine() == "x86_64"):
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
            k_base = CustomButton(text='Select Kernel Base', pos_hint={'x':.0, 'y':.550}, size_hint=(.90, .06))
            k_mods = CustomButton(text='Select Kernel Mods', pos_hint={'x':.0, 'y':.550}, size_hint=(.90, .06))
            b_img = CustomButton(text='Pull Boot.img', pos_hint={'x':.0, 'y':.550}, size_hint=(.90, .06))
            unpack = CustomButton(text='Unpack Boot.img', pos_hint={'x':.0, 'y':.550}, size_hint=(.90, .06))
            k_build = CustomButton(text='Build Kernel', pos_hint={'x':.0, 'y':.550}, size_hint=(.90, .06))
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
            grid_layout.add_widget(k_mods)
            grid_layout.add_widget(b_img)
            grid_layout.add_widget(unpack)
            grid_layout.add_widget(k_build)
            grid_layout.add_widget(k_other)
            
            def ker_type(instance):
                kernel_type(self)
            k_base.bind(on_release=ker_type)

            def ker_mods(instance):
                kernel_mods(self)
            k_mods.bind(on_release=ker_mods)
            
            def boot_img(instance):
                pull_boot(self)
            b_img.bind(on_release=boot_img)
            
            def ker_build(instance):
                print "build kernel"
            k_build.bind(on_release=ker_build)
    
            def ker_other(instance):
                kernel_other(self)
            k_other.bind(on_release=ker_other)
            
        else:
            self.panel_layout.clear_widgets()
            title = Label(text='[b][color=ff2222][size=20]Kernel Building[/size][/color][/b]', markup = True, pos_hint={'x':-.05, 'y':.20})
            lin = Label(text='[b][color=ffffff][size=15]You Must Be Using 64bit Ubuntu Based Linux to\nbuild Kernels 32bit and other distros will be added\nin later releases.[/size][/color][/b]', markup = True, pos_hint={'x':-.05, 'y':.0})
            self.panel_layout.add_widget(title)
            self.panel_layout.add_widget(lin)
            
        if package_count == 0:
            pass
        else:
            i_packages.bind(on_release=install_packages)
    except:
        no_os(self)
        
