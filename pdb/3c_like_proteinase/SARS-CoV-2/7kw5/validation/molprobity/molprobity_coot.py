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
data['rama'] = [('A', ' 119 ', 'ASN', 0.008577513857237597, (-22.546, -0.004, 14.761)), ('A', ' 142 ', 'ASN', 0.04317867196950437, (-18.672, 5.326, 22.300000000000008)), ('A', ' 143 ', 'GLY', 0.09597084062134244, (-20.323000000000008, 2.947, 19.769))]
data['omega'] = [('A', ' 119 ', 'ASN', None, (-21.381, 0.7989999999999999, 15.133000000000001))]
data['rota'] = [('B', '  45 ', 'THR', 0.008159601566148922, (18.902, -19.768, -6.433000000000001)), ('B', '  50 ', 'LEU', 0.05827810344745534, (24.614, -12.144, -5.931000000000001)), ('B', ' 189 ', 'GLN', 0.03164700751993958, (21.934000000000008, -10.669, -1.285))]
data['cbeta'] = [('A', ' 142 ', 'ASN', ' ', 0.26953574812534725, (-19.739, 6.405999999999997, 22.491000000000003)), ('A', ' 240 ', 'GLU', ' ', 0.2788148403194119, (2.4600000000000004, -6.460999999999999, 39.33500000000001)), ('B', ' 154 ', 'TYR', ' ', 0.3123955097860253, (-15.11, 3.605999999999999, 3.375)), ('B', ' 240 ', 'GLU', ' ', 0.2569571933281496, (11.444000000000004, 14.521999999999997, 9.022))]
data['probe'] = [(' B 132  PRO  CA ', ' B 132  PRO  N  ', -1.329, (11.547, 8.646, 6.101)), (' A 102  LYS  NZ ', ' A 156  CYS  SG ', -0.802, (-9.884, -23.05, 20.363)), (' B  22  CYS  SG ', ' B 550  HOH  O  ', -0.72, (10.972, -20.572, -10.598)), (' B 189  GLN  HA ', ' B 189  GLN  NE2', -0.718, (21.644, -10.53, -0.111)), (' A  76  ARG  HB3', ' A  92  ASP  OD2', -0.716, (-35.89, -14.409, 11.737)), (' A 142  ASN  O  ', ' A 601  HOH  O  ', -0.693, (-20.648, 2.427, 22.773)), (' B 297  VAL  O  ', ' B 401  SER  N  ', -0.69, (-11.888, 12.168, 12.377)), (' A   0  MET  HG2', ' A   3  PHE  HB2', -0.688, (10.839, -8.904, 18.2)), (' A 130  MET  HE3', ' A 134  PHE  HA ', -0.682, (-8.345, -6.222, 34.324)), (' A 505  DMS  S  ', ' A 657  HOH  O  ', -0.681, (-1.927, -2.139, 18.505)), (' B 132  PRO  C  ', ' B 132  PRO  N  ', -0.656, (12.344, 7.656, 6.198)), (' A   6  MET  HB2', ' A 509  DMS  H11', -0.633, (0.807, -9.971, 15.794)), (' B  86  VAL HG13', ' B 179  GLY  HA2', -0.631, (7.203, -4.675, -7.496)), (' A 221  ASN  OD1', ' A 602  HOH  O  ', -0.6, (21.85, -8.247, 37.212)), (' B 298  ARG HH11', ' B 403  DMS  H13', -0.598, (-7.644, 4.889, 10.917)), (' A  21  THR  OG1', ' A  26  THR HG23', -0.593, (-28.885, -0.729, 16.465)), (' B  69  GLN  HG2', ' B  74  GLN  HG3', -0.591, (-0.468, -25.397, -3.467)), (' A 169  THR HG23', ' A 171  VAL HG22', -0.591, (-10.072, 4.657, 33.101)), (' B 136  ILE  HB ', ' B 172  HIS  CD2', -0.582, (8.588, -2.678, 6.876)), (' A 130  MET  HE1', ' A 182  TYR  HB3', -0.561, (-10.905, -7.81, 33.826)), (' A  55  GLU  OE1', ' A 603  HOH  O  ', -0.549, (-30.028, -8.837, 37.091)), (' B  51  ASN  ND2', ' B  51  ASN  O  ', -0.546, (24.294, -10.737, -11.716)), (' A 256  GLN  NE2', ' A 300  CYS  O  ', -0.544, (13.638, -20.47, 23.332)), (' A 108  PRO  HA ', ' A 130  MET  HG3', -0.537, (-5.496, -8.872, 33.207)), (' A  86  VAL HG13', ' A 179  GLY  HA2', -0.533, (-21.511, -11.07, 29.509)), (' A  95  ASN  HB3', ' A  98  THR  OG1', -0.529, (-21.665, -18.477, 12.792)), (' A  30  LEU HD22', ' A 148  VAL HG11', -0.519, (-17.789, -10.994, 20.596)), (' A 129  ALA  N  ', ' A 290  GLU  OE2', -0.519, (-2.07, -5.175, 26.174)), (' A 141  LEU  O  ', ' A 141  LEU HD23', -0.518, (-18.065, 7.104, 18.532)), (' A  19  GLN  OE1', ' A 119  ASN  HB3', -0.513, (-24.935, 0.203, 13.31)), (' A  58  LEU HD22', ' A  82  MET  HE2', -0.51, (-32.595, -10.478, 31.107)), (' A  62  SER  H  ', ' A  65  ASN HD22', -0.51, (-40.035, -6.414, 23.639)), (' B 142  ASN  O  ', ' B 501  HOH  O  ', -0.509, (6.238, -8.352, 8.644)), (' A 264  MET  HE3', ' A 267  SER  HB2', -0.504, (18.053, -8.349, 34.052)), (' B  84  ASN  HB2', ' B 179  GLY  HA3', -0.502, (8.249, -3.199, -9.89)), (' B  27  LEU HD21', ' B  42  VAL  HB ', -0.489, (10.043, -15.329, -3.801)), (' B  63  ASN  OD1', ' B  80  HIS  HD2', -0.482, (4.512, -18.907, -16.516)), (' A  27  LEU HD21', ' A  42  VAL  HB ', -0.479, (-26.261, -2.636, 23.855)), (' A 235  MET  SD ', ' A 241  PRO  HG3', -0.479, (3.616, -5.401, 45.745)), (' A 130  MET  CE ', ' A 134  PHE  HA ', -0.475, (-8.7, -6.991, 34.433)), (' B 167  LEU HD12', ' B 171  VAL HG23', -0.474, (15.481, -2.339, 7.431)), (' B  45  THR HG23', ' B  48  ASP  HB2', -0.471, (20.325, -18.741, -8.909)), (' B 209  TYR  O  ', ' B 213  ILE HG13', -0.47, (-6.279, 17.484, 19.074)), (' B 245  ASP  O  ', ' B 249  ILE HG13', -0.47, (0.488, 19.621, 3.765)), (' B 298  ARG  NH1', ' B 403  DMS  H13', -0.47, (-7.505, 5.152, 10.483)), (' A  95  ASN  OD1', ' A  97  LYS  HB2', -0.464, (-21.135, -15.885, 9.899)), (' B   8  PHE  HB3', ' B 152  ILE HD12', -0.461, (-8.158, -2.043, 7.401)), (' B  49  MET  HG2', ' B  49  MET  O  ', -0.459, (21.335, -12.552, -4.099)), (' A 503  PEG  H11', ' A 503  PEG  H32', -0.459, (-1.03, 2.563, 27.648)), (' A  26  THR  O  ', ' A 604  HOH  O  ', -0.459, (-24.069, 1.895, 19.747)), (' B 259  ILE HG21', ' B 264  MET  HE2', -0.457, (-1.035, 23.378, 18.852)), (' A 115  LEU HD11', ' A 122  PRO  HB3', -0.457, (-13.129, -5.065, 12.643)), (' A 114  VAL  HB ', ' A 126  TYR  CE1', -0.456, (-8.617, -3.911, 21.513)), (' B 207  TRP  CD2', ' B 288  GLU  HB3', -0.451, (2.283, 10.199, 19.626)), (' A 505  DMS  H22', ' B 127  GLN  H  ', -0.449, (0.44, -2.445, 14.73)), (' B  88  LYS  NZ ', ' B 509  HOH  O  ', -0.447, (2.536, -5.108, -14.928)), (' A  27  LEU HD13', ' A  39  PRO  HD2', -0.444, (-23.519, -4.58, 23.162)), (' B 298  ARG HH12', ' B 403  DMS  H22', -0.442, (-6.251, 4.744, 9.943)), (' A  47  GLU  HG3', ' A 501  PEG  H12', -0.438, (-34.379, 9.425, 33.913)), (' A  63  ASN  HB3', ' A  77  VAL  O  ', -0.436, (-37.591, -12.649, 18.399)), (' B 217  ARG  HB2', ' B 220  LEU HD12', -0.435, (-3.553, 23.46, 25.382)), (' B  27  LEU HD13', ' B  39  PRO  HD2', -0.431, (7.17, -13.526, -2.047)), (' B 218  TRP  CG ', ' B 279  ARG  HD3', -0.427, (1.727, 18.635, 30.867)), (' B  31  TRP  CE2', ' B  95  ASN  HB2', -0.424, (-7.535, -15.545, -5.932)), (' A  40  ARG  HG3', ' A  54  TYR  CE1', -0.423, (-28.191, -4.576, 31.373)), (' A 502  PEG  H22', ' A 502  PEG  H41', -0.422, (-29.011, 1.249, 11.98)), (' A 246  HIS  HA ', ' A 249  ILE HD12', -0.42, (4.287, -16.739, 36.528)), (' A  31  TRP  CZ2', ' A  75  LEU HD21', -0.416, (-27.374, -13.829, 11.854)), (' A  32  LEU HD13', ' A 101  TYR  CD2', -0.416, (-18.115, -18.239, 19.944)), (' B  49  MET  CG ', ' B  49  MET  O  ', -0.411, (21.317, -12.771, -4.185)), (' B  45  THR  CG2', ' B  48  ASP  HB2', -0.41, (20.858, -18.879, -8.732)), (' A 286  LEU  HG ', ' B 286  LEU HD12', -0.408, (8.9, 5.162, 25.288)), (' B  49  MET  HG2', ' B 189  GLN  H  ', -0.407, (20.846, -11.522, -3.316)), (' A 124  GLY  HA2', ' B   9  PRO  HD3', -0.407, (-9.584, -1.753, 11.967)), (' A  73  VAL HG12', ' A  75  LEU HD12', -0.407, (-29.873, -11.128, 9.039)), (' A   0  MET  SD ', ' A 210  ALA  HB1', -0.407, (11.71, -10.979, 22.374)), (' B 109  GLY  HA2', ' B 200  ILE HD13', -0.401, (6.397, 8.974, 8.845)), (' A  51  ASN  O  ', ' A 605  HOH  O  ', -0.401, (-33.202, 1.998, 37.61))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
