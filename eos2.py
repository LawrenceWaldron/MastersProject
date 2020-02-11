from ase.io import read, write
from ase.units import kJ
from ase.eos import EquationOfState
from quippy.potential import Potential

pot = Potential('IP GAP', param_filename='gp_new_hcp.xml')
configs = read('Zr.traj@0:100')  # read 100 configurations
zr.set_calculator(pot)
# Extract volumes and energies:
volumes = [zr.get_volume() for zr in configs]
energies = [zr.get_potential_energy() for zr in configs]


with open('volume.txt', 'w') as filehandle:
    for listitem in volumes:
        filehandle.write('%s\n' % listitem)

with open('energy.txt', 'w') as filehandle:
    for listitem in energies:
        filehandle.write('%s\n' % listitem)
