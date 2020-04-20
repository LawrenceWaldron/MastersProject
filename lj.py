from quippy.potential import Potential
from ase import Atoms
from ase.io import write
from ase.io.trajectory import Trajectory

pot = Potential('IP GAP', param_filename='/home/lawrence/zr_hcp_test.xml')
traj = Trajectory('zrlj.traj', 'w')

a=3.23
c=5.16

for x in range(1,500):
    zr2 = Atoms('Zr2', positions=[[0,0,0], [a/3,2*a/3,c/2]], cell =[a, a, c, 90, 90, 120], pbc=[0,0,0])
    zr2.set_calculator(pot)
    zr2.get_potential_energy()
    traj.write(zr2)
