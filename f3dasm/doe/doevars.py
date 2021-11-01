
#######################################################
# Data class for the manipulation and transformation  #
# of data within F3DASM                               #
#######################################################

"""
A dataclass for storing variables (features) during the DoE
"""

from dataclasses import dataclass
import numpy as np, array
from data import DATA
from typing import Optional
from abc import ABC

# using Optional
# attritube: Optional[optional-object] = None

@dataclass
class Material:
    """represents a material"""
    parameters: dict  # materials can be represeted a variable list of name:value pairs


@dataclass
class Geometry:
    """represents parametrized geometry"""
    parameters: dict  # materials can be represeted a variable list of name:value pairs


@dataclass
class BaseMicrosructure(ABC):
    """Represents a generic microstructue"""
    
    material: Material


@dataclass
class CircleMicrostructure(BaseMicrosructure):
    """Represents a microstructure for a circle"""

    diameter: any # can be a single value or a range of values
    shape: str = 'Circle'


@dataclass
class CilinderMicrostructure(BaseMicrosructure):
    """Represents a microstructure for """

    diameter: any # can be a single value or a range of values
    length: float
    shape: str = 'Cilinder'


@dataclass
class Imperfection:
    """Represents imperfections"""

    #TODO: define the class further, can we define subtypes?
    imperfections: dict # a list parameters defining an imperfection as name:value pairs


@dataclass
class Problem:
    material: Material

@dataclass
class REV(Problem):
    """Represents an Representative Elementary Volume"""
    
    Lc: float # characteristic length
    #material: Material
    microstructure: BaseMicrosructure
    dimesionality: int = 2 # e.g. 2D

@dataclass 
class Design(Problem):
    geometry: Geometry




@dataclass
class DoeVars:
    """Parameters for the design of experiments"""

    boundary_conditions: dict  # boundary conditions 
    #rev: REV
    problem : Problem
    imperfections: Optional[Imperfection] = None

    def info(self):

        """ Overwrite print function"""

        print('-----------------------------------------------------')
        print('                       DOE INFO                      ')
        print('-----------------------------------------------------')
        print('\n')
        print('Boundary conditions:',self.boundary_conditions)
        # print('REV dimensions:',self.rev.dimesionality)
        # print('REV Lc:',self.rev.Lc)
        # print('REV material:',self.rev.material.parameters)
        # print('Microstructure shape:',self.rev.microstructure.shape)
        # print('Microstructure material:',self.rev.microstructure.material.parameters)
        print('Imperfections:',self.imperfections)
        return '\n'

    # todo: convert values to array
    # todo: collect names for data colums
    # pass them on to data.py
    #TODO: implement own method to convert to pandas dataframe, use data.py as example
    
    def save(self,filename):

        """ Save experiemet doe points as pickle file
        
        Args:
            filename (string): filename for the pickle file
        
        Returns: 
            None
         """  

        data_frame = DATA(self.values,self.feature_names)       # f3dasm data structure, numpy array
        data_frame.to_pickle(filename)




def main():

    components= {'F11':[-0.15, 1], 'F12':[-0.1,0.15],'F22':[-0.15, 1]}
    mat1 = Material({'param1': 1, 'param2': 2})
    mat2 = Material({'param1': 3, 'param2': 4})
    micro = CircleMicrostructure(material=mat2, diameter=0.3)
    rev = REV(Lc=4,material=mat1, microstructure=micro, dimesionality=2)
    doe = DoeVars(boundary_conditions=components, rev=rev)

    print(doe)

    print(doe.info())


if __name__ == "__main__":
    main()