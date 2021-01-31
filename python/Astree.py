import numpy as np

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
    
    def remove_bad_photons(self):
        pass

#################################################################################################
class Surface:
    def __init__(self):
        pass

    def receive(self,light):
        pass

    def stop(self,light):
        pass

    def compute_normals(self,light):
        pass

class Ticks(Surface):
    def __init__(self,ticks):
        self.ticks=ticks
    
    def receive(self,light):
        light.x=light.x+self.ticks

class Reflect(Surface):
    def __init__(self,diameter=-1.,rc=-1.):
        self.diameter=diameter
        self.rc=rc

    def receive(self,light):
        self.stop(light)
        light.remove_bad_photons()
        n=self.compute_normals(light)
        #todo reflect using n

class Image(Surface):
    def __init__(self):
        pass

    def receive(self,light):
        self.stop(light)
        light.remove_bad_photons()

#################################################################################################
class ImageQuality:
    def __init__(self):
        self.lights=[]
        self.must_compute=True

    def add(self,l):
        self.lights.append(l)
        self.must_compute=True

    def compute(self):
        if self.must_compute==False:
            return
        #todo
        self.must_compute=False
#################################################################################################
