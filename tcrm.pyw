#!/usr/bin/env pythonw
"""
TCRM User Interface
"""

import matplotlib as mp
import Tkinter as tk
import ttk
import numpy as np
import collections
import json

from matplotlib.widgets import RectangleSelector
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure as MatplotlibFigure
from matplotlib.patches import Rectangle
from mpl_toolkits.basemap import Basemap

#json.encoder.FLOAT_REPR = lambda f: ('%.2f' % f)

ICON = """
R0lGODlhIAAgAPcAAAAAAAAAMwAAZgAAmQAAzAAA/wArAAArMwArZgArmQArzAAr/wBVAA
BVMwBVZgBVmQBVzABV/wCAAACAMwCAZgCAmQCAzACA/wCqAACqMwCqZgCqmQCqzACq/wDV
AADVMwDVZgDVmQDVzADV/wD/AAD/MwD/ZgD/mQD/zAD//zMAADMAMzMAZjMAmTMAzDMA/z
MrADMrMzMrZjMrmTMrzDMr/zNVADNVMzNVZjNVmTNVzDNV/zOAADOAMzOAZjOAmTOAzDOA
/zOqADOqMzOqZjOqmTOqzDOq/zPVADPVMzPVZjPVmTPVzDPV/zP/ADP/MzP/ZjP/mTP/zD
P//2YAAGYAM2YAZmYAmWYAzGYA/2YrAGYrM2YrZmYrmWYrzGYr/2ZVAGZVM2ZVZmZVmWZV
zGZV/2aAAGaAM2aAZmaAmWaAzGaA/2aqAGaqM2aqZmaqmWaqzGaq/2bVAGbVM2bVZmbVmW
bVzGbV/2b/AGb/M2b/Zmb/mWb/zGb//5kAAJkAM5kAZpkAmZkAzJkA/5krAJkrM5krZpkr
mZkrzJkr/5lVAJlVM5lVZplVmZlVzJlV/5mAAJmAM5mAZpmAmZmAzJmA/5mqAJmqM5mqZp
mqmZmqzJmq/5nVAJnVM5nVZpnVmZnVzJnV/5n/AJn/M5n/Zpn/mZn/zJn//8wAAMwAM8wA
ZswAmcwAzMwA/8wrAMwrM8wrZswrmcwrzMwr/8xVAMxVM8xVZsxVmcxVzMxV/8yAAMyAM8
yAZsyAmcyAzMyA/8yqAMyqM8yqZsyqmcyqzMyq/8zVAMzVM8zVZszVmczVzMzV/8z/AMz/
M8z/Zsz/mcz/zMz///8AAP8AM/8AZv8Amf8AzP8A//8rAP8rM/8rZv8rmf8rzP8r//9VAP
9VM/9VZv9Vmf9VzP9V//+AAP+AM/+AZv+Amf+AzP+A//+qAP+qM/+qZv+qmf+qzP+q///V
AP/VM//VZv/Vmf/VzP/V////AP//M///Zv//mf//zP///wAAAAAAAAAAAAAAACH5BAEAAP
wALAAAAAAgACAAAAj/AB9UqCCQ4MCCCA8qNMiw4MAKDg5SMEjB4cOLGDPu28ix48aMIEF6
HBktpMmHI0eevGhhIIcKHFJ6hAnzJQebNjfQLAKkyA8LRSp0rBCUww8jR5PyXNqzpxGBRo
wUidrRCBCpWKdezer0B8KKP37A6fjGSFk1cIyoMWsWCJy0DRcK7Pj27Ru7dX8QjPigYgUK
fiNC7CiQL8EiHoP6PehQ4IOOhitCS6lMYMWJgSEK5ZhwrEw4juMe7Hh5sMyNi0vzpUD4IG
LODh5zHGj46+aNhj3v0/RQ075o+/QaLChY9kbiuu2sflB7omaDDkgX1M0bY9/hyytChvjg
DUc4FWPHz77c9wHz8cwhl/e+UVPE99zfO5gfPzrs+cnPz6c/X//++ZDtx94+mfQn3n8I/h
fgfAPCkeCDCXaEwHwIDFjgfDiE9QOCDUyIgIeQHTDfGBwtM+EBHeHggIcINCDiAS52dECL
LXakDA7AcfRihwjM2OGMMs54AIqnRSNkjzAO+WKQPxKZUgBJujgkkkMGqeQBAYxEz5VUXo
llJpqACaWXAByQSSZpeHkllGWOeUCbBgwJ5ZhzYvmmnW2WCUAABuxpAJ+AAtDnn4Pyqeeb
gBoQEAA7
"""


class Observable(object):

    """
    Base class for observable objects.
    """

    def __init__(self):
        """
        Initialise the class.
        """
        self.callbacks = []

    def addCallback(self, callback):
        """
        Add a function to be called when the 'notify' event occurs.
        """
        self.callbacks.append(callback)

    def notify(self, value):
        """
        Notify all subscribed callback functions. This function is
        typically called by subclasses of this object when they wish
        to notify that their state has changed. All registered
        callbacks are called with 'value' as their argument.
        """
        for callback in self.callbacks:
            callback(value)


class ObservableDict(Observable):

    """
    An observable dictionary object.
    """

    def __init__(self, theDict=None):
        """
        Construct an observable dictionary from `theDict`. If `theDict`
        is not provided then a new `dict` is created.
        """
        super(ObservableDict, self).__init__()
        self.theDict = theDict or {}

    def __setitem__(self, key, value):
        """
        Set an item in the dict with `dict[key] = value`.
        """
        prev = self.theDict.get(key)
        if value != prev:
            self.theDict[key] = value
            self.notify(self.theDict)

    def __getitem__(self, key):
        """
        Get an item in the dict with `dict[key]`.
        """
        return self.theDict.get(key)

    def __repr__(self):
        """
        Return a string representation of the dictionary.
        """
        return self.theDict.__repr__(self)


class ObservableVariable(Observable):

    """
    An observable variable. The `variable` is internally stored as a
    tk.StringVar object so that it can be used by Tk controls. Basic
    python objects are serialised to JSON format so that they can be
    easily edited through Tk controls as well.
    """

    def __init__(self, value):
        """
        Construct a variable with initial value `value`.
        """
        super(ObservableVariable, self).__init__()
        self.variable = tk.StringVar()
        self.set(value)
        self.variable.trace('w', self.changed)

    def changed(self, *args):
        """
        Automatically called when the variable changes.
        """
        self.notify(self.get())

    def set(self, value):
        """
        Helper function to set the value of the variable.
        """
        self.variable.set(json.dumps(value))

    def get(self):
        """
        Helper function to get the value of the variable.
        """
        value = self.variable.get()
        return json.loads(value)


class Model(object):
    pass


class Simulation(Model):
    pass


class View(object, ttk.Frame):

    """
    An abstract view.
    """

    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent)


class LabeledView(object, ttk.Labelframe):

    """
    A labeled view.
    """

    def __init__(self, parent, name='', **kwargs):
        ttk.Labelframe.__init__(self, parent, text=name)


class ObservableEntry(ttk.Frame, ObservableVariable):

    """
    An observable entry control.
    """

    def __init__(self, parent, **kwargs):
        name = kwargs.pop('name', '')
        value = kwargs.pop('value', '')

        ttk.Frame.__init__(self, parent)
        ObservableVariable.__init__(self, value=value)

        self.label = ttk.Label(self, text=name + ':')
        self.label.grid(column=0, row=0, sticky='W', padx=2)

        self.entry = ttk.Entry(self, **kwargs)
        self.entry.grid(column=1, row=0, sticky='E', padx=2)
        self.entry.config(textvariable=self.variable)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)


class ObservableSpinbox(ttk.Frame, ObservableVariable):

    def __init__(self, parent, **kwargs):
        name = kwargs.pop('name', '')
        width = kwargs.pop('width', 10)
        lower = kwargs.pop('lower', 0)
        upper = kwargs.pop('upper', 100)
        value = kwargs.pop('value', 0)

        ttk.Frame.__init__(self, parent)
        ObservableVariable.__init__(self, value)

        self.label = ttk.Label(self, width=width, text=name + ':')
        self.label.grid(column=0, row=0, sticky='NSEW')

        self.spinbox = tk.Spinbox(self, from_=lower, to=upper, increment=10)
        self.spinbox.grid(column=1, row=0, sticky='NSEW')
        self.spinbox.config(textvariable=self.variable)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)


class ObservableScale(ttk.Frame, ObservableVariable):

    def __init__(self, parent, **kwargs):
        name = kwargs.pop('name', '')
        lower = kwargs.pop('lower', 0)
        upper = kwargs.pop('upper', 100)
        value = kwargs.pop('value', 0)

        ttk.Frame.__init__(self, parent)
        ObservableVariable.__init__(self, value)

        self.label = ttk.Label(self, text=name + ':')
        self.label.grid(column=0, row=0, sticky='EW',  padx=2)

        self.value = ttk.Entry(self, textvariable=self.variable, **kwargs)
        self.value.grid(column=1, row=0, sticky='W', padx=2)

        self.scale = ttk.Scale(self, from_=lower, to=upper, value=value,
                               length=50)
        self.scale.grid(column=2, row=0, sticky='EW', padx=2)
        self.scale.config(variable=self.variable, command=self.format)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

        self.noPendingNotification = True

    def format(self, *args):
        self.set('%.2f' % self.get())

    def changed(self, *args):
        if self.noPendingNotification:
            self.after(1000, self.doNotify)
            self.noPendingNotification = False

    def doNotify(self, *args):
        self.notify(self.get())
        self.noPendingNotification = True


class ObservableCombobox(ttk.Frame, ObservableVariable):

    def __init__(self, parent, **kwargs):
        name = kwargs.pop('name', '')
        width = kwargs.pop('width', 10)
        values = kwargs.pop('values', ['a', 'b', 'c'])

        ttk.Frame.__init__(self, parent)
        ObservableVariable.__init__(self, value='')

        self.label = ttk.Label(self, width=width, text=name + ':')
        self.label.grid(column=0, row=0, sticky='NSEW')

        self.combo = ttk.Combobox(self, values=values)
        self.combo.grid(column=1, row=0, sticky='NSEW')
        self.combo.config(textvariable=self.variable)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)


class MapView(View):

    def __init__(self, parent, **kwargs):
        bgColor = '#%02x%02x%02x' % \
                  tuple([c / 255 for c in
                         parent.winfo_rgb('SystemButtonFace')])
        figSize = kwargs.pop('figSize', (3, 1.3))
        continentColor = kwargs.pop('continentColor', '0.8')
        coastlineWidth = kwargs.pop('coastlineWidth', 0.3)

        ttk.Frame.__init__(self, parent)

        figure = MatplotlibFigure(figsize=figSize, facecolor=bgColor)

        self.axes = figure.add_subplot(111, aspect='auto')

        self.basemap = Basemap(llcrnrlon=0, llcrnrlat=-80, urcrnrlon=360,
                               urcrnrlat=80, projection='mill', ax=self.axes)
        self.basemap.drawcoastlines(linewidth=coastlineWidth)
        self.basemap.fillcontinents(color=continentColor)

        self.axes.set_aspect('auto')
        figure.tight_layout(pad=0)

        self.canvas = FigureCanvasTkAgg(figure, master=self)
        widget = self.canvas.get_tk_widget()
        widget.config(highlightthickness=0)
        widget.config(background=bgColor, relief=tk.GROOVE, borderwidth=1)
        widget.grid(column=0, row=0, sticky='NSEW')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class MapRegionSelector(MapView, ObservableVariable):

    def __init__(self, parent, **kwargs):
        value = kwargs.pop('value', 0)
        self.regionFaceColor = kwargs.pop('regionFaceColor', 'cyan')
        self.regionEdgeColor = kwargs.pop('regionEdgeColor', 'black')
        self.regionAlpha = kwargs.pop('regionAlpha', 0.5)

        MapView.__init__(self, parent, **kwargs)
        ObservableVariable.__init__(self, value=value)

        self.selector = RectangleSelector(self.axes, self.onSelected,
                                          drawtype='box', useblit=True,
                                          minspanx=5, minspany=5,
                                          spancoords='pixels')
        self.addCallback(self.onValueChanged)
        self.region = None

    def drawRegion(self, xMin, xMax, yMin, yMax):
        x0, y0 = self.basemap(xMin, yMin)
        x1, y1 = self.basemap(xMax, yMax)
        w, h = (x1 - x0), (y1 - y0)
        if self.region is not None:
            self.region.remove()
        self.region = Rectangle((x0, y0), w, h, ec=self.regionEdgeColor,
                                fc=self.regionFaceColor, alpha=self.regionAlpha)
        self.axes.add_patch(self.region)
        self.canvas.draw()

    def onValueChanged(self, value):
        limits = self.get()
        xMin = limits['xMin']
        xMax = limits['xMax']
        yMin = limits['yMin']
        yMax = limits['yMax']
        self.drawRegion(xMin, xMax, yMin, yMax)

    def onSelected(self, eclick, erelease):
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        xMin, yMin = self.basemap(min(x1, x2), min(y1, y2), inverse=True)
        xMax, yMax = self.basemap(max(x1, x2), max(y1, y2), inverse=True)
        self.set({'xMin': xMin, 'xMax': xMax, 'yMin': yMin, 'yMax': yMax})

class GridLimitsEntry(ObservableEntry):

    def __init__(self, parent, **kwargs):
        super(GridLimitsEntry, self).__init__(parent, **kwargs)

    def get(self):
        limits = eval(self.variable.get(), {'__builtins__': None}, {})
        xMin = float(limits['xMin'])
        xMax = float(limits['xMax'])
        yMin = float(limits['yMin'])
        yMax = float(limits['yMax'])
        return {'xMin': xMin, 'xMax': xMax, 'yMin': yMin, 'yMax': yMax}


class DictEntry(ttk.Labelframe, ObservableVariable):

    def __init__(self, parent, **kwargs):
        name = kwargs.pop('name', '')
        columns = kwargs.pop('columns', 2)

        ttk.Labelframe.__init__(self, parent, text=name)
        ObservableVariable.__init__(self, value='')

        self.keys = kwargs.pop('keys', None)
        self.entries = {key: ObservableEntry(self, name=key, **kwargs)
                        for key in self.keys}
        for i, key in enumerate(self.keys):
            c, r = i % columns, i / columns
            entry = self.entries[key]
            entry.addCallback(self.changed)
            entry.grid(row=r, column=c, sticky='EW', padx=2, pady=2)
            self.rowconfigure(r, weight=1)
            self.columnconfigure(c, weight=1)

        self.allowNotify = False

    def changed(self, *args):
        if self.allowNotify:
            self.notify(self.get())

    def set(self, value):
        if isinstance(value, dict):
            self.allowNotify = False
            for key in self.keys:
                entry = self.entries[key]
                entry.set(value[key])
            self.allowNotify = True

    def get(self):
        value = {}
        for key in self.keys:
            entry = self.entries[key]
            value[key] = entry.get()
        return value


class MapRegionGrid(MapView):

    def __init__(self, parent, **kwargs):
        self.gridStyle = kwargs.pop('gridStyle', '-')
        self.gridColor = kwargs.pop('gridColor', '0.7')
        MapView.__init__(self, parent, **kwargs)
        self.region = None
        self.step = None

    def set(self, limits, step):
        if (self.region != limits) or (self.step != step):
            self.setRegionLimits(limits)
            self.region = limits
            self.axes.grid(False)
            self.canvas.draw()
            self.setGridStep(step)
            self.step = step
            self.after_idle(self.canvas.draw)

    def setRegionLimits(self, limits):
        xMin = limits['xMin']
        xMax = limits['xMax']
        yMin = limits['yMin']
        yMax = limits['yMax']
        x0, y0 = self.basemap(xMin, yMin)
        x1, y1 = self.basemap(xMax, yMax)
        self.axes.set_xlim((x0, x1))
        self.axes.set_ylim((y0, y1))

    def setGridStep(self, step):
        print('setGridStep')
        if step < 0.5 or self.region is None:
            return
        xMin = self.region['xMin']
        xMax = self.region['xMax']
        yMin = self.region['yMin']
        yMax = self.region['yMax']
        xs = np.arange(min(xMin, xMax), max(xMin, xMax), step)
        ys = np.arange(min(yMin, yMax), max(yMin, yMax), step)
        xs, ys = self.basemap(*np.meshgrid(xs, ys))
        self.axes.xaxis.set_ticks(xs.flatten())
        self.axes.yaxis.set_ticks(ys.flatten())
        self.axes.xaxis.set_ticklabels([])
        self.axes.yaxis.set_ticklabels([])
        self.axes.grid(True, which='both', linestyle=self.gridStyle,
                       color=self.gridColor)
        print('setGridStep end')


class GridSettingsView(ttk.Frame):

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        #self.limits = GridLimitsEntry(self, name='Grid limits')
        #self.limits.grid(column=0, row=1, sticky='EW', padx=2, pady=2)

        #self.foo = ObservableCombobox(self, name='Location')
        #self.foo.grid(column=0, row=3, padx=2, pady=2)

        self.bar = DictEntry(self, keys=('xMin', 'xMax', 'yMin', 'yMax'),
                             name='Grid limits', width=5, justify='center')
        self.bar.grid(column=0, row=0, padx=2, pady=2, sticky='W')

        self.step = ObservableScale(self, name='Grid step', width=5,
                                    justify='center')
        self.step.grid(column=0, row=1, padx=2, pady=2, sticky='NEW')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        #self.rowconfigure(2, weight=0)
        #self.rowconfigure(3, weight=0)
        #self.rowconfigure(4, weight=0)


class TrackSettingsView(ttk.Frame):

    def __init__(self, parent):
        #super(TrackSettingsView, self).__init__(parent, name='Track Settings')
        ttk.Frame.__init__(self, parent)
        self.nSims = ObservableEntry(self, name='Simulations',
                                     width=7, justify='center')
        self.nYears = ObservableEntry(self, name='Years per sim',
                                      width=7, justify='center')
        self.gridSpace = DictEntry(self, name='Grid space', keys=('x', 'y'),
                                   width=7, justify='center')
        self.gridInc = DictEntry(self, name='Grid increment', keys=('x', 'y'),
                                 width=7, justify='center')
        self.seasonSeed = ObservableEntry(self, name='Season seed', width=7,
                                          justify='center')
        self.trackSeed = ObservableEntry(self, name='Track seed', width=7,
                                         justify='center')
        for i, control in enumerate([self.gridSpace, self.gridInc, self.nSims,
                                     self.nYears, self.seasonSeed,
                                     self.trackSeed]):
            control.grid(column=0, row=i, sticky='WE', padx=4, pady=4)
            self.rowconfigure(i, weight=1)
        self.columnconfigure(0, weight=1)

class MainWindow(View):

    def init(self):
        lf, rf = self._initSideBySidePanes(self,
                                           left='Model Configuration',
                                           right='Graphics')
        self._initModelConfigControls(lf)

        figure = LineFigure(rf)
        figure.grid(sticky='NSEW')
        rf.columnconfigure(0, weight=1)
        rf.rowconfigure(0, weight=1)

        # self.columnconfigure(0, weight=0)
        # self.columnconfigure(1, weight=1)
        # self.rowconfigure(0, weight=1)

    def _initSideBySidePanes(self, parent, left='', right=''):
        p = ttk.Panedwindow(parent, orient=tk.HORIZONTAL)
        p.grid(sticky='NSEW', padx=3, pady=3)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        lf = ttk.Labelframe(p, text=left)
        rf = ttk.Labelframe(p, text=right)
        p.add(lf)
        p.add(rf)
        return (lf, rf)

    def _initModelConfigControls(self, parent):
        notebook = ttk.Notebook(parent)
        notebook.grid(sticky='NSEW')

        dataProcessFrame = ttk.Frame(notebook)
        self._initDataProcessingControls(dataProcessFrame)
        notebook.add(dataProcessFrame, text='Data')

        calibrationFrame = ttk.Frame(notebook)
        self._initCalibrationControls(calibrationFrame)
        notebook.add(calibrationFrame, text='Calibration')

        progress = ttk.Progressbar(parent,
                                   orient=tk.HORIZONTAL,
                                   mode='determinate')
        progress.grid(row=1, column=0, sticky='EW', padx=20)

        button = ttk.Button(parent, text=u'Ok', command=self.onOkClicked)
        button.grid(row=2, column=0)

        progress['value'] = 50

        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

        return notebook

    def _initDataProcessingControls(self, parent):
        self.entry1 = tk.StringVar()
        entry = ttk.Entry(parent, textvariable=self.entry1)
        entry.grid(column=0, row=0, sticky='EW')
        parent.columnconfigure(0, weight=1)

        self.combo = tk.StringVar()
        combo = ttk.Combobox(parent, textvariable=self.combo,
                             state='readonly')
        combo['values'] = ('one', 'two', 'three')
        combo.current(0)
        combo.grid(column=0, row=2, sticky='EW')

    def _initCalibrationControls(self, parent):
        self.entry2 = tk.StringVar()
        entry = ttk.Entry(parent, textvariable=self.entry2)
        entry.grid(column=0, row=0, sticky='NEW')

        button = ttk.Button(parent, text=u'Ok', command=self.onOkClicked)
        button.grid(column=0, row=1)

    def onOkClicked(self):
        self.entry1.set('Ok pressed.')

class Main(View):

    def __init__(self, parent):
        super(Main, self).__init__(parent)

        self.region = MapRegionSelector(self, figSize=(3, 1.3))
        self.region.grid(column=0, row=0, padx=2, pady=2, sticky='NEW')

        notebook = ttk.Notebook(self)
        notebook.grid(column=0, row=1, sticky='NW', padx=2, pady=2)

        self.gridSettings = GridSettingsView(notebook)
        self.track = TrackSettingsView(notebook)

        notebook.add(self.gridSettings, text='Region')
        notebook.add(self.track, text='Simulation')

        self.view = MapRegionGrid(self, figSize=(7, 5),
                                  continentColor='#cdcbc1',
                                  coastlineWidth=0.8)
        self.view.grid(column=1, row=0, rowspan=2, sticky='NSEW',
                       padx=2, pady=2)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)


class Controller(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.withdraw()
        self.title('Tropical Cyclone Risk Model')
        self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(data=ICON))

        self.settings = ObservableDict({
            'GRID_LIMITS': {'xMin': 113, 'xMax': 116, 'yMin': 10.5, 'yMax': -25},
            'GRID_STEP': 20.
        })  # Model

        self.view = Main(self)

        self.settings.addCallback(self.onSettingsChanged)

        # self.view.gridSettings.limits.addCallback(self.onGridLimitsChanged)
        self.view.region.addCallback(self.onGridLimitsChanged)
        self.view.gridSettings.bar.addCallback(self.onGridLimitsChanged)
        self.view.gridSettings.step.addCallback(self.onGridStepChanged)

        self.view.pack(fill='both', expand=True)

        self.onSettingsChanged(self.settings)

        self.after_idle(self.show)

    def onSettingsChanged(self, settings):
        # self.view.gridSettings.limits.set(settings['GRID_LIMITS'])
        self.view.region.set(settings['GRID_LIMITS'])
        self.view.gridSettings.bar.set(settings['GRID_LIMITS'])
        self.view.gridSettings.step.set(settings['GRID_STEP'])
        self.view.view.set(settings['GRID_LIMITS'], settings['GRID_STEP'])

    def onGridLimitsChanged(self, limits):
        self.settings['GRID_LIMITS'] = limits

    def onGridStepChanged(self, step):
        self.settings['GRID_STEP'] = step

    def show(self):
        self.update()
        self.deiconify()

Controller().mainloop()