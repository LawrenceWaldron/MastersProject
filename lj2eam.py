from ase.io import read, write
from ase.calculators.eam import EAM

configs = read('zrlj.traj@0:500')
pot = EAM(potential='Zr_3.eam.fs')
a = [zr2.set_calculator(pot) for zr2 in configs]
energies = [zr2.get_potential_energy() for zr2 in configs]

with open('energy.txt', 'w') as filehandle:
    for listitem in energies:
        filehandle.write('%s\n' % listitem)
