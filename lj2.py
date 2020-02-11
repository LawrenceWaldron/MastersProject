from ase.io import read, write

configs = read('zrlj.traj@0:500')

energies = [zr2.get_potential_energy() for zr2 in configs]

with open('energy.txt', 'w') as filehandle:
    for listitem in energies:
        filehandle.write('%s\n' % listitem)
