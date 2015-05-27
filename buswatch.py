from gi.repository import GLib
from gi.repository import Gio
from datetime import datetime
from time import time
import json


class Log():
    def __init__(self, url, metadata, timestamp=None):
        if timestamp is None:
            self.timestamp = time()
        else:
            self.timestamp = timestamp
        
        self.url = url
        self.metadata = metadata
        
    def __repr__(self):
        attrs = vars(self)
        attrs['creation_date'] = datetime.utcnow().isoformat()
        return str(attrs)
        
    def serialize(self):
        return json.dumps({
                'metadata': self.metadata,
                'creation_date': datetime.utcnow().isoformat()
            })
        
        
logged = None
timer_id = -1

def log(data):
    print ('LOGGING', data.serialize())
    return False


def callback(conn, sender, obj, iface, signal, value):
    global logged
    global timer_id
    obj_changed, properties, args = value
    print ('DEBUG', properties)
    if 'Metadata' in properties:
        url = properties['Metadata']['xesam:url']
        duration = properties['Metadata']['vlc:time']
        metadata = properties['Metadata']

        now = time()
        
        if logged is None:
            assert timer_id == -1, 'logged is None. Timer Id should be -1'
            logged = Log(url, metadata)
            timer_id= GLib.timeout_add_seconds(int(.5*duration), log, logged)
            
        elif logged.url == url:
            lapse = now - logged.timestamp
            if lapse > .5 * duration:
                log(logged)
                logged = None
                if timer_id > -1:
                    GLib.source_remove(timer_id)
                    timer_id = -1
            else:    
                delta = int(.5 * duration) - lapse
            
                if timer_id > -1:
                    GLib.source_remove(timer_id)
            
                timer_id= GLib.timeout_add_seconds(delta, log, logged)
        else:
            lapse = now - logged.timestamp
            if lapse > .5 * duration:
                log(logged)
                logged = Log(url, metadata)
                if timer_id > -1:
                    GLib.source_remove(timer_id)
                timer_id= GLib.timeout_add_seconds(int(.5*duration), log, logged)

    return None
   

conn = Gio.bus_get_sync(Gio.BusType.SESSION)

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
