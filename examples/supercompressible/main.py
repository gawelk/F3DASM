from f3dasm.doe.doevars import Design, DoeVars, Material, Geometry
#from 
import pandas as pd

#1 DOE
# bcs= {'F11':[-0.15, 1], 'F12':[-0.1,0.15],'F22':[-0.15, 1]}
# mat1 = Material({'young_modulus': 3500.,
#                     'shear_modulus': 1287.,})

# geometry = Geometry({'ratio_d': [0.004, 0.073],
#                     'ratio_pitch': [.25, 1.5],
#                     'ratio_top_diameter': [0., 0.8], 
#                     'bottom_diameter': 100.})

# design = Design(material= mat1, geometry= geometry)
# doe  = DoeVars(boundary_conditions= bcs, 
#                 problem = design)

#Specified as disctionary for now
doe_dict =   { 'material': {'young_modulus': 3500.,
                    'shear_modulus': 1287.,} , 
                
                'geometry' :{'ratio_d': [0.004, 0.073],
                            'ratio_pitch': [.25, 1.5],
                            'ratio_top_diameter': [0., 0.8], 
                            'bottom_diameter': 100.}, 
                'bcs' : {'F11':[-0.15, 1], 
                        'F12':[-0.1,0.15],
                        'F22':[-0.15, 1]}} 

#2 Simulator


#3 ML 


#4 Optimization