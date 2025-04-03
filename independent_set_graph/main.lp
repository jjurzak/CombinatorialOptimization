% Załóżmy, że graf nieskierowany jest zadany za pomocą predykatów vertex
% oraz edge. Zaproponuj program logiczny wyznaczający maksymalny zbiór niezależny.
% (https://en.wikipedia.org/wiki/Independent_set_(graph_theory))
% Jakub Jurzak 59099

 
% wierzchołki
vertex(a).
vertex(b).
vertex(c).
vertex(d).
vertex(e).
vertex(f).

% krawędzie
edge(a,b).
edge(b,c).
edge(c,d).
edge(d,e).
edge(e,f).
edge(b,f).

{ in(X) : vertex(X) }.

:- in(X), in(Y), edge(X,Y).

% Funkcja celu
#maximize { 1,X : in(X) }.

neighbor_in(X) :- edge(X,Y), in(Y).
neighbor_in(X) :- edge(Y,X), in(Y).

#show in/1.