from Astree import *

d=Device()
d.set_field_of_view(1.)

d.add_surface(Reflect())
d.add_surface(Ticks(1200.))
d.add_surface(Image())

iq=d.compute()

print(iq)