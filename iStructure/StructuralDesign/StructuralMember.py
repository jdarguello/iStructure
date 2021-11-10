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

        self.Selection = self.Selection(self)   #Creates child class "Selection", which has all the attributes and methods required for
                                                #the specific structural design procedure

    class Selection:
        #General selection procedure of the cross section of the structural member.
        #Child class of the structural member.
        def __init__(self, parent):
            self.consts = pd.DataFrame().append({"L":parent.long, "Lx":0, "Ly":0, "Lt":0, "kx":0, "ky":0, "kt":0}, ignore_index=True)
            self.sections = parent.sections
            self.section = None     #Best section
        
        def designProcedure(self):
            #0. Check that the sections has been defined
            if self.sections is None:
                raise AttributeError("To proceed with the structural design, you should provide the sections of the structural member.")

            #1. Calculate the combined loads => the design dataframe is created and will contain all the structural design information of the member
            self.combinedLoad()

            #2. Calculate the axial stress

            #3. Calculate momentum stress

            #4. Calculate elastic buckling

            #5. Calculate Von Misses stress

            #6. Select the best section and bring a summary of results

        def combinedLoad(self):
            #design DataFrame preparation
            long = np.zeros(len(self.sections))
            self.designDF = pd.DataFrame(data = {
                "Cross Section": np.array([*self.sections]),
                "Dead": long,
                "Live": long,
                "Product": long
            })

            dataValues = lambda t: np.array([rawInfo[t] for rawInfo in self.sections.values()])
            info = pd.DataFrame(data = {key:dataValues(key) for key in [*self.sections[next(iter(self.sections))]]})
            self.designDF = pd.concat([self.designDF, info], axis=1)    

            self.designDF = self.designDF.loc[:, self.designDF.notna().any(axis=0)] #Delete all of the null values

            #Loads calculation

        def axialStress(self):
            print("Ble")

        def momentumStress(self):
            print("Holala")    

        def elasticBuckling(self):
            pass
    
        def __call__(self):
            return self.section