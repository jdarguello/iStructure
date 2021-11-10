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

from iStructure.Arquitect.Schemes.Areas import *
from matplotlib import lines
import pytest

class Test_Area:
    def setup_class(self):
        self.modulesInfo = [
            {
                "length":3,
                "width": 3, 
                "height": 3,
                "joist_sep":0.5,
                "pos": [0,0]
            },
            {
                "length":3,
                "width": 3.5, 
                "height": 3,
                "joist_sep":0.5,
                "pos": [3,0]
            }
        ]

        self.collidingModules = [
            #Vertex inside a module's domain
            [
                {
                    "length":3,
                    "width": 3, 
                    "height": 3,
                    "joist_sep":0.5,
                    "pos": [0,0]
                },
                {
                    "length":3,
                    "width": 3.5, 
                    "height": 3,
                    "joist_sep":0.5,
                    "pos": [0.2,0.5]
                }
            ],
            [
                {
                    "length":3,
                    "width": 3, 
                    "height": 3,
                    "joist_sep":0.5,
                    "pos": [2,3]
                },
                {
                    "length":3,
                    "width": 3.5, 
                    "height": 3,
                    "joist_sep":0.5,
                    "pos": [2.2,2.5]
                }
            ],
            [
                {
                    "length":3,
                    "width": 3, 
                    "height": 3,
                    "joist_sep":0.5,
                    "pos": [0,0]
                },
                {
                    "length":3,
                    "width": 3.5, 
                    "height": 3,
                    "joist_sep":0.5,
                    "pos": [-1,-1]
                }
            ],
            #Superposition of modules
            [
                {
                    "length":3,
                    "width": 3, 
                    "height": 3,
                    "joist_sep":0.5,
                    "pos": [0,0]
                },
                {
                    "length":3,
                    "width": 3.5, 
                    "height": 3,
                    "joist_sep":0.5,
                    "pos": [0,0]
                }
            ],
            [
                {
                    "length":3,
                    "width": 3, 
                    "height": 3,
                    "joist_sep":0.5,
                    "pos": [0,0]
                },
                {
                    "length":6,
                    "width": 7.5, 
                    "height": 3,
                    "joist_sep":0.5,
                    "pos": [-2,-3]
                }
            ],
            [
                {
                    "length":3,
                    "width": 3, 
                    "height": 3,
                    "joist_sep":0.5,
                    "pos": [0,0]
                },
                {
                    "length":3,
                    "width": 3.5, 
                    "height": 3,
                    "joist_sep":0.5,
                    "pos": [0,0]
                }
            ],
            [
                {
                    "length":3,
                    "width": 3, 
                    "height": 3,
                    "joist_sep":0.5,
                    "pos": [0,0]
                },
                {
                    "length":2,
                    "width": 3.5, 
                    "height": 3,
                    "joist_sep":0.5,
                    "pos": [0,0]
                }
            ],
            #Equally side inside of a module
            [
                {"length":3, "width":3, "height":2.5, "joist_sep":0.5, "pos": [0,0]},
                {"length":3, "width":3, "height":2.5, "joist_sep":0.5, "pos": [2,0]},
                {"length":3, "width":3, "height":2.5, "joist_sep":0.5, "pos": [6,0]},
                {"length":3, "width":3, "height":2.5, "joist_sep":0.5, "pos": [0,3]},
                {"length":3, "width":3, "height":2.5, "joist_sep":0.5, "pos": [3,3]},
                {"length":3, "width":3, "height":2.5, "joist_sep":0.5, "pos": [6,3]}
            ],
            
            [
                {"length":3, "width":3, "height":2.5, "joist_sep":0.5, "pos": [0,0]},
                {"length":3, "width":3, "height":2.5, "joist_sep":0.5, "pos": [3,2]},
                {"length":3, "width":3, "height":2.5, "joist_sep":0.5, "pos": [6,0]},
                {"length":3, "width":3, "height":2.5, "joist_sep":0.5, "pos": [0,3]},
                {"length":3, "width":3, "height":2.5, "joist_sep":0.5, "pos": [3,3]},
                {"length":3, "width":3, "height":2.5, "joist_sep":0.5, "pos": [6,3]}
            ]
        ]

        self.floors = [
            self.modulesInfo,
            [
                {
                    "length":3,
                    "width": 3, 
                    "height": 3,
                    "joist_sep":0.5,
                    "pos": [0,0]
                },
                {
                    "length":3,
                    "width": 3, 
                    "height": 3,
                    "joist_sep":0.5,
                    "pos": [0,3]
                }
            ]
        ]

    def test_module(self):
        for module in self.modulesInfo:
            assert isinstance(Module(**module), Module)

    
    def test_empty_floor(self):
        flr = Floor()
        assert len(flr.modules) == 0
    
    def test_nonColliding_modules_floor(self):
        flr = Floor(self.modulesInfo)
        assert len(flr.modules) == len(self.modulesInfo)
        assert flr.dims['height'][0] == 3
        assert flr.dims['length'][0] == 3
        assert flr.dims['width'][0] == 6.5

    def test_colliding_modules_floor(self):
        for modulesInfo in self.collidingModules:
            with pytest.raises(ValueError):
                Floor(modulesInfo)

    def test_removeModule(self):
        flr = Floor(self.modulesInfo)
        flr.removeModule([0,0]) #Remove first module
        assert flr.modules[0].pos == self.modulesInfo[1]['pos']
    
    def test_mezzanine_1empty_floor(self):
        mz = Mezzanine()
        mz.addFloor()
        assert mz.floors[0].modules == []
    
    def test_mezzanine_empty_floor(self):
        mz = Mezzanine()
        dims = pd.DataFrame().append({"length":0, "width":0, "height":0}, ignore_index=True)
        assert mz.dims["length"][0] == dims["length"][0]
    
    def test_mezzanine_floors(self):
        mz = Mezzanine()
        for floor in self.floors:
            mz.addFloor(modules = floor)
        assert mz.floors[0].modules[0].pos == self.floors[0][0]['pos']
    
    def test_design_dims(self):
        mz = Mezzanine()
        for floor in self.floors:
            mz.addFloor(modules = floor)
        dims = mz.dims
        assert dims['length'][0] == 3
        assert dims['width'][0] == 3.5
        assert dims['height'][0] == 3
        assert dims['joist_sep'][0] == 0.5
    
    def test_mezzanine_area_scheme_modules_1floor(self):
        mz = Mezzanine()
        mz.addFloor(modules = self.modulesInfo)
        fig = mz.scheme(False)
        ax = fig.axes[0]
        numLines = 0
        for child in ax.get_children():
            if isinstance(child, lines.Line2D):
                numLines += 1
        assert numLines/2 == 18.0
    
    def test_mezzanine_area_sheme_modules(self):
        mz = Mezzanine()
        for floor in self.floors:
            mz.addFloor(modules = floor)
        fig = mz.scheme(False)
        for ax in fig.axes:
            numLines = 0
            for child in ax.get_children():
                if isinstance(child, lines.Line2D):
                    numLines += 1
            assert numLines/2 == 18.0