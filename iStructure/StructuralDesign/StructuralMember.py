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

class StructuralMember:
    #Abstract class with the general attributes and methods of the
    #structural members
    def __init__(self, long, section = None, sections = None, pos=np.zeros(2)):
        self.sections = sections    #All possible sections considered by the user
        self.long = long
        self.section = section      #Selected cross section
        self.pos = pos 
    
    @property
    def combinedLoad(self):
        loads = pd.DataFrame().append({"dead":0, "live":0, "product":0}, ignore_index=True)

        return loads

    def Selection(self):
        parent = self
        class Selection:
            #General selection procedure of the cross section of the structural member.
            consts = pd.DataFrame().append({"L":0, "Lx":0, "Ly":0, "Lt":0, "kx":0, "ky":0, "kt":0}, ignore_index=True)
            
            def __init__(self):
                self.parent = parent
                self.maxLoads()

            def maxLoads(self):
                print(self.parent.long)

            def axialStress():
                print("hola")

            def momentumStress():
                pass    

            def elasticBuckling():
                pass
        
        return Selection()
    
    def __call__(self):
        return self.section

if __name__ == "__main__":
    viga = StructuralMember(3)

    viga.Selection()

    print(viga.long)