import sys
from pathlib import Path
sys.path.append(Path(__file__))
import solvers.preProcessor as pre
import post.plotModel as pt

from matplotlib.pyplot import close
close("all")

fsi = pre.read("SPHW_reservoir_case")
pt.zerothPlot(fsi)
pt.firstPlot(fsi)

# print(fsi.firstOrder(10))
