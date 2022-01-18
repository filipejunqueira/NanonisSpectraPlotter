import nanonispy as napy

def load_img(filename):
    return napy.read.Scan(filename).signals

def load_grid(filename):
    return napy.read.Grid(filename)
