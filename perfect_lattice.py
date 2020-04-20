from quippy.potential import Potential

from ase.optimize import BFGS

from ase.build import bulk

from ase.io import write

# The potential file should be in the same folder you are running the script in

pot = Potential('IP GAP', param_filename='zr_hcp_test.xml')



# Create a unit cell (from here it’s all ASE commands)

zr=bulk('Zr', crystalstructure='hcp', a=3.23, c=5.16) * (5, 5, 5)

zr.set_calculator(pot)

dyn = BFGS(zr, trajectory='zr.traj')

dyn.run(fmax=0.001)

print(zr.get_volume())
write('output.xyz', zr)
