# script auto-generated by phenix.molprobity


from __future__ import absolute_import, division, print_function
from six.moves import cPickle as pickle
from six.moves import range
try :
  import gobject
except ImportError :
  gobject = None
import sys

class coot_extension_gui(object):
  def __init__(self, title):
    import gtk
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    scrolled_win = gtk.ScrolledWindow()
    self.outside_vbox = gtk.VBox(False, 2)
    self.inside_vbox = gtk.VBox(False, 0)
    self.window.set_title(title)
    self.inside_vbox.set_border_width(0)
    self.window.add(self.outside_vbox)
    self.outside_vbox.pack_start(scrolled_win, True, True, 0)
    scrolled_win.add_with_viewport(self.inside_vbox)
    scrolled_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

  def finish_window(self):
    import gtk
    self.outside_vbox.set_border_width(2)
    ok_button = gtk.Button("  Close  ")
    self.outside_vbox.pack_end(ok_button, False, False, 0)
    ok_button.connect("clicked", lambda b: self.destroy_window())
    self.window.connect("delete_event", lambda a, b: self.destroy_window())
    self.window.show_all()

  def destroy_window(self, *args):
    self.window.destroy()
    self.window = None

  def confirm_data(self, data):
    for data_key in self.data_keys :
      outlier_list = data.get(data_key)
      if outlier_list is not None and len(outlier_list) > 0 :
        return True
    return False

  def create_property_lists(self, data):
    import gtk
    for data_key in self.data_keys :
      outlier_list = data[data_key]
      if outlier_list is None or len(outlier_list) == 0 :
        continue
      else :
        frame = gtk.Frame(self.data_titles[data_key])
        vbox = gtk.VBox(False, 2)
        frame.set_border_width(6)
        frame.add(vbox)
        self.add_top_widgets(data_key, vbox)
        self.inside_vbox.pack_start(frame, False, False, 5)
        list_obj = residue_properties_list(
          columns=self.data_names[data_key],
          column_types=self.data_types[data_key],
          rows=outlier_list,
          box=vbox)

# Molprobity result viewer
class coot_molprobity_todo_list_gui(coot_extension_gui):
  data_keys = [ "rama", "rota", "cbeta", "probe" ]
  data_titles = { "rama"  : "Ramachandran outliers",
                  "rota"  : "Rotamer outliers",
                  "cbeta" : "C-beta outliers",
                  "probe" : "Severe clashes" }
  data_names = { "rama"  : ["Chain", "Residue", "Name", "Score"],
                 "rota"  : ["Chain", "Residue", "Name", "Score"],
                 "cbeta" : ["Chain", "Residue", "Name", "Conf.", "Deviation"],
                 "probe" : ["Atom 1", "Atom 2", "Overlap"] }
  if (gobject is not None):
    data_types = { "rama" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "rota" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "cbeta" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT],
                   "probe" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT] }
  else :
    data_types = dict([ (s, []) for s in ["rama","rota","cbeta","probe"] ])

  def __init__(self, data_file=None, data=None):
    assert ([data, data_file].count(None) == 1)
    if (data is None):
      data = load_pkl(data_file)
    if not self.confirm_data(data):
      return
    coot_extension_gui.__init__(self, "MolProbity to-do list")
    self.dots_btn = None
    self.dots2_btn = None
    self._overlaps_only = True
    self.window.set_default_size(420, 600)
    self.create_property_lists(data)
    self.finish_window()

  def add_top_widgets(self, data_key, box):
    import gtk
    if data_key == "probe" :
      hbox = gtk.HBox(False, 2)
      self.dots_btn = gtk.CheckButton("Show Probe dots")
      hbox.pack_start(self.dots_btn, False, False, 5)
      self.dots_btn.connect("toggled", self.toggle_probe_dots)
      self.dots2_btn = gtk.CheckButton("Overlaps only")
      hbox.pack_start(self.dots2_btn, False, False, 5)
      self.dots2_btn.connect("toggled", self.toggle_all_probe_dots)
      self.dots2_btn.set_active(True)
      self.toggle_probe_dots()
      box.pack_start(hbox, False, False, 0)

  def toggle_probe_dots(self, *args):
    if self.dots_btn is not None :
      show_dots = self.dots_btn.get_active()
      overlaps_only = self.dots2_btn.get_active()
      if show_dots :
        self.dots2_btn.set_sensitive(True)
      else :
        self.dots2_btn.set_sensitive(False)
      show_probe_dots(show_dots, overlaps_only)

  def toggle_all_probe_dots(self, *args):
    if self.dots2_btn is not None :
      self._overlaps_only = self.dots2_btn.get_active()
      self.toggle_probe_dots()

class rsc_todo_list_gui(coot_extension_gui):
  data_keys = ["by_res", "by_atom"]
  data_titles = ["Real-space correlation by residue",
                 "Real-space correlation by atom"]
  data_names = {}
  data_types = {}

class residue_properties_list(object):
  def __init__(self, columns, column_types, rows, box,
      default_size=(380,200)):
    assert len(columns) == (len(column_types) - 1)
    if (len(rows) > 0) and (len(rows[0]) != len(column_types)):
      raise RuntimeError("Wrong number of rows:\n%s" % str(rows[0]))
    import gtk
    self.liststore = gtk.ListStore(*column_types)
    self.listmodel = gtk.TreeModelSort(self.liststore)
    self.listctrl = gtk.TreeView(self.listmodel)
    self.listctrl.column = [None]*len(columns)
    self.listctrl.cell = [None]*len(columns)
    for i, column_label in enumerate(columns):
      cell = gtk.CellRendererText()
      column = gtk.TreeViewColumn(column_label)
      self.listctrl.append_column(column)
      column.set_sort_column_id(i)
      column.pack_start(cell, True)
      column.set_attributes(cell, text=i)
    self.listctrl.get_selection().set_mode(gtk.SELECTION_SINGLE)
    for row in rows :
      self.listmodel.get_model().append(row)
    self.listctrl.connect("cursor-changed", self.OnChange)
    sw = gtk.ScrolledWindow()
    w, h = default_size
    if len(rows) > 10 :
      sw.set_size_request(w, h)
    else :
      sw.set_size_request(w, 30 + (20 * len(rows)))
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    box.pack_start(sw, False, False, 5)
    inside_vbox = gtk.VBox(False, 0)
    sw.add(self.listctrl)

  def OnChange(self, treeview):
    import coot # import dependency
    selection = self.listctrl.get_selection()
    (model, tree_iter) = selection.get_selected()
    if tree_iter is not None :
      row = model[tree_iter]
      xyz = row[-1]
      if isinstance(xyz, tuple) and len(xyz) == 3 :
        set_rotation_centre(*xyz)
        set_zoom(30)
        graphics_draw()

def show_probe_dots(show_dots, overlaps_only):
  import coot # import dependency
  n_objects = number_of_generic_objects()
  sys.stdout.flush()
  if show_dots :
    for object_number in range(n_objects):
      obj_name = generic_object_name(object_number)
      if overlaps_only and not obj_name in ["small overlap", "bad overlap"] :
        sys.stdout.flush()
        set_display_generic_object(object_number, 0)
      else :
        set_display_generic_object(object_number, 1)
  else :
    sys.stdout.flush()
    for object_number in range(n_objects):
      set_display_generic_object(object_number, 0)

def load_pkl(file_name):
  pkl = open(file_name, "rb")
  data = pickle.load(pkl)
  pkl.close()
  return data

data = {}
data['rama'] = []
data['omega'] = [('A', ' 163 ', 'PRO', None, (41.458, 18.932999999999996, 46.91))]
data['rota'] = [('A', '  40 ', 'ASP', 0.18687698307995373, (35.13, 70.737, 66.045)), ('A', '  48 ', 'VAL', 0.2962659722249227, (40.151, 59.301, 65.445)), ('A', '  83 ', 'GLN', 0.22536335626495205, (28.993, 36.104, 68.98)), ('A', '  86 ', 'MET', 0.0010565438772889508, (28.003, 41.0, 67.779)), ('A', ' 107 ', 'LEU', 0.0, (36.716, 69.396, 59.204)), ('A', ' 112 ', 'ILE', 0.028114606726213815, (41.049, 63.09899999999998, 59.907)), ('A', ' 113 ', 'LYS', 0.03955957021378619, (38.12299999999998, 64.041, 57.628)), ('A', ' 138 ', 'ILE', 0.043008065392471234, (23.046, 33.602, 56.44300000000001)), ('A', ' 140 ', 'LEU', 0.26560071472420743, (27.955, 31.814999999999998, 57.84)), ('A', ' 298 ', 'SER', 0.06355442101471322, (58.874, 22.342999999999993, 28.182000000000002)), ('A', ' 303 ', 'GLU', 0.015489188386475864, (56.552, 16.902, 38.433)), ('A', ' 307 ', 'LYS', 0.22584530474332185, (60.812999999999995, 15.467, 41.836)), ('A', ' 352 ', 'CYS', 0.20980570069726304, (39.969999999999985, 25.729999999999993, 51.645)), ('A', ' 375 ', 'LEU', 0.0, (53.001, 26.020000000000003, 39.396)), ('A', ' 394 ', 'TYR', 0.08596416395927325, (50.78699999999998, 50.208, 55.9)), ('A', ' 399 ', 'VAL', 0.05747665186808464, (43.16799999999999, 51.136, 60.89)), ('A', ' 425 ', 'LYS', 0.1981246704471854, (64.421, 32.312, 32.844)), ('A', ' 453 ', 'ASP', 0.06923743547341715, (45.667, 32.279, 32.529)), ('A', ' 468 ', 'ARG', 0.13474658655220978, (25.938, 40.911, 40.963)), ('A', ' 479 ', 'GLU', 0.0030695098980134537, (13.534999999999997, 34.18, 38.92)), ('A', ' 537 ', 'LEU', 0.0009709970618957433, (58.847, 48.242, 37.503)), ('A', ' 539 ', 'GLN', 0.055282402627415836, (61.556999999999995, 50.14899999999999, 33.336)), ('A', ' 609 ', 'LEU', 0.2819117874563267, (45.053, 30.64399999999999, 8.165))]
data['cbeta'] = [('A', ' 108 ', 'GLN', ' ', 0.9939173488757177, (41.086, 72.13, 58.612000000000016))]
data['probe'] = [(' A 179  LEU HD11', ' A 499  VAL HG23', -0.71, (26.948, 18.177, 31.068)), (' A 448  MET  HE2', ' A 599  LEU HD11', -0.674, (48.972, 32.429, 21.814)), (' A 104  VAL HG13', ' A 113  LYS  HG2', -0.673, (35.123, 64.601, 55.657)), (' A 148  VAL HG12', ' A 349  GLU  HG2', -0.659, (33.047, 21.475, 55.932)), (' A 579  GLN  NE2', ' A 584  GLN  HA ', -0.619, (51.154, 59.854, 35.737)), (' A 562  LEU  HB3', ' A 566  MET  HE2', -0.599, (54.847, 47.03, 46.228)), (' A 496  CYS  SG ', ' A 623  PRO  HD3', -0.592, (27.627, 24.863, 24.044)), (' A 304  ALA  O  ', ' A 308  GLN  HG2', -0.586, (61.618, 19.119, 40.844)), (' A  96  GLY  HA3', ' A 122  LEU  CD2', -0.577, (29.041, 54.164, 62.546)), (' A 267  GLU  HB2', ' A 618  GLN  NE2', -0.575, (28.774, 28.665, 13.196)), (' A 463  LEU HD11', ' A 489  ARG  HA ', -0.574, (30.009, 34.78, 31.221)), (' A 179  LEU HD11', ' A 499  VAL  CG2', -0.566, (26.04, 17.886, 31.298)), (' A 247  LEU  O  ', ' A 251  VAL HG23', -0.563, (42.326, 29.937, 22.511)), (' A 584  GLN  HB2', ' A 585  PRO  HD2', -0.555, (49.402, 59.077, 33.897)), (' A 365  PHE  CE1', ' A 392  MET  HG2', -0.538, (52.814, 42.556, 58.496)), (' A 252  ARG  HD2', ' A 265  ASN  O  ', -0.519, (33.02, 26.911, 17.766)), (' A 323  PHE  O  ', ' A 328  LEU  HB2', -0.484, (60.16, 42.758, 49.122)), (' A 412  ALA  O  ', ' A 416  VAL HG23', -0.482, (50.872, 42.883, 40.803)), (' A 490  LEU HD21', ' A 619  TYR  HB2', -0.48, (24.758, 33.348, 22.381)), (' A  98  GLN  HA ', ' A 101  LYS  HE2', -0.478, (28.575, 60.573, 67.738)), (' A 223  MET  HE1', ' A 519  PRO  HG2', -0.477, (34.002, 44.572, 47.514)), (' A 281  GLN HE21', ' A 680  RX3  H27', -0.466, (40.655, 32.268, 39.201)), (' A 448  MET  HE1', ' A 603  LEU HD21', -0.461, (46.996, 31.524, 21.022)), (' A 299  MET  HB2', ' A 433  LEU HD23', -0.46, (60.487, 22.528, 32.731)), (' A 127  LEU  HG ', ' A 207  ALA  HB2', -0.459, (22.433, 45.536, 57.208)), (' A 325  SER  O  ', ' A 554  GLN  HA ', -0.458, (66.074, 41.963, 44.663)), (' A 511  LYS  O  ', ' A 515  PRO  HD2', -0.451, (30.527, 31.69, 45.438)), (' A 498  PRO  HA ', ' A 623  PRO  HG2', -0.451, (27.313, 21.932, 26.935)), (' A  54  THR  OG1', ' A  91  HIS  HE1', -0.451, (37.593, 51.463, 68.844)), (' A 488  LEU HD22', ' A 492  TYR  HE1', -0.448, (27.734, 41.012, 31.106)), (' A 606  GLU  OE2', ' A 610  HIS  CE1', -0.447, (46.607, 26.78, 12.848)), (' A 209  ARG  HA ', ' A 213  TYR  O  ', -0.444, (21.123, 52.65, 50.638)), (' A 148  VAL HG12', ' A 349  GLU  CG ', -0.442, (33.312, 21.17, 56.197)), (' A 428  HIS  HD2', ' A 433  LEU  O  ', -0.441, (66.339, 24.928, 33.887)), (' A 299  MET  HB3', ' A 299  MET  HE2', -0.432, (60.765, 19.942, 33.876)), (' A  82  LEU HD11', ' A 140  LEU HD22', -0.428, (26.52, 31.103, 62.623)), (' A 326  LEU  O  ', ' A 559  GLY  HA3', -0.423, (62.57, 46.484, 46.468)), (' A 162  GLU  HA ', ' A 163  PRO  HA ', -0.422, (40.993, 20.532, 45.113)), (' A 584  GLN  HB2', ' A 585  PRO  CD ', -0.42, (49.11, 59.034, 34.61)), (' A 169  MET  O  ', ' A 276  GLY  HA2', -0.416, (40.46, 20.965, 33.355)), (' A 390  TYR  HB3', ' A 410  HIS  CE1', -0.416, (47.827, 44.523, 51.621)), (' A 493  GLN  HB3', ' A 495  LEU  HG ', -0.414, (33.276, 31.836, 28.376)), (' A 529  ILE HD12', ' A 533  PHE  CZ ', -0.413, (47.939, 48.685, 40.502)), (' A 548  HIS  HA ', ' A 595  TYR  CE1', -0.41, (55.861, 39.503, 30.085)), (' A 382  HIS  O  ', ' A 414  GLY  HA3', -0.408, (51.606, 38.148, 45.67)), (' A 281  GLN  NE2', ' A 680  RX3  H27', -0.403, (40.151, 32.068, 39.209)), (' A  82  LEU  HA ', ' A  85  ASN HD22', -0.403, (29.32, 35.896, 63.837)), (' A 189  ALA  O  ', ' A 193  ILE HG12', -0.402, (25.704, 26.448, 47.15)), (' A  48  VAL HG21', ' A 112  ILE HG13', -0.4, (41.379, 61.602, 61.96))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
