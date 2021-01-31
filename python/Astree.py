import numpy as np

INFINITE=9.e999
NB_LIGHT=3 # from center to edge
YELLOW=560.e-9# 560 nanometers

#################################################################################################
class Device:
    def __init__(self):
        self.surfaces=[]
        self.fov=0.
        self.must_recompute=True

    def add_surface(self,s):
        self.surfaces.append(s)
        self.must_recompute=True

    def set_field_of_view(self,fov,nb_angles=3):
        self.fov=fov
        self.nb_angles=nb_angles
        self.must_recompute=True

    def compute(self):

        iq=ImageQuality()

        for tilt in np.linspace(0,self.fov/2.,self.nb_angles):
            l=Light(self.surfaces[0].diameter,tilt)
            for s in self.surfaces:
                s.receive(l)
            iq.add(l)

        # compute Image Quality
        return iq

#################################################################################################
class Light:
    def __init__(self,diameter,tilt, nb_photons=31):
        nb_total=nb_photons*nb_photons
        self.tilt=tilt # todo
        self.dx=np.zeros(nb_total)
        self.dy=np.zeros(nb_total)
        self.dz=np.ones(nb_total)
        
        xd=np.linspace(-diameter,diameter,nb_photons)
        yd=np.linspace(-diameter,diameter,nb_photons)
        self.x,self.y=np.meshgrid(xd,yd)
        self.z=np.zeros(nb_total)
        self.valid=np.ones(nb_total)
        self.wavelenght=np.ones(nb_total)*YELLOW
        self.index=np.ones(nb_total)

#################################################################################################
class Surface:
   
    def __init__(self):#,surf_type,rcurv,diameter):
        pass
        # self.type=surf_type
        # self.rcurv=rcurv
        # self.diameter=diameter

    def receive(self,light):
        pass
    
        # if self.type=="stop" :
        #     self.stop(light)

        # if self.type=="reflect" :
        #     self.reflect(light)

        # if self.type=="transmit" :
        #     self.transmit(light)

    def stop(self,light):
        pass

    def reflect(self,light):
        self.stop(light)
       # nrm=self.compute_normals(light)
        pass

    def transmit(self,light):
        self.stop(light)
        #nrm=self.compute_normals(light)
        pass

    def compute_normals(self,light):
        pass


class Ticks(Surface):
    def __init__(self,ticks):
        self.ticks=ticks

class Reflect(Surface):
    def __init__(self,diameter=-1.):
        self.diameter=diameter
        pass

class Image(Surface):
    def __init__(self):
        pass

#################################################################################################
class ImageQuality:
    def __init__(self):
        self.lights=[]
        pass

    def add(self,l):
        self.lights.append(l)

 

#################################################################################################
