from quippy.potential import Potential
from ase import Atoms
from ase.io import write
from ase.io.trajectory import Trajectory

pot = Potential('IP GAP', param_filename='gp_new_hcp.xml')
traj = Trajectory('zrlj.traj', 'w')

for x in range(1,500):
    zr2 = Atoms('Zr2', positions=[[0,0,0], [0,0,(x/100)]])
    zr2.set_calculator(pot)
    zr2.get_potential_energy()
    traj.write(zr2)
