from quippy.potential import Potential

from ase.optimize import BFGS

from ase.build import bulk

from ase.io import write

# The potential file should be in the same folder you are running the script in

pot = Potential('IP GAP', param_filename='zr_hcp_test.xml')



# Create a unit cell (from here it’s all ASE commands)

n = 5

vac=bulk('Zr', crystalstructure='hcp', a=3.23, c=5.16) * (n, n, n)

del vac[n**3]   #deletes centre atom

vac.set_calculator(pot)



# Relax the structure and get total energy

dyn = BFGS(vac, trajectory='vac.traj')

dyn.run(fmax=0.001)
