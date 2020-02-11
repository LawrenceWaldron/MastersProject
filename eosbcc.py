import numpy as np

from ase.io.trajectory import Trajectory
from ase.build import bulk
from quippy.potential import Potential
from ase.io import write

pot = Potential('IP GAP', param_filename='gp_new_hcp.xml')

a0=3.57


traj = Trajectory('Zr.traj', 'w')

eps = 0.1
for a in a0 * np.linspace(1 - eps, 1 + eps, 100):
        zr = bulk('Zr', 'bcc', a=a, cubic=True)
        zr.set_calculator(pot)
        zr.get_potential_energy()
        traj.write(zr)
