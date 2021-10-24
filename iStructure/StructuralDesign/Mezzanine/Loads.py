from math import ceil

class CombinedLoad():
    """
        Combined load calculus for all of the structural members.
    """
    kind_loads = ['dead', 'live', 'product']
    def __init__(self, Secciones, Inicio, member='Joists', ganador=None, muerte_vigas = None):
        #Initialize
        self.Combined_Loads = {}
        self.Loads, self.Dist_Loads = self.Variables(Secciones, member)

        #Calcular
        self.Calc(Secciones, Inicio, member, ganador, muerte_vigas)

    def Calc(self, Secciones, Inicio, member, ganador, muerte_vigas):
        #---LOADS---
        #... per kind of member (column, beam or joist)
        if member == 'Columns':
            #Module area
            Area = Inicio['Long_Viga']*\
                    Inicio['Long_Vigueta']
            L = float(Inicio['Height'])
            precarga = muerte_vigas*Area
            mult = Area*(5/4)
        elif member == 'Beams':
            L = Inicio['Long_Viga']
            #Module area
            Area = Inicio['Long_Viga']*\
                    Inicio['Long_Vigueta']
            peso_vigueta = Secciones['Joists'][ganador]['Full Section Properties']['Wt.']['Value']*(1000/9.81)*Inicio['Long_Vigueta']
            Num_Viguetas = ceil(Inicio['Long_Viga']/Inicio['Sep'])
            precarga = peso_vigueta*Num_Viguetas
            mult = L
        else:
            L = Inicio['Sep']
            #Module area
            Area = Inicio['Long_Viga']*\
                    Inicio['Sep']
            precarga = 0
            mult = L
        #... per reference
        for reference, value in Secciones[member].items():
            #... per kind of load
            for kind in self.kind_loads:
                anss = {}
                if kind == 'dead':
                    A = Secciones[member][reference]\
                        ['Full Section Properties']['Area']['Value']*\
                            (1/(1000**2))
                    ANS = Secciones[member][reference]['Full Section Properties']\
                        ['Wt.']['Value']*L*(1000/(Inicio['g']['Value']))+precarga
                elif kind == 'live':
                    ANS = 293*0.3
                elif kind == 'product':
                    ANS = Inicio['Load']*Area - \
                    (self.Loads[reference]['dead']['Value']+\
                    self.Loads[reference]['live']['Value'])
                """
                ans['Value'] = round(
                    ANS*Inicio['g']['Value']/1000,
                    3
                )
                ans['Units'] = 'kN'
                """
                anss['Value'] = ANS
                anss['Units'] = 'kg'
                self.Loads[reference][kind] = anss
                self.Dist_Loads[reference][kind] = {
                    'Value': round(ANS/Area, 3),
                    'Units': 'kg/m2'
                }
                #print(self.Dist_Loads[kind][member][reference])
            ans = {}
            D = self.Dist_Loads[reference]['dead']['Value']
            Liv = self.Dist_Loads[reference]['live']['Value']
            P = self.Dist_Loads[reference]['product']['Value']
            ans['Value'] = round(
                (1.2*D + 1.4*P + 1.6*Liv)*(9.81/1000)*mult,
                3
            )
            ans['Units'] = 'kN/m'
            self.Combined_Loads[reference] = ans

    def Variables(self, Secciones, member):
        Loads = {}
        Dist_Loads = {}
        for ref in Secciones[member]:
            Loads[ref] = {}
            Dist_Loads[ref] = {}
            for kind in self.kind_loads:
                Loads[ref][kind] = {}
                Dist_Loads[ref][kind] = {}
        return Loads, Dist_Loads

    def __call__(self):
        return self.Loads, self.Dist_Loads, self.Combined_Loads