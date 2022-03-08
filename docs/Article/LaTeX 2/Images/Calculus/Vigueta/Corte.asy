settings.outformat="pdf";
settings.render=16;
size(10cm, 0);

//Viga
real a,h;
a = 0.6;
h=0.2;
draw(box(0, (a,h)));

//FA
draw((0,-2*h/3)--(0,0), arrow=Arrow, L=Label("$\vec{F_A}$", position=BeginPoint, align=S));

/*
//Momentos
draw(arc((r+g,h/2), r=4*r, angle1=45+90, angle2=30), arrow=Arrow);
draw(arc((a-(r+g),h/2), r=4*r, angle1=30, angle2=45+90), arrow=Arrow);

//Label
label("$M_0$", (r+g,8*r));
label("$M$", (a-(r+g),8*r));
*/

//W
real flecha = h;
draw((a/2,h/2) -- (a/2,h/2-flecha), arrow=Arrow, L=Label("$W x$", position=EndPoint, align=S));
draw((0,-flecha/4) -- (a/2,-flecha/4), arrow=Arrows(), L=Label("$\frac{x}{2}$", position=MidPoint, align=S));
fill(circle((a/2,h/2), h/40));

//x
draw((a, h) -- (a, h+flecha));
draw((a,h+flecha/2) -- (2*a/3,h+flecha/2), arrow=Arrow, L=Label("$x$", position=EndPoint, align=W));

//Cortantes
draw((41*a/40, 41*h/40) -- (41*a/40, -h/40), arrow=Arrow, L=Label("$\vec{V}$", position=EndPoint, align=S));
draw(arc((a,2*h/3), r=2*h/3, angle1=-30, angle2=45+90), arrow=Arrow, L=Label("$\vec{M}$", position=MidPoint, align=E));