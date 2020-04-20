from ase.calculators.eam import EAM
from ase import Atoms
from ase.io import write
from ase.io.trajectory import Trajectory

pot = EAM(potential='Zr_3.eam.fs')
traj = Trajectory('zrlj.traj', 'w')

for x in range(1,500):
    zr2 = Atoms('Zr2', positions=[[0,0,0], [0,0,(x/100)]], cell =[10, 10, (x/50)], pbc=[0,0,0])
    zr2.set_calculator(pot)
    zr2.get_potential_energy()
    traj.write(zr2)
