import gobject
import pango
import gtk
from gtk import gdk

class ScrolledTextWidget(gtk.Widget):
    def __init__(self):
        gtk.Widget.__init__(self)
        self.__start = True
        self.set_font()
        self.set_text('Caio Eduardo Canestraro de Souza',
                      'Ana Julia Canestraro de Souza')
        # update once a 30 milisecond - time.sleep(0.010)
        gobject.timeout_add(30, self.do_redraw)

    def set_font(self, font='Sans', size=10):
        font = '%s %s' % (font, size)
        self._font = pango.FontDescription(font)

    def set_text(self, t, tt):
        self.p = self.create_pango_layout(t)
        self.p.set_font_description(self._font)
        self.pp = self.create_pango_layout(tt)
        self.pp.set_font_description(self._font)

    def do_realize(self):
        self.set_flags(self.flags() | gtk.REALIZED)
        self.window = gdk.Window(
            self.get_parent_window(),
            width=self.allocation.width,
            height=self.allocation.height,
            window_type=gdk.WINDOW_CHILD,
            wclass=gdk.INPUT_OUTPUT,
            event_mask=self.get_events() | gdk.EXPOSURE_MASK)
        self.window.set_user_data(self)
        self.style.attach(self.window)
        self.style.set_background(self.window, gtk.STATE_NORMAL)
        self.window.move_resize(*self.allocation)

    def do_unrealize(self):
        self.window.set_user_data(None)

    def do_size_request(self, requisition):
        width, height = self.p.get_size()
        requisition.width = 150 # Fixed width
        requisition.height = height // pango.SCALE

    def do_size_allocate(self, allocation):
        self.allocation = allocation
        if self.flags() & gtk.REALIZED:
            self.window.move_resize(*allocation)

    def do_expose_event(self, event):
        # Create first context
        c = self.window.cairo_create()
        c.rectangle(event.area.x, event.area.y,
                    event.area.width, event.area.height)
        c.clip()
        # Create second context
        cc = self.window.cairo_create()
        cc.rectangle(event.area.x, event.area.y,
                     event.area.width, event.area.height)
        cc.clip()
        fw, fh = self.p.get_pixel_size() # First text size
        fww, fhh = self.pp.get_pixel_size() # Second text size
        x, y, h, w = self.get_allocation() # Window size
        if self.__start:
            self.x = h
            self.y = 3 # Fixed value
            self.xx = h + fw + 5
            self.yy = self.y
        # First context
        c.move_to(self.x, self.y)
        c.update_layout(self.p)
        c.show_layout(self.p)
        # Second context        
        cc.move_to(self.xx, self.yy)
        cc.update_layout(self.pp)
        cc.show_layout(self.pp)
        if self.x == -fw:
            self.x = self.xx + fww + 5
        elif self.xx == -fw:
            self.xx = self.x + fw + 5
        else:
            self.x = self.x - 1
            self.xx = self.xx - 1
            self.__start = False

    def do_redraw(self):
        if self.window:
            alloc = self.get_allocation()
            rect = gdk.Rectangle(alloc.x, alloc.y, alloc.width, alloc.height)
            self.window.invalidate_rect(rect, True)
            self.window.process_updates(True)
        # keep running this event
        return True
gobject.type_register(ScrolledTextWidget)
