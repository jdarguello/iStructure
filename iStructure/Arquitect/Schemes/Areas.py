# Copyright 2021 The iStructure Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
import numpy as np

class Module:
    #A mezzanine floor racking system consist of a series of modules. Each module is made of four columns, four beams
    #and a series of joists. 
    def __init__(self, length, width, height, joist_sep, pos):
        self.length = length
        self.width = width
        self.height = height
        self.joist_sep = joist_sep
        self.pos = pos              #Vector of two elements: [x,y] (width, length)

class Floor:
    #Made by a series of modules. A mezzanine floor racking system can be made by multiple floors. 
    #It has at least one floor.
    def __init__(self, modules=[], **kwargs):
        #Set the general dimensions of the mezzanine floor (genetic algorithm can be used in a next version to minimize cost of the structure)
        if "length" in kwargs and "width" in kwargs and "height" in kwargs:
            self.dims = pd.DataFrame().append({
                "length":kwargs["length"],
                "width":kwargs["width"],
                "height":kwargs["height"]
            }, ignore_index=True)
        else: 
            self.dims = pd.DataFrame().append({
                "length":0,
                "width":0,
                "height":0
            }, ignore_index=True)
        
            self.modules = []
            for module in modules:
                self.addModule(**module)
            
    def addModule(self, length, width, height, joist_sep, pos):
        #Check if the module to append is valid. A module is valid if the position (pos)
        #is unique and if width and length do not collide with other modules. Modules
        #collition can be produced in the horiontal or vertical direction. A difference
        #in height can, also, be considered a collition between floors. 

        #Modules can be registered in disorder.
        if len(self.modules) > 0:
            valid = height == self.modules[-1].height #A difference in height can not be tolerated
        else:
            #This is the first module to be registered
            valid = True
            self.dims['height'] = height

        if valid:
            #Registered module => coords
            coords = np.zeros((4,2))    #(x,y)
            #Module to be registered => mod_coords
            mod_coords = np.array([
                pos,                                #pos = (x,y)
                [pos[0] + width, pos[1]],
                [pos[0] + width, pos[1] + height],
                [pos[0], pos[1] + height]
            ])
            for module in self.modules:
                for i in range(4):
                    coords[i] = module.pos
                coords[1][0] += module.width
                coords[2][0] = coords[1][0]
                coords[2][1] +=  module.height
                coords[3][1] += module.height

                #Now, lets check if the new module is valid...
                #There are two ways for a collition to exist:
                #1. Module superposition
                c1 = mod_coords[0] <= coords[0]
                c2 = mod_coords[2] >= coords[1]
                if c1.all() and c2.all():
                    valid = False
                    break
                #2. A vertex is inside the registered module
                for i in range(4):
                    c1 = mod_coords[i] > coords[0]
                    c2 = mod_coords[i] < coords[2]
                    #import pdb; pdb.set_trace()
                    if c1.all() and c2.all():
                        #The vertex is inside the module's domain
                        valid = False
                        break
                
        if valid:
            self.modules.append(Module(length, width, height, joist_sep, pos))
            #Update dimensions of the floor
            if self.dims['width'][0] < pos[0] + width:
                self.dims['width'] = pos[0] + width
            if self.dims['length'][0] < pos[1] + length:
                self.dims['length'] = pos[1] + length

        else:
            raise ValueError("Module, in position {pos} and dimensions {dims}, is not valid because it overlaps with other modules.".format(pos=pos, dims=np.array([length, width])))

    def removeModule(self, pos):
        #'pos' referes to the modules original position
        for module in self.modules:
            if pos == module.pos:
                self.modules.remove(module)
                break

class Mezzanine:
    #Structure made by a series of floors.
    def __init__(self):
        self.floors = []

    def addFloor(self, **kwargs):
        self.floors.append(Floor(**kwargs))
    
    def addModule(self, numFloor, length, width, height, joist_sep, pos):
        self.floors[numFloor].addModule(length, width, height, joist_sep, pos)
    
    @property
    def dims(self):
        #Get the biggest dimensions of modules to the structural design analysis
        dims = pd.DataFrame().append({"length":0, "width":0, "height":0}, ignore_index=True)
        for floor in self.floors:
            for module in floor.modules:
                if module.length > dims["length"]:
                    dims["length"] = module.length
                if module.width > dims["width"]:
                    dims["width"] = module.width
                if module.height > dims["height"]:
                    dims["height"] = module.height
        return dims