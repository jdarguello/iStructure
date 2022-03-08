settings.outformat="pdf";
settings.render=16;
size(15cm, 0);

//Viga
real a,h;
a = 6;
h=0.8;
draw(box(0, (a,h)));

//Triángulo
real r = h/5;
real g = a/30;
real base, alt, init, xref;
xref = r+g;
init = 2*r;
base = 1.5;
alt = h;
fill((xref-base/2, -init) -- (xref, alt) -- (xref+base/2, -init) -- cycle, mediumgray);


//Pasadores
fill(circle((r + g,h/2), r), white);
draw(circle((r + g,h/2), r));
draw(circle((a-(r + g),-r), r));

//Suelo
void Suelo(real x, real y) {
    real ancho = 1.6;
    real sep = 0.2;
    real h = 0.2;
    draw((x,y) -- (x+ancho,y));
    real num_lin = round(ancho/sep);
    real suma = -sep;
    real suma_ant = -sep;
    for (int i=0; i<=num_lin; i=i+1) {
        suma = suma +sep;
        draw((x+suma_ant,y-h) -- (x+suma, y));
        suma_ant = suma;
    }
}
Suelo(xref-base/3 - 0.3,-init);
Suelo((a-(r+g))-(xref-base/2 + 0.8),-init);

/*
//Momentos
draw(arc((r+g,h/2), r=4*r, angle1=45+90, angle2=30), arrow=Arrow);
draw(arc((a-(r+g),h/2), r=4*r, angle1=30, angle2=45+90), arrow=Arrow);

//Label
label("$M_0$", (r+g,8*r));
label("$M$", (a-(r+g),8*r));
*/

//Carga distribuida
real flecha = 4*h/3;
real suma = r+g;
real num_flechas = 10;
for (int i=0; i<=num_flechas; i=i+1) {
    draw((suma,h+flecha) -- (suma,h), arrow=Arrow);
    suma = suma + (a-2*(r + g))/num_flechas;
}
draw((r+g,h+flecha) -- (a-(r + g),h+flecha), L=Label("$W$", position=MidPoint, align=N));

//Longitud
draw((r + g,-3*h/2) -- (r+g,-3*h/4));
draw((a-(r + g),-3*h/2) -- (a-(r + g),-3*h/4));
draw((r + g,-3*h/4-(3*h/2-3*h/4)/2) -- (a-(r + g),-3*h/4-(3*h/2-3*h/4)/2), arrow=Arrows(), L=Label("$\ell$", position=MidPoint, align=S));

//Nomenclatura
label("$A$", (r + g,h/2));
label("$B$", ((a-(r + g),-r)));

