import json
import os

from iStructure.CrossSection.MechProp import CrossSection
from iStructure.CrossSection.MechProp import CrossSection 
from iStructure.Arquitect.Schemes.Areas import Mezzanine
from iStructure.StructuralDesign.Mezzanine.Members import *

"""
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
"""

class DB:
    def __init__(self, format="json"):
        import sectionproperties.pre.sections as sections
        rectHollow1 = sections.Rhs(d=102, b=102, t=2.5, r_out=5.4, n_r=8)
        meshRect1 = rectHollow1.create_mesh(mesh_sizes=[3.0])
        rectHollow2 = sections.Rhs(d=102, b=102, t=2.0, r_out=5.4, n_r=8)
        meshRect2 = rectHollow1.create_mesh(mesh_sizes=[3.0])

        iSec1 = sections.ISection(d=240, b=100, t_f=1.5, t_w=2.5, r=5, n_r=16)
        meshISec1 = iSec1.create_mesh(mesh_sizes=[2.0])

        CSec1 = sections.CeeSection(d=234, b=60, l=15, t=1.5, r_out=5.4, n_r=8)
        meshC1 = CSec1.create_mesh(mesh_sizes=[0.2])
        CSec2 = sections.CeeSection(d=234, b=60, l=15, t=2.5, r_out=5.4, n_r=8)
        meshC2 = CSec1.create_mesh(mesh_sizes=[0.2])

        self.format = format

        self.files = [
            ["MZJ23416", CSec1, meshC1], ["MZJ23412", CSec2, meshC2], ["MZB24016", iSec1, meshISec1],
            ["MZC10212", rectHollow1, meshRect1], ["MZC10214", rectHollow2, meshRect2]
        ]
        
        self.updateDB()

    def updateDB(self):
        files = os.listdir("iStructure/Tests/CrossSections/Files")
        for file in self.files:
            if not file[0] + "." + self.format in files:
                #File does not exist, create it...
                obj = CrossSection(file[1], file[2])
                obj.calculate_properties()
                with open("iStructure/Tests/CrossSections/Files/" + file[0] + "." + self.format, "w+") as newFile:
                    json.dump(obj(), newFile)
    
    def readDB(self):
        files = os.listdir("iStructure/Tests/CrossSections/Files")
        info = {"Columns":{}, "Beams": {}, "Joists": {}}
        for file in files:
            ref = file.replace("." + self.format, "")
            with open("iStructure/Tests/CrossSections/Files/" + file, "r") as rFile:  
                if ref[2] == "C":
                    info["Columns"][ref] = json.load(rFile)
                elif ref[2] == "B":
                    info["Beams"][ref] = json.load(rFile)
                elif ref[2] == "J":
                    info["Joists"][ref] = json.load(rFile)
        return info

class FileSetup:
    def setup_class(self):
        self.mz = Mezzanine()
        self.mz.addFloor(modules = [
            {
                "length":3,
                "width":3,
                "height":3,
                "joist_sep":0.5,
                "pos": [0,0]
            },
            {
                "length":3,
                "width":3.2,
                "height":3,
                "joist_sep":0.5,
                "pos": [3,0]
            }
        ])

        dims = self.mz.dims

        crud = DB()

        sections = crud.readDB()

        self.joist = Joist(dims, sections=sections["Joists"])
        self.beam = Beam(dims, sections=sections["Beams"])
        self.column = Column(dims, sections=sections["Columns"])

