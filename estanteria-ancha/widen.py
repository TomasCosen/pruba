import trimesh,numpy as np,manifold3d as mf,sys
O=sys.argv[1]
def load(f):
    m=trimesh.load(f); t=m.bounds[0].copy(); m.apply_translation(-t); return m
# --- lateral (82 -> 112): extremos fijos, zona central estirada
def remap_side(x):
    a,b,d=9.9,72.1,30.0
    return np.where(x<=a,x,np.where(x>=b,x+d,a+(x-a)*(b-a+d)/(b-a)))
m=load('4a1eedb9-stackable-shelf-long-150mm.stl'); m.vertices[:,0]=remap_side(m.vertices[:,0])
m.export(f'{O}/stackable-shelf-long-150mm-112.stl'); print('side',m.extents)
for f,n in [('1051de45-stackable-shelf-long-cap-10mm.stl','stackable-shelf-long-cap-10mm-112.stl'),
            ('ccc3123c-stackable-shelf-long-feet-10mm.stl','stackable-shelf-long-feet-10mm-112.stl')]:
    m=load(f); x=m.vertices[:,0]; assert not ((x>10)&(x<72)).any()
    m.vertices[:,0]=np.where(x>41,x+30,x); m.export(f'{O}/{n}'); print(n,m.extents)
# --- estante (70 -> 100): duplicar 8 filas de hexagonos (28mm, periodo 7) y escalar 98->100
m=load('7e479075-long-shelf-hexagon-cutout-v2.stl'); m.merge_vertices()
M=mf.Manifold(mf.Mesh(vert_properties=m.vertices.astype(np.float32),tri_verts=m.faces.astype(np.uint32)))
box=lambda y0,y1: mf.Manifold.cube([300,y1-y0,20]).translate([-50,y0,-5])
c,P=35.0,28.0
A=M^box(-5,c); B=(M^box(c-P,c)).translate([0,P,0]); C=(M^box(c,80)).translate([0,P,0])
R=(A+B+C).scale([1,100/98,1])
mm=R.to_mesh(); t=trimesh.Trimesh(mm.vert_properties[:,:3],mm.tri_verts)
t.export(f'{O}/long-shelf-hexagon-cutout-v2-100.stl'); print('shelf',t.extents,t.is_watertight,len(t.split()))
