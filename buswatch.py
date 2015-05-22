from gi.repository import GLib
from gi.repository import Gio

def callback(conn, sender, obj, iface, signal, value):
    obj_changed, properties, args = value
    print(obj_changed, properties)
    return None

conn = Gio.bus_get_sync(Gio.BusType.SESSION)

#print (conn.init())

conn.signal_subscribe(
    'org.mpris.MediaPlayer2.vlc',
    'org.freedesktop.DBus.Properties',
    'PropertiesChanged',
    '/org/mpris/MediaPlayer2',
    None,
    Gio.DBusSignalFlags.NONE,
    callback)



loop = GLib.MainLoop()
loop.run()
