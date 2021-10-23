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

class UnitSystems:
    #
    pass

class Material:
    #Contains the base mechanical properties of the selected material.
    #International System of Units is taken as base system. Other system of units can be implemented, 
    # but must be converted to the international system for calculation purposes.
    unitSystems = UnitSystems()
    def __init__(self, density, young_modulus, poisson, yieldStrength, ultStrength, Units="SI"):
        #Setting attributes values
        self.density = density
        self.young_modulus = young_modulus
        self.poisson = poisson
        self.yieldStrength = yieldStrength
        self.ultStrength = ultStrength

class CrossSection(Material):
    #Specify general information of the cross section. 
    def __init__(self, material, Units="SI"):
        super(CrossSection, self).__init__(**material.__dict__)

if __name__ == '__main__':
    acero = Material(0,0,0,0,0)

    I = CrossSection(acero)

    print(I.__dict__)