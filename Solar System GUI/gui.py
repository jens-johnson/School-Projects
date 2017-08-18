'''
gui.py: An interactive model of the solar system that utilizes TKinter and an input
text file to allow the user to simulate orbital rotations

Author(s): Christopher Jens Johnson
Credit(s): Professor John Conery, University of Oregon
'''

from Orbits import *

IPython = (__doc__ is not None) and ('IPython' in __doc__)
Main    = __name__ == '__main__'

if IPython:
    get_ipython().magic('gui tk')

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from time import sleep



# File Input
def read_bodies(filename, cls):
    '''
    Read descriptions of planets, return a list of body objects.  The first
    argument is the name of a file with one planet description per line, the
    second argument is the type of object to make for each planet.
    '''
    if not issubclass(cls, Body):
        raise TypeError('cls must be Body or a subclass of Body')

    bodies = [ ]

    with open(filename) as bodyfile:
        for line in bodyfile:
            line = line.strip()
            if len(line) == 0 or line[0] == '#':
                continue
            name, m, rx, ry, rz, vx, vy, vz, diam, color = line.split()
            args = {
                'mass' : float(m),
                'position' : Vector(float(rx), float(ry), float(rz)),
                'velocity' : Vector(float(vx), float(vy), float(vz)),
            }
            opts = {'name': name, 'color': color, 'size': int(diam)}
            for x in opts:
                if getattr(cls, x, None):
                    args[x] = opts[x]
            bodies.append(cls(**args))

    return bodies


# Graphics celestial body object
class TkBody(Body):
    def __init__(self, mass, position, velocity, name, size, color):
        Body.__init__(self, mass, position, velocity, name)
        self._size = size
        self._color = color
        self._graphic = None
    def size(self):
        return self._size
    def color(self):
        return self._color
    def graphic(self):
        return self._graphic
    def set_graphic(self,arg):
        self._graphic = arg

# Canvas object for the solar system
class SolarSystemCanvas(tk.Canvas):
    
    def __init__(self, parent, height=600, width=600):
        tk.Canvas.__init__(self, parent, height=height, width=width, background='gray90', highlightthickness=0)
        self._planets = None
        self._outer = None
        self._scale = None
        self._offset = Vector(int(self['width'])/2, int(self['height'])/2, 0)
        
    def set_planets(self, lst):
        self._planets = lst
        self._outer = len(lst)
        self._compute_scale(lst)
        self.view_planets(len(lst))
        
    def view_planets(self, n):
        self.delete("all")
        self._compute_scale(self._planets[:n])
        for i in range(n):
            x=(self._planets[i].position().x() * self._scale)+self._offset.x()
            y=(self._planets[i].position().y() * self._scale)+self._offset.y()
            obj = self.create_oval(x-self._planets[i].size(),y+ self._planets[i].size(),x + self._planets[i].size(),y- self._planets[i].size(),fill=self._planets[i].color())
            self._planets[i].set_graphic(obj)
        
    def move_planets(self, lst):
        for planet in lst[:self._outer]:
            currx,curry = self._current_loc(planet)
            newx,newy = self._compute_loc(planet)
            disx = newx - currx
            disy = newy - curry
            self.move(planet._graphic,disx,disy)
            self.create_line(currx,curry,newx,newy)
        
    def _compute_scale(self, bodies):
        width = int(self['width'])
        height = int(self['height'])
        p = min(width, height)
        norm_list = [ body._position.norm() for body in bodies ]
        dmax = 1.1 * max(norm_list)
        scale = (p/2) / (abs(dmax))
        self._scale = scale
    
    def _compute_loc(self, p):
        pos = p.position() * self._scale + self._offset
        return pos.x(), pos.y()
    
    def _current_loc(self, p):
        ul, ur, _, _ = self.coords(p.graphic())
        return ul + p.size(), ur + p.size()
    



# TKinter view control element
class ViewControl(tk.Frame):
    
    def __init__(self, parent, callback):
        tk.Frame.__init__(self, parent)
        
        self['width'] = 100             
        self['height'] = 25             
        self['background'] = 'gray'     
        
        self.view = tk.Label(self,text="View: ")
        self.view.grid(row=0,column=0)
        self._spinbox = tk.Spinbox(self,state="disabled",command=callback)
        self._spinbox.grid(row=0,column=1)

    def reset(self, nbodies):
        self._spinbox.config(from_=2,to=nbodies,state="normal")
        self._spinbox.delete(0)
        self._spinbox.insert(0,nbodies)
        
    def nbodies(self):
        if isinstance(self._spinbox.get(), str):
            return int(self._spinbox.get())
        return 0


# TKinter frame element
class RunFrame(tk.Frame):
    
    def __init__(self, parent, callback):
        tk.Frame.__init__(self, parent)
        
        self['width'] = 200
        self['height'] = 100
        self['background'] = 'gray'
        
        self._dt_entry = tk.Entry(self)
        self._dt_entry.pack()
        self._dt_entry.insert(0,'86459')
        
        self._nsteps_entry = tk.Entry(self)
        self._nsteps_entry.pack()
        self._nsteps_entry.insert(0,'365')
        
        self._run_button = tk.Button(self,text='Run',command=callback)
        self._run_button.pack()
        
        self._progress = ttk.Progressbar(self,orient='horizontal')
        self._progress.pack()
        
    def dt(self):
        return int(self._dt_entry.get())
    
    def nsteps(self):
        return int(self._nsteps_entry.get())
        
    def init_progress(self, n):
        self._progress['maximum'] = n
        
    def update_progress(self, n):
        self._progress['value'] += n
        
    def clear_progress(self):
        self._progress['value'] = 0



root = tk.Tk()
root.title("Solar System")

bodies = None

def load_cb():
    global bodies
    fn = tk.filedialog.askopenfilename()
    bodies = read_bodies(fn, TkBody)
    canvas.set_planets(bodies)
    view_count.reset(len(bodies))

def view_cb():
    canvas.view_planets(view_count.nbodies())
    
def run_cb():
    
    def time_step():
        nonlocal nsteps
        step_system(bodies, dt)
        canvas.move_planets(bodies)
        run_frame.update_progress(1)
        sleep(0.02)
        if nsteps > 0:
            nsteps -= 1
            canvas.after_idle(time_step)
        else:
            run_frame.clear_progress()
        
    nsteps = run_frame.nsteps()
    run_frame.init_progress(nsteps)
    dt = run_frame.dt()
    canvas.after_idle(time_step)

canvas = SolarSystemCanvas(root)
canvas.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10, sticky="nsew")

tk.Button(root, text='Load', command=load_cb).grid(row=1, column=0, pady = 20)

view_count = ViewControl(root, view_cb)
view_count.grid(row=1, column=1, pady=20)

run_frame = RunFrame(root, run_cb)
run_frame.grid(row=1, column=2, pady=20)

if Main and not IPython:
    try:
        bodies = read_bodies("solarsystem.txt", TkBody)
        canvas.set_planets(bodies)
        view_count.reset(len(bodies))
        for i in range(5):
            view_count._spinbox.invoke('buttondown')
        run_frame._nsteps_entry.delete(0, tk.END)
        run_frame._nsteps_entry.insert(0,'100')
        root.update()
        run_frame._run_button.invoke()
    except Exception as err:
        print(err)
    input('hit return to continue...')
