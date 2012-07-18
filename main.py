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
import kivy
kivy.require('1.2.0')

from kivy.app import App
from kivy.config import ConfigParser
from kivy.config import Config
from scripts.GI import *


from scripts.Adb import *
from scripts.Fastboot import *
from scripts.Apk import *
from scripts.Base import *
from scripts.About import *
from scripts.Misc import *
from scripts.Cm7Bloat import *
from scripts.SenseBloat import *
from scripts.RomOther import *
from scripts.settings_panel import *
from scripts.CamMods import *
from scripts.FrameMods import *
from scripts.script import *
from scripts.source import *



class Background(Image):
    pass

class TextInput(Widget):
    pass

# CREATE MAIN MENU
class MainMenu(Widget):
    app = ObjectProperty(None)
    text_input = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.background = Background(source=(Bg))
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.adb_menu = AdbMenu(app=self)
        self.fastboot_menu = FastbootMenu(app=self)
        self.apk_menu = ApkMenu(app=self)
        self.rom_menu = RomMenu(app=self)
        self.about_menu = AboutMenu(app=self)
        self.source = Source(app=self)
        
    def do_adb_action(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(self.adb_menu)
        
        
    def do_fastboot_action(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(self.fastboot_menu)
        
    def do_apk_action(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(self.apk_menu)
        
    def do_about_action(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(self.about_menu)

    def do_rom_action(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(self.rom_menu)
        
    def do_misc_action(self):
        pass
        
    def do_source_action(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(self.source)
        
    def get_text_action(self):
        comm = self.text_input.text
        output = os.popen(comm).read()
        print output
        self.text_input.text = ''
        try:
            import pynotify
            if pynotify.init(NAME):
                n = pynotify.Notification("Shell Command Output", output)
                n.set_urgency(pynotify.URGENCY_NORMAL)
                n.show()
            else:
                print "there was a problem initializing the 'pynotify' module"
        except:
            print "you don't seem to have 'pynotify' installed" 
        
    def do_main_help_action(self):
        pass
        
    def open_settings(self):
        # is called from the rightmost button (the "setup" button") --> function call binding in the .kv file
        self.app.open_settings()
                      
# CREATE ADB MENU
class AdbMenu(Widget):
    app = ObjectProperty(None)
    pull_text = ObjectProperty(None)
    push_text = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(AdbMenu, self).__init__(**kwargs)
        self.background = Background(source=(Bg))
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        
    def close_adb_menu(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(MainMenu(app=self))
   
    def do_push_action(self):
        adb_push(self)
        
    def adb_push_location(self):
        push_path(self)
                
    def do_pull_action(self):
        adb_pull(self)
        
    def do_adb_help_action(self):
        adb_help(self)
        
    def adb_text_action(self):
        adb_run(self)
        
    def adb_commands(self):
        adb_comm(self)
        
    def dismiss_popup(self):
        dismiss(self)
             
    def show_load(self):
        show_adb_browse(self)

    def load(self, path, filename):
        select_adb_file(self, path, filename)
        
    def open_settings(self):
        self.app.open_settings()
           
# CREATE FASTBOOT MENU
class FastbootMenu(Widget):
    app = ObjectProperty(None) 
    def __init__(self, **kwargs):
        super(FastbootMenu, self).__init__(**kwargs)
        self.background = Background(source=(Bg))
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        
    def close_fastboot_menu(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(MainMenu(app=self))
        
    def do_boot_action(self):
        flash_boot(self)
    
    def do_rec_action(self):
        boot_recovery(self)
        
    def do_fastboot_help_action(self):
        fastboot_help(self)
        
    def fastboot_text_action(self):
        fastboot_run(self)
        
    def fastboot_commands(self):
        fastboot_comm(self)
    
    def reboot_fastboot(self):
        go_fastboot(self)
     
    def dismiss_popup(self):
        dismiss(self)
             
    def show_load(self):
        show_fb_browse(self)

    def load(self, path, filename):
        select_fb_file(self, path, filename)  

    def open_settings(self):
        self.app.open_settings() 
   
# CREATE APK MENU       
class ApkMenu(Widget):
    app = ObjectProperty(None)    
    def __init__(self, **kwargs):
        super(ApkMenu, self).__init__(**kwargs)
        self.background = Background(source=(Bg))
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        
    def close_apk_menu(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(MainMenu(app=self))
        
    def do_clean_action(self):
        clean_working(self)
        
    def do_install_action(self):
        install_framework(self)
        
    def do_dec_apk_action(self):
        dec_apk(self)
        
    def do_rec_apk_action(self):
        rec_apk(self)
        
    def do_sign_action(self):
        sign(self)
        
    def do_source_action(self):
        source(self)
        
    def do_sign_other_action(self):
        sign_misc(self)
        
    def do_draw9_action(self):
        draw9_patch(self)
        
    def do_dec_dex_action(self):
        dec_dex(self)
        
    def do_rec_dex_action(self):
        rec_dex(self)
        
    def do_apk_help_action(self):
        apk_help(self)
        
    def apk_text_action(self):
        apk_run(self)
 
    def open_settings(self):
        self.app.open_settings()        
 
# CREATE ROM MENU       
class RomMenu(Widget):
    app = ObjectProperty(None)  
    def __init__(self, **kwargs):
        super(RomMenu, self).__init__(**kwargs)
        self.background = Background(source=(Bg))
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.base_menu = BaseRom(app=self)
        self.bloat_menu = Bloatware(app=self)
        self.script_menu = ScriptMenu(app=self)
        self.rom_other = RomOther(app=self)
        self.mods_menu = ModsMenu(app=self)
        
    def close_rom_menu(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(MainMenu(app=self))
        
    def do_rom_base_action(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(self.base_menu)
        
    def do_bloat_action(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(self.bloat_menu)

    def do_add_apps_action(self):
        pass
        
    def do_mod_apps_action(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(self.mods_menu)
        
    def do_theme_action(self):
        pass
        
    def do_tweaks_action(self):
        pass
    
        
    def do_script_action(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(self.script_menu)

    
    def do_other_action(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(self.rom_other)

    def do_rom_help_action(self):
        pass

    
    def open_settings(self):
        self.app.open_settings() 
     
        
class RomOther(Widget):
    app = ObjectProperty(None)
    main_layout = ObjectProperty(None)
    other_box_layout = ObjectProperty(None)
    other_scroll_view = ObjectProperty(None)
    other_grid_layout = ObjectProperty(None)
    panel_layout = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(RomOther, self).__init__(**kwargs)
        self.background = Background(source=(Bg))
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        
    def close_rom_other_menu(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(RomMenu(app=self))         
    
    def do_aroma_action(self):
        if os.path.exists(Aroma) == True:
            aroma(self)
        else: 
            try:
                import pynotify
                if pynotify.init(NAME):
                    n = pynotify.Notification("Aroma Files Not Found", "\nYou Need To install Aroma From Base Rom Menu")
                    n.set_urgency(pynotify.URGENCY_LOW)
                    n.show()
                else:
                    print "there was a problem initializing the 'pynotify' module"
            except:
                print "you don't seem to have 'pynotify' installed"

    def do_boot_img_action(self):
        boot_img(self)
        
    def do_build_kernel_action(self):
        build_kernel(self)
               
    def do_deodex_action(self):
        deodex(self)
    
    def do_odex_action(self):
        odex(self)

    def do_rom_other_help_action(self):
        pass

    def open_settings(self):
        self.app.open_settings() 

class ModsMenu(Widget):
    app = ObjectProperty(None) 
    def __init__(self, **kwargs):
        super(ModsMenu, self).__init__(**kwargs)
        self.background = Background(source=(Bg))
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))       
        
    def close_mods_menu(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(RomMenu(app=self))  
    
    def system_mods(self):
        sys_mods(self)
        
    def framework_mods(self):
        frame_mods(self)
        
    def settings_mods(self):
        sett_mods(self)
        
    def browser_mods(self):
        browse_mods(self)
        
    def camera_mods(self):
        cam_mods(self)
        
    def sound_mods(self):
        audio_mods(self)
        
    def messaging_mods(self):
        mms_mods(self)
        
    def other_mods(self):
        misc_mods(self)
        
    def do_mod_help_action(self):
        pass
          
    def open_settings(self):
        self.app.open_settings() 
        
class ScriptMenu(Widget):
    app = ObjectProperty(None) 
    def __init__(self, **kwargs):
        super(ScriptMenu, self).__init__(**kwargs)
        self.background = Background(source=(Bg))
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))       
        
    def close_script_menu(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(RomMenu(app=self))  
    
    def changelog(self):
        changes(self)
        
    def aroma_cfg(self):
        aroma_config(self)
        
    def do_script_help_action(self):
        pass
    
    def open_settings(self):
        self.app.open_settings() 
  
          
# CREATE BASE MENU       
class BaseRom(Widget): 
    app = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(BaseRom, self).__init__(**kwargs)
        self.background = Background(source=(Bg))
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        
    def close_base_menu(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(RomMenu(app=self))

    def do_select_base_action(self):
        select_base(self)
        
    def do_aroma_action(self):
        add_aroma(self)

    def do_boot_scripts_action(self):
        boot_scripts(self)
    
    def do_transition_action(self):
        trans_scripts(self)
        
    def do_boot_img_action(self):
        boot_img(self)

    def do_boot_anims_action(self):
        boot_anims(self)

    def open_settings(self):
        self.app.open_settings()

    def show_load(self):
        show_base_browse(self)
        
    def load(self, path, filename):
        select_base_file(self, path, filename)

    def dismiss_popup(self):
        dismiss(self)

    def do_base_help_action(self):
        pass   
        
# CREATE BLOATWARE MENU       
class Bloatware(Widget): 
    app = ObjectProperty(None)   
    def __init__(self, **kwargs):
        super(Bloatware, self).__init__(**kwargs)
        self.background = Background(source=(Bg))
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))       
        self.cm7_bloat_menu = Cm7Bloat(app=self)
        self.sense_bloat_menu = SenseBloat(app=self)

    def close_bloat_menu(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(RomMenu(app=self))

    def do_cm7_bloat_action(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(self.cm7_bloat_menu)

    def do_sense_bloat_action(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(self.sense_bloat_menu)
        
    def do_bloat_help_action(self):
        pass
        
    def open_settings(self):
        self.app.open_settings()
                
             
# CREATE CM7 BLOAT MENU       
class Cm7Bloat(Widget): 
    app = ObjectProperty(None)    
    def __init__(self, **kwargs):
        super(Cm7Bloat, self).__init__(**kwargs)
        self.background = Background(source=(Bg))
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))       
        
    def close_cm7_bloat_menu(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(Bloatware(app=self))

    def do_rm_adw(self):
        rm_adw(self)
        
    def do_rm_dsp(self):
        rm_dsp(self)
        
    def do_rm_spareparts(self):
        rm_spareparts(self)
        
    def do_rm_androidian(self):
        rm_androidian(self)
        
    def do_rm_file_manager(self):
        rm_file_manager(self)
    
    def do_rm_theme_chooser(self):
        rm_theme_chooser(self)
        
    def do_rm_term(self):
        rm_term(self)
        
    def do_rm_live_walls(self):
        rm_live_walls(self)
        
    def do_rm_theme_manager(self):
        rm_theme_manager(self)
    
    def do_rm_cm_parts(self):
        rm_cm_parts(self)
        
    def do_rm_live_picker(self):
        rm_live_picker(self)
        
    def do_rm_torch(self):
        rm_torch(self)
        
    def do_rm_screenshot(self):
        rm_screenshot(self)
    
    def do_rm_smoke_walls(self):
        rm_smoke_walls(self)
        
    def do_rm_vis_walls(self):
        rm_vis_walls(self)
        
    def do_rm_cm_stats(self):
        rm_cm_stats(self)
        
    def do_rm_protips(self):
        rm_protips(self)
        
    def do_rm_cm_update(self):
        rm_cm_update(self)    
    
    def do_rm_search_box(self):
        rm_search_box(self)
        
    def do_rm_cm_walls(self):
        rm_cm_walls(self)
        
    def do_rm_rom_manager(self):
        rm_rom_manager(self)
    
    def do_rm_cyanobread(self):
        rm_cyanobread(self)
    
    def do_rm_sound_rec(self):
        rm_sound_rec(self)
    
    def do_clean_removed(self):
        clean_removed(self)
        
    def do_restore_removed(self):
        restore_removed(self)
        
    def do_cm7_bloat_help_action(self):
        pass
        
    def open_settings(self):
        self.app.open_settings()   
    
# CREATE SENSE BLOAT MENU       
class SenseBloat(Widget): 
    app = ObjectProperty(None)  
    def __init__(self, **kwargs):
        super(SenseBloat, self).__init__(**kwargs)
        self.background = Background(source=(Bg))
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))       
        
    def close_sense_bloat_menu(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(Bloatware(app=self))

    def do_rm_adobe(self):
        rm_adobe(self)
        
    def do_rm_amazon(self):
        rm_amazon(self)
        
    def do_rm_app_share(self):
        rm_app_share(self)
        
    def do_rm_blockbuster(self):
        rm_blockbuster(self)
        
    def do_rm_bluesky(self):
        rm_bluesky(self)
    
    def do_rm_burgandy(self):
        rm_burgandy(self)
        
    def do_rm_dcs(self):
        rm_dcs(self)
        
    def do_rm_field(self):
        rm_field(self)
        
    def do_rm_flickr(self):
        rm_flickr(self)
    
    def do_rm_hornet(self):
        rm_hornet(self)
        
    def do_rm_car_pannel(self):
        rm_car_pannel(self)
        
    def do_rm_direct(self):
        rm_direct(self)
        
    def do_rm_feedback(self):
        rm_feedback(self)
    
    def do_rm_sync_provider(self):
        rm_sync_provider(self)
        
    def do_rm_streak(self):
        rm_streak(self)
        
    def do_rm_weather_wall(self):
        rm_weather_wall(self)
        
    def do_rm_smoke_wall(self):
        rm_smoke_wall(self)
        
    def do_rm_mode_10(self):
        rm_mode_10(self)  
    
    def do_rm_mspot(self):
        rm_mspot(self)
        
    def do_rm_my_htc(self):
        rm_my_htc(self)
        
    def do_rm_my_report(self):
        rm_my_report(self)
    
    def do_rm_nscm(self):
        rm_nscm(self)
    
    def do_rm_asset(self):
        rm_asset(self)
        
    def do_rm_picasa(self):
        rm_picasa(self)
        
    def do_rm_poloris(self):
        rm_poloris(self)
        
    def do_rm_qik(self):
        rm_qik(self)
    
    def do_rm_lookup(self):
        rm_lookup(self)        
    
    def do_rm_qxdm(self):
        rm_qxdm(self)       
    
    def do_rm_guide(self):
        rm_guide(self)
    
    def do_rm_smith(self):
        rm_smith(self)
    
    def do_rm_spidy(self):
        rm_spidy(self)
    
    def do_rm_installer(self):
        rm_installer(self)
    
    def do_rm_wallet(self):
        rm_wallet(self)
    
    def do_rm_nav(self):
        rm_nav(self)
    
    def do_rm_tv(self):
        rm_tv(self)        
    
    def do_rm_zone(self):
        rm_zone(self)
    
    def do_rm_stock(self):
        rm_stock(self)       
    
    def do_rm_vis_wall(self):
        rm_vis_wall(self)
    
    def do_rm_weather_live(self):
        rm_weather_live(self)
                               
    def do_clean_removed(self):
        clean_removed(self)
        
    def do_restore_removed(self):
        restore_removed(self)
        
    def do_sense_bloat_help_action(self):
        pass
        
    def open_settings(self):
        self.app.open_settings() 
         
# CREATE MISC MENU
class MiscMenu(Widget):
    app = ObjectProperty(None)  
    def __init__(self, **kwargs):
        super(MiscMenu, self).__init__(**kwargs)
        self.background = Background(source=(Bg))
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        
    def close_Misc_menu(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(MainMenu(app=self))
       
    def open_settings(self):
        self.app.open_settings() 
        
                
# CREATE OTHER MENU       
class Source(Widget):
    app = ObjectProperty(None)  
    def __init__(self, **kwargs):
        super(Source, self).__init__(**kwargs)
        self.background = Background(source=(Bg))
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        
    def close_source_menu(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(MainMenu(app=self))

    def do_source_action(self):
        source_menu(self)
        
    def do_kernel_action(self):
        os_detect(self)

    def open_settings(self):
        self.app.open_settings()
           
# CREATE ABOUT MENU            
class AboutMenu(Widget):
    app = ObjectProperty(None) 
    def __init__(self, **kwargs):
        super(AboutMenu, self).__init__(**kwargs)
        self.background = Background(source=(Bg))
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        
    def close_about_menu(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.background, index=len(self.main_layout.children))
        self.main_layout.add_widget(MainMenu(app=self))
        
    def do_site_action(self):
        show_site(self)
        
    def do_twitter_action(self):
        show_twitter(self)
        
    def do_forum_action(self):
        show_forum(self)
        
    def do_bugs_action(self):
        show_bugs(self)
        
    def do_credits_action(self):
        credits_popup(self)

    def open_settings(self):
        self.app.open_settings()


# MAIN APP CLASS       
class EdsApp(App):
    title = NAME
    def build(self):
        mkworking(self)
        mkusr_fs(self)
        self.use_kivy_settings = False
        #Builder.load_file('%s/eds.kv' % (Usr)) 
        self.main_menu = MainMenu(app=self)
        return self.main_menu 
    
    def get_application_config(self):
        return os.path.expanduser('~/.easydevstudio/eds.ini')
    
        
    def build_config(self, config):
        #Settings Default EDS config settings  
        Config.set('kivy', 'window_icon', Icon)
        Config.set('input', 'mouse', 'mouse,disable_multitouch') 
        config.adddefaultsection('Themes')
        config.setdefault('Themes', 'file_layout', 'List View')
        config.setdefault('Themes', 'selected', 'Stock')
        config.setdefault('Themes', 'usr_themes', 'None')
        config.setdefault('Themes', 'browse_themes', '%s' % Home)
        config.setdefault('Themes', 'wallpaper', '%s' % Home)
        
        config.adddefaultsection('Config')
        config.setdefault('Config', 'uname', '%s' % You)
        config.setdefault('Config', 'email', '')
        config.setdefault('Config', 'repo_dir', '%s/bin' % Home)
        config.setdefault('Config', 'rm_config', '')
        config.setdefault('Config', 'logging', '1')       
        config.setdefault('Config', 'log_dir', 'logs')
        config.setdefault('Config', 'log_level', 'Info')
        config.setdefault('Config', 'multitouch', '1')
        
        if config.getint('Config', 'multitouch') == 1:
            Config.setdefault('input', 'mouse', 'mouse,disable_multitouch')

        
        config.adddefaultsection('System Info')
        config.setdefault('System Info', 'version', '%s' % VERSION)
        config.setdefault('System Info', 'me', '%s' % You)       
        config.setdefault('System Info', 'usr_os', '%s' % platform.system())
        config.setdefault('System Info', 'arch', '%s' % platform.machine())
        config.setdefault('System Info', 'py', '%s' % platform.python_version())
        config.setdefault('System Info', 'py_type', '%s' % platform.python_implementation())
        
        config.adddefaultsection('Register')
        config.setdefault('Register', 'reg_name', '')
        config.setdefault('Register', 'reg_key', '')
 
           
    def build_settings(self, settings):
        settings.add_json_panel('Themes', self.config, '%s/themes.json' % Conf)
        settings.add_json_panel('Config', self.config, '%s/config.json' % Conf)
        settings.add_json_panel('System Info', self.config, '%s/info.json' % Conf)
        settings.add_json_panel('Register', self.config, '%s/register.json' % Conf)      

    def on_config_change(self, config, section, key, value):
        token = (section, key, value)
        
        if token == ('Register', 'reg_name', value):
            name(self, value)
            
        elif token == ('Register', 'reg_key', value):
            reg(self, value)
        
        if token == ('Themes', 'file_layout', 'ListView'):
            list_view(self)
            
        elif token == ('Themes', 'file_layout', 'Icon View'):
            icon_view(self)
                
        if token == ('Themes', 'selected', 'Stock'):
            ins_stock_theme(self)
            
        elif token == ('Themes', 'selected', 'Red'):
            ins_red_theme(self)
            
        elif token == ('Themes', 'selected', 'Blue'):
            ins_blue_theme(self)
            
        if token == ('Themes', 'usr_themes', "Joe's"):
            ins_joes_theme(self)
            
        elif token == ('Themes', 'selected', "Tom's"):
            ins_toms_theme(self)

        # TODO Error when selecting option for second time
        # OSError: [Errno 20] Not a directory:
        # Still returns correct value: Issue with kivys path implimentation in settings
        
        if token == ('Themes', 'browse_themes', value):
            destpath = '%s' % (Usr)
            z = zipfile.ZipFile(value)
            z.extractall(destpath)
            restart(self)
            config.set('Themes', 'selected', 'Custom')
            config.write()
            config.set('Themes', 'browse_themes', '%s' % Home)
            config.write()
               
        # TODO Error when selecting option for second time
        # OSError: [Errno 20] Not a directory:
        # Still returns correct value: Issue with kivys path implimentation in settings
        
        if token == ('Themes', 'wallpaper', value):
            shutil.copy(value, '%s/background.jpg' % Usr)
            restart(self)
            config.set('Themes', 'selected', 'Custom')
            config.write()
            config.set('Themes', 'wallpaper', '%s' % Home)
            config.write()           

        if token == ('Config', 'rm_config', 'eds.ini'):
            print 'eds.ini has been removed'
            os.remove('%s/eds.ini' % Usr)
            
        # Logging Options To control kivy logging

        if token == ('Config', 'logging', '1'):
            Config.set('kivy', 'log_enable', '1')
            Config.write()
        elif token == ('Config', 'logging', '0'):
            Config.set('kivy', 'log_enable', '0')
            Config.write()
            
        if token == ('Config', 'log_level', 'Trace'):
            Config.set('kivy', 'log_level', 'trace')
            Config.write()
        elif token == ('Config', 'log_level', 'Debug'):
            print 'Log More'
            Config.set('kivy', 'log_level', 'debug')
            Config.write()    
        elif token == ('Config', 'log_level', 'Info'):
            Config.set('kivy', 'log_level', 'info')
            Config.write()
        elif token == ('Config', 'log_level', 'Warning'):
            print 'Log More'
            Config.set('kivy', 'log_level', 'warning')
            Config.write()
        elif token == ('Config', 'log_level', 'Error'):
            Config.set('kivy', 'log_level', 'error')
            Config.write()
        elif token == ('Config', 'log_level', 'Critical'):
            print 'Log More'
            Config.set('kivy', 'log_level', 'critical')
            Config.write()
        
            
        if token == ('Config', 'log_dir', 'logs'):
            Config.set('kivy', 'log_dir', '/home/wes/Desktop')
            Config.write()
            
        elif token == ('Config', 'log_dir', value):
            Config.set('kivy', 'log_dir', value)
            Config.write()
            
        if token == ('Config', 'multitouch', '1'):
            Config.set('input', 'mouse', 'mouse,disable_multitouch')
            Config.write() 
            
        elif token == ('Config', 'multitouch', '0'):
            Config.set('input', 'mouse', 'mouse')
            Config.write() 
     

if __name__ == '__main__':
    EdsApp().run()
    Config.set('kivy', 'window_icon', '')
    Config.write()
