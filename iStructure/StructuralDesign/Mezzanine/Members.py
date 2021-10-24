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

class StructuralMember:
    #Abstract class with the general attributes and methods of all the
    #structural members
    def __init__(self, sections, long):
        self.sections = sections    #All possible sections considered by the user
        self.long = long
        self.section = None         #Selected cross section 
    
    def combinedLoad(self):
        loads = pd.DataFrame().append({"dead":0, "live":0, "product":0}, ignore_index=True)
    
    class Selection:
        #General selection procedure of the cross section of the structural member.
        def axialStress(self):
            pass

        def momentumStress(self):
            pass    

        def elasticBuckling(self):
            pass

class Beam(StructuralMember):
    pass

class Joist(StructuralMember):
    pass

class Column(StructuralMember):
    pass