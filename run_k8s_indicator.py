#!/usr/bin/env python3
from kubernetes import client, config
import subprocess
import os
import signal
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3
currpath = os.path.dirname(os.path.realpath(__file__))

class Indicator():
    def __init__(self):
        self.app = 'k8s_context_switcher'
        iconpath = currpath+"/icon.png"
        self.indicator = AppIndicator3.Indicator.new(
            self.app, iconpath,
            AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
    def refresh_menu(self):
        # k8s cluster 
        self.menu = Gtk.Menu()
        contexts, current = self.list_contexts()
        for c in contexts:
            if c['name'] == current['name']:
                c['name'] = '* ' + c['name']
            menu_item = Gtk.MenuItem(c['name'].strip())
            menu_item.connect("activate", self.run_script, c['name'])
            self.menu.append(menu_item)            
    def create_menu(self):
        self.menu = Gtk.Menu()
        self.refresh_menu()
        # quit
        item_quit = Gtk.MenuItem('Quit')
        sep = Gtk.SeparatorMenuItem()
        self.menu.append(sep)
        item_quit.connect('activate', self.stop)
        self.menu.append(item_quit)
        self.menu.show_all()
        return self.menu
    def run_script(self, widget, context):
        self.change_context(context)
        self.indicator.set_menu(self.create_menu())
    def stop(self, source):
        Gtk.main_quit()
    
    def change_context(self,context):
        subprocess.check_output(['kubectl', 'config','use-context', context])

    def list_contexts(self):
        config.load_kube_config()
        contexts , current = config.list_kube_config_contexts()
        return contexts, current 
                
Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()