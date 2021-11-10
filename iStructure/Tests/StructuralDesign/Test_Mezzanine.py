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

from iStructure.Tests.CrossSections.Sections import FileSetup

class Test_StructuralMembers(FileSetup):
    def test_joistLength(self):
        assert self.joist.long == 3.2
        
    def test_joistLoads_table(self):
        table =  self.joist.Selection.combinedLoad()
        
    def test_beamLoads(self):
        pass