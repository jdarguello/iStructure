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

from sectionproperties.analysis.cross_section import CrossSection as Section
import pandas as pd

class UnitSystems:
    #
    pass


class CrossSection(Section):
    #Specify general information of the cross section; including material and geometry.
    def __init__(self, geometry, mesh, name = "", materials=None, time_info=False, units="SI"):
        super(CrossSection, self).__init__(geometry, mesh, materials, time_info)
        self.name = name
    
    def get_geometry(self):
        return self.geometry
    
    def calculate_properties(self):
        self.calculate_geometric_properties()
        #self.calculate_warping_properties()
        #self.calculate_plastic_properties()
    
    def read_properties (self, fileFormat="json"):
        pass

    def __call__(self):
        return self.section_props.__dict__