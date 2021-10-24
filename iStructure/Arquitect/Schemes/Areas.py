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
    def __init__(self, modules=None, **kwargs):
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
        #is unique and if width and length do not collide with other modules
        valid = True
        #for module in self.modules:
        
        if valid:
            self.modules.append(Module(length, width, height, joist_sep, pos))
        else:
            raise ValueError("Module, in position {pos} and dimensions {dims}, is not valid because it overlaps with other modules.".format(pos=pos, dims=[length, width]))

    def removeModule(self, pos):
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