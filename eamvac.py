from ase.calculators.eam import EAM

from ase.optimize import BFGS

from ase.build import bulk

from ase.io import write

# The potential file should be in the same folder you are running the script in

pot = EAM(potential='Zr_3.eam.fs')


# Create a unit cell (from here it’s all ASE commands)

n = 5

unit_cell=bulk('Zr', crystalstructure='hcp', a=3.23, c=5.16) * (n, n, n)

del unit_cell[n**3]

unit_cell.set_calculator(pot)


write('vacunrel.xyz', unit_cell)
# Optimise the geometry of this cell – this won’t really do anything

dyn = BFGS(unit_cell)

dyn.run(fmax=0.001)

write('vacrel.xyz', unit_cell)
