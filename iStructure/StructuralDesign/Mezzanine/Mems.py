import numpy as np
from IPython.display import Markdown, display
import pandas as pd

class Selection():
    """
        Selección de miembros estructurales
    """
    selec = {}
    def __init__(self, Loads, Data, Cross_Sections, member="Joists"):
        def Valor(ref, nombre, val, un):
            dic[ref][nombre] = {}
            dic[ref][nombre]['Value'] = val
            dic[ref][nombre]['Units'] = un
        #...Members
        dic = {}
        if member == 'Columns':
            L = float(Data['Height'])
            Lx = L
            Ly = Lx
            Lt = Ly
            kx = 1.3
            ky = 1.2
            kt = 1.0
        elif member == 'Beams':
            L = Data['Long_Viga']
            Ly = Data['Sep']
            Lx = L
            Lt = Ly
            kx = 1
            ky = kx
            kt = ky
        else:
            L = Data['Long_Vigueta']
            Ly = L
            Lx = L
            Lt = Lx
            kx = 1
            ky = kx
            kt = ky
        #...Reference
        for reference, value in Loads[member].items():
            dic[reference] = {}
            #Cargas máximas
            Mu = (Loads[member][reference]['Value']*L**2)/8
            Valor(reference, 'Mu', Mu, 'kN*m')
            Vu = (Loads[member][reference]['Value']*L)/2
            Valor(reference, 'Vu', Vu, 'kN')
            #Resistencia
            Valor(reference, 'Ly', Ly, 'm')
            Valor(reference, 'Lx', Lx, 'm')
            Valor(reference, 'Lt', Lt, 'm')
            Valor(reference, 'kx', kx, '')
            Valor(reference, 'ky', ky, '')
            Valor(reference, 'kt', kt, '')
            r_y = Cross_Sections[member][reference]['Full Section Properties']['ry']
            Valor(reference, 'r_y', r_y['Value'], r_y['Units'])
            A = Cross_Sections[member][reference]['Full Section Properties']['Area']
            Valor(reference, 'A', A['Value'], A['Units'])
            r_0 = Cross_Sections[member][reference]['Full Section Properties']['ro']
            Valor(reference, 'r_0', r_0['Value'], r_0['Units'])
            c_w = Cross_Sections[member][reference]['Full Section Properties']['Cw']
            Valor(reference, 'c_w', c_w['Value'], c_w['Units'])
            J = Cross_Sections[member][reference]['Full Section Properties']['J']
            Valor(reference, 'J', J['Value'], J['Units'])
            r_x = Cross_Sections[member][reference]['Full Section Properties']['rx']
            Valor(reference, 'r_x', r_x['Value'], r_x['Units'])
            if member == 'Columns':
                x0 = Cross_Sections[member][reference]['Full Section Properties']['xo -']
                Valor(reference, 'x0', x0['Value'], x0['Units'])
                Ae = Cross_Sections[member][reference]['Fully Braced Strength - 2016 North American Specification - US (LRFD)']['Ae']
                Valor(reference, 'Ae', Ae['Value'], Ae['Units'])
            #Sf, Sc, Fy
            Sf = Cross_Sections[member][reference]['Full Section Properties']['Sx(t)']
            Valor(reference, 'Sf', Sf['Value'], Sf['Units'])
            Sc = Cross_Sections[member][reference]['Fully Braced Strength - 2016 North American Specification - US (LRFD)']['Sxe(t)']
            Valor(reference, 'Sc', Sc['Value'], Sc['Units'])
            Fy = Cross_Sections[member][reference]['Calculation Details - 2016 North American Specification - US (LRFD)']['Positive Flexural Strength about X-axis'][' Fy']
            Valor(reference, 'Fy', Fy['Value'], Fy['Units'])
            
        self.selec[member] = dic
        self.selec[member]['Winners'] = [] 
        #---Esfuerzos---
        for reference, value in Loads[member].items():
            self.selec[member][reference]['sigma'] = {}
            self.selec[member][reference]['sigma']['sigma_ex'], self.selec[member][reference]['sigma']['sigma_ey'], self.selec[member][reference]['sigma']['sigma_t']= self.PandeoEl(self.selec[member][reference], Data)
            
            if member != 'Columns':
                #Resistancia a la flexión
                self.selec[member][reference]['Flexion'] = {}
                self.selec[member][reference]['Flexion']['F_e'], self.selec[member][reference]['Flexion']['F_c'] = self.Flexion(self.selec[member][reference])

                self.selec[member][reference]['Flexion']['My'], self.selec[member][reference]['Flexion']['Mn'], self.selec[member][reference]['Flexion']['phi'], self.selec[member][reference]['Flexion']['MT'] = self.FlexMomentos(self.selec[member][reference])
                
                if self.selec[member][reference]['Flexion']['MT'] >= Mu:
                    self.selec[member]['Winners'].append(reference)
            else:
                #Es columna (carga axial predominante, no flectora)
                self.selec[member][reference]['Axial'] = {}
                self.selec[member][reference]['Axial']['beta'], self.selec[member][reference]['Axial']['sigma_ft'], self.selec[member][reference]['Axial']['Fe'], self.selec[member][reference]['Axial']['lamda_c'], self.selec[member][reference]['Axial']['Fn'], self.selec[member][reference]['Axial']['Pn'], self.selec[member][reference]['Axial']['Phi'] = self.Axial(self.selec[member][reference])
                if self.selec[member][reference]['Axial']['Pn'] >= Loads[member][reference]['Value']:
                    self.selec[member]['Winners'].append(reference)

        self.win, self.winner = self.ImprimirGanador(self.selec[member]['Winners'], Cross_Sections[member])
    
    def Axial(self, info):
        #print(info)
        beta = 1-(info['x0']['Value']/info['r_0']['Value'])**2
        sigma_ft = (1/(2*beta))*((info['sigma']['sigma_ex']+info['sigma']['sigma_t'])-np.sqrt((info['sigma']['sigma_ex']+info['sigma']['sigma_t'])**2-4*beta*info['sigma']['sigma_ex']*info['sigma']['sigma_t']))
        Fe = min(info['sigma']['sigma_ex'], info['sigma']['sigma_ey'], info['sigma']['sigma_t'],sigma_ft)
        lambda_c = np.sqrt(info['Fy']['Value']/Fe)
        
        if lambda_c <= 1.5:
            Fn = (0.658**(lambda_c**2))*info['Fy']['Value']
        else:
            Fn = (0.877/lambda_c**2)*info['Fy']['Value']
        Pn = info['Ae']['Value']*Fn/1000
        phi = 0.85
        Pn = phi*Pn
        return beta, sigma_ft, Fe, lambda_c, Fn, Pn, phi
        
    def ImprimirGanador(self, ganadores, secciones):
        secs = {"Reference":[], "Satisfactory?":[]}
        if len(ganadores) > 0:
            #Ganador absoluto (más barato = menos material)
            gganador = ganadores[0]
            for g in ganadores:
                if secciones[gganador]['Full Section Properties']['Area']['Value'] > secciones[g]['Full Section Properties']['Area']['Value']:
                    gganador = g
            #Ganadores
            index = -1
            suma = 0
            for ref in ganadores:
                if ref == gganador:
                    index = suma
                secs["Reference"].append(ref)
                secs["Satisfactory?"].append("O")
                suma += 1
        else:
            #No hay ganadores
            gganador = ''
            index = -1
        #Perdedores
        for key in secciones:
            ganador = False
            for ref in ganadores:
                if ref == key:
                    ganador = True
            if not ganador:
                secs["Reference"].append(key)
                secs["Satisfactory?"].append("X")
        #Imprime
        g = pd.DataFrame(secs)
        return g, [gganador, index]        
            
    def FlexMomentos(self, info):
        My = info['Sc']['Value']*info['Fy']['Value']/(10**6)
        Mn = info['Sf']['Value']*info['Flexion']['F_c']/(10**6)
        if Mn > My:
            Mn = My
        if info['Flexion']['F_c'] == info['Fy']['Value']:
            phi = 0.95
        else:
            phi = 0.9
        MT = phi*Mn
        return My, Mn, phi, MT

    def Flexion(self, info):
        Cb = 1
        F_c = ((Cb*info['r_0']['Value']*info['A']['Value'])/info['Sf']['Value'])*np.sqrt(info['sigma']['sigma_ey']*info['sigma']['sigma_t'])

        if F_c >= 2.78*info['Fy']['Value']:
            F_n = info['Fy']['Value']
        elif F_c <= 0.56*info['Fy']['Value']:
            F_n = F_c
        else:
            F_n = (10/9)*info['Fy']['Value']*(1-((10*info['Fy']['Value'])/(36*F_c)))
        return F_c, F_n
    
    def PandeoEl(self, info, Init):
        #print(info)
        sigma_ex = ((np.pi**2)*Init['E']['Value']*1000)/((info['kx']['Value']*info['Lx']['Value']*1000/info['r_x']['Value'])**2)
        sigma_ey = ((np.pi**2)*Init['E']['Value']*1000)/((info['ky']['Value']*info['Ly']['Value']*1000/info['r_y']['Value'])**2)
        sigma_t = (1/(info['A']['Value']*info['r_0']['Value']**2))*(Init['G']*info['J']['Value']+(((np.pi**2)*Init['E']['Value']*1000*info['c_w']['Value'])/((info['kt']['Value']*info['Lt']['Value']*1000)**2)))
        return sigma_ex, sigma_ey, sigma_t

    def __call__(self):
        return self.selec