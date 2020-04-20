from quippy.potential import Potential
from ase import Atoms
from ase.io import write
from ase.io.trajectory import Trajectory
import numpy as np
from ase.optimize import BFGS
from ase.build import bulk

pot = Potential('IP GAP', param_filename='zr_improved_more_bcc.xml')
a=3.23
c=5.16
#generate structure
zr=bulk('Zr', crystalstructure='hcp', a=3.23, c=5.16) * (5, 5, 10)

#Shift layer of atoms from height 25-26 (single layer) incrementally in x-y direcitons
for shift_x in range(0,21):
    for shift_y in range(0,21):
        zr.positions=[x+np.array([(shift_x/20)*a,(shift_y/20)*a,0]) if 25<x[2]<26 else x for x in zr.positions]
#Add constraint so relaxation is only in z direction
        from ase.constraints import FixConstraint

        class FixAtomsLine(FixConstraint):

            """Constraint object for fixing some chosen atoms."""



            def __init__(self, direction, indices=None, mask=None):


                """Constrain chosen atoms.



                Parameters

                ----------

                indices : list of int

                   Indices for those atoms that should be constrained.

                mask : list of bool

                   One boolean per atom indicating if the atom should be

                   constrained or not.



                direction : line long hoch movement is allowed



                Examples

                --------

                Fix all Copper atoms:



                >>> mask = [s == 'Cu' for s in atoms.get_chemical_symbols()]

                >>> c = FixAtoms(mask=mask)

                >>> atoms.set_constraint(c)



                Fix all atoms with z-coordinate less than 1.0 Angstrom:



                >>> c = FixAtoms(mask=atoms.positions[:, 2] < 1.0)

                >>> atoms.set_constraint(c)

                """



                if indices is None and mask is None:

                    raise ValueError('Use "indices" or "mask".')

                if indices is not None and mask is not None:

                    raise ValueError('Use only one of "indices" and "mask".')



                if mask is not None:

                    indices = np.arange(len(mask))[np.asarray(mask, bool)]

                else:

                    # Check for duplicates:

                    srt = np.sort(indices)

                    if (np.diff(srt) == 0).any():

                        raise ValueError(

                            'FixAtoms: The indices array contained duplicates. '

                           'Perhaps you wanted to specify a mask instead, but '

                            'forgot the mask= keyword.')

                self.index = np.asarray(indices, int)



                if self.index.ndim != 1:

                    raise ValueError('Wrong argument to FixAtoms class!')



                self.removed_dof = 3 * len(self.index)

                self.dir = np.asarray(direction) / np.sqrt(np.dot(direction, direction))



            def adjust_positions(self, atoms, new):

                for a in self.index:

                    step = new[a] - atoms.positions[a]

                    x = np.dot(step, self.dir)

                    new[a] = atoms.positions[a] + x * self.dir





            def adjust_forces(self, atoms, forces):

                for a in self.index:

                    forces[a] = self.dir * np.dot(forces[a], self.dir)



            def index_shuffle(self, atoms, ind):

                # See docstring of superclass

                index = []

                for new, old in slice2enlist(ind, len(atoms)):

                    if old in self.index:

                        index.append(new)

                if len(index) == 0:

                    raise IndexError('All indices in FixAtoms not part of slice')

                self.index = np.asarray(index, int)



            def get_indices(self):

                return self.index



            def __repr__(self):

                return 'FixAtoms(indices=%s)' % ints2string(self.index)



            def todict(self):

                return {'name': 'FixAtoms',

                        'kwargs': {'indices': self.index.tolist()}}



            def repeat(self, m, n):

                i0 = 0

                natoms = 0

                if isinstance(m, int):

                    m = (m, m, m)

                index_new = []

                for m2 in range(m[2]):

                    for m1 in range(m[1]):

                        for m0 in range(m[0]):

                            i1 = i0 + n

                            index_new += [i + natoms for i in self.index]

                            i0 = i1

                            natoms += n

                self.index = np.asarray(index_new, int)

                return self



            def delete_atoms(self, indices, natoms):

                """Removes atom number ind from the index array, if present.



                Required for removing atoms with existing FixAtoms constraints.

                """



                i = np.zeros(natoms, int) - 1

                new = np.delete(np.arange(natoms), indices)

                i[new] = np.arange(len(new))

                index = i[self.index]

                self.index = index[index >= 0]

                if len(self.index) == 0:

                    return None

                return self


        c = FixAtomsLine(direction=[0,0,1], mask=zr)

        zr.set_constraint(c)
        zr.set_calculator(pot)
        dyn = BFGS(zr)
#relax
        dyn.run(fmax=0.001)
#writes out raw data in file (needs to be separated into 21x21 grid to plot gamma surface)
        with open('energy.txt', 'a') as filehandle:
            filehandle.write('%s\n' % zr.get_potential_energy())

#reset strucutre
        zr=bulk('Zr', crystalstructure='hcp', a=3.23, c=5.16) * (5, 5, 10)
