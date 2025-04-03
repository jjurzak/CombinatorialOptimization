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



% Zgadywanie zbioru niezależnego: dla każdego wierzchołka decydujemy, czy należy on do zbioru.
{ in(X) : vertex(X) }.

% Ograniczenie niezależności: dwa sąsiadujące wierzchołki nie mogą być jednocześnie w zbiorze.
:- in(X), in(Y), edge(X,Y).

% Funkcja celu: maksymalizujemy liczbę wierzchołków w zbiorze niezależnym.
#maximize { 1,X : in(X) }.

% Predykat określający, że wierzchołek X ma sąsiada w zbiorze.
neighbor_in(X) :- edge(X,Y), in(Y).
neighbor_in(X) :- edge(Y,X), in(Y).

#show in/1.