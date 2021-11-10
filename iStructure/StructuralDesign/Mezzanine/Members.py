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
from iStructure.StructuralDesign.StructuralMember import StructuralMember

class Joist(StructuralMember):
    def __init__(self, designDims, section = None, sections = None, pos=np.zeros(2)):
        super().__init__(designDims['width'][0], section, sections, pos)
    
    class Selection(StructuralMember.Selection):
        def __init__(self, parent):
            #'parent' refers to the base structural member class
            super().__init__(parent)

        def combinedLoad(self):
            super().combinedLoad()

        def axialStress(self):
            super().axialStress()
        
        def momentumStress(self):
            StructuralMember.Selection.momentumStress(self) 
            print("Ohh")

        def elasticBuckling(self):
            pass

class Beam(StructuralMember):
    def __init__(self, designDims, section = None, sections = None, pos=np.zeros(2)):
        super().__init__(designDims['length'][0], section, sections, pos)
    
    class Selection(StructuralMember.Selection):
        def __init__(self, parent):
            #'parent' refers to the base structural member class
            StructuralMember.Selection.__init__(self, parent)

        def combinedLoad(self):
            StructuralMember.Selection.combinedLoad(self)

        def axialStress(self):
            StructuralMember.Selection.axialStress(self)
        
        def momentumStress(self):
            StructuralMember.Selection.momentumStress(self) 
            print("Ohh")

        def elasticBuckling(self):
            pass

class Column(StructuralMember):
    def __init__(self, designDims, section = None, sections = None, pos=np.zeros(2)):
        super().__init__(designDims['height'][0], section, sections, pos)
    
    class Selection(StructuralMember.Selection):
        def __init__(self, parent):
            #'parent' refers to the base structural member class
            StructuralMember.Selection.__init__(self, parent)

        def combinedLoad(self):
            StructuralMember.Selection.combinedLoad(self)

        def axialStress(self):
            StructuralMember.Selection.axialStress(self)
        
        def momentumStress(self):
            StructuralMember.Selection.momentumStress(self) 
            print("Ohh")

        def elasticBuckling(self):
            pass