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
                l.remove_bad_photons()
            iq.add(l)

        return iq

#################################################################################################
class Light:
    def __init__(self,diameter,tilt, nb_photons=31):
        self.nb_photons=nb_photons*nb_photons
        self.tilt=tilt # todo
        self.dx=np.zeros(self.nb_photons)
        self.dy=np.zeros(self.nb_photons)
        self.dz=np.ones(self.nb_photons)
        
        xd=np.linspace(-diameter,diameter,nb_photons)
        yd=np.linspace(-diameter,diameter,nb_photons)
        self.x,self.y=np.meshgrid(xd,yd)
        self.x=np.reshape(self.x,self.nb_photons)
        self.y=np.reshape(self.y,self.nb_photons)
        self.z=np.zeros(self.nb_photons)
        self.valid=np.ones(self.nb_photons)
        self.wavelength=np.ones(self.nb_photons)*YELLOW
        self.index=np.ones(self.nb_photons)
    
    def remove_bad_photons(self):
        to_delete = (self.valid ==0)
        self.dx=np.delete(self.dx,to_delete,axis=0)
        self.dy=np.delete(self.dy,to_delete,axis=0)
        self.dz=np.delete(self.dz,to_delete,axis=0)
        self.x=np.delete(self.x,to_delete,axis=0)
        self.y=np.delete(self.y,to_delete,axis=0)
        self.z=np.delete(self.z,to_delete,axis=0)
        self.wavelength=np.delete(self.wavelength,to_delete,axis=0)
        self.index=np.delete(self.index,to_delete,axis=0)
        self.valid=np.delete(self.valid,to_delete,axis=0)

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

class Stop(Surface):
    def __init__(self,diameter=-1.):
        self.diameter=diameter

    def receive(self,light):
        self.stop(light)
        light.remove_bad_photons()

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
