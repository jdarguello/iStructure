from iStructure.Arquitect.Schemes.Areas import *
#from unittest import TestCase
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
                    "pos": [3,0]
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