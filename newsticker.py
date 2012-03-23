#!/usr/bin/env python

import sys
import getopt

import gtk
import gnomeapplet
import gobject

from widget import ScrolledTextWidget

PACKAGE = 'newsticker'
VERSION = '0.1'

def background_show(applet):
    print "background: ", applet.get_background()

def newsticker_factory(applet, iid):
    scroll = ScrolledTextWidget()
    applet.add(scroll)
    applet.show_all()
    gobject.timeout_add(1000, background_show, applet)
    return True

def newsticker_window():
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_title("NewsTicker")
    win.connect("destroy", gtk.main_quit)
    win.set_default_size(180, 20)
    applet = gnomeapplet.Applet()
    newsticker_factory(applet, None)
    applet.reparent(win)
    win.show_all()
    return win

def usage():
    print """Usage: newsticker [OPTIONS]

  OPTIONS:
  --help, -h            Print this help.
  --window, -w	        Launch the applet in a standalone window (default=no).
  """
    sys.exit()

if __name__ == "__main__":	
    standalone = False
	
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hw", ["help", "window"])
    except getopt.GetoptError:
        opts = []
        args = sys.argv[1:]
	
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-w", "--window"):
            standalone = True
	
    if standalone:
        import gnome
        gnome.init(PACKAGE, VERSION)
        newsticker_window()
        gtk.main()
    else:
        gnomeapplet.bonobo_factory('OAFIID:GNOME_NewsTicker_Factory', 
                                   gnomeapplet.Applet.__gtype__, 
                                   'newsticker',
                                   '0.1',
                                   newsticker_factory)
