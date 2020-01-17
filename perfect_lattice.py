from quippy.potential import Potential

from ase.optimize import BFGS

from ase.build import bulk

from ase.io import write

# The potential file should be in the same folder you are running the script in

pot = Potential('IP GAP', param_filename='gp_new_hcp.xml')



# Create a unit cell (from here it’s all ASE commands)

unit_cell=bulk('Zr', crystalstructure='hcp', a=3.223352707047396, c=5.172324479026618) * (5, 5, 5)

unit_cell.set_calculator(pot)


# Optimise the geometry of this cell – this won’t really do anything

dyn = BFGS(unit_cell)

dyn.run(fmax=0.05)

write('output.xyz', unit_cell)
