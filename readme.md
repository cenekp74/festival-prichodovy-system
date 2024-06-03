Prichodovy system na GEKOM filmovy festival 2024

# Poznamky
- funkce add slouzi k pridani novych studentu pomoci post requestu. pouzivam ji proste tak, ze docasne odstranim @login_required, pridam co potrebuju a pak zase @login_required vratim.
## Editovani
- templaty souvisejici s editovanim jsou ve slozce edit/
- route /edit ukaze seznam trid
- route /edit/class/trida ukaze seznam zaku ve tride
- route /edit/student/student_id ukaze studenta spolecne s jeho tridou
- template edit_base.html je kvuli tomu, aby se do edit.html, edit_class.html a edit_student.html nemusel prepisovat vyber trid v levym sloupecku
## Search
- vyhledavani musi odlisne zobrazovat vysledky pro prohlizeni (pro ucitele) a pro editovani (v jednom musi byt odkaz na absenci studenta a ve druhem na editovani studenta)
- proto jsou v routs 2 fce na vyhledavani a obe pouzivaji stejny zaklad z utils.py
## Write
- samotne zapisovani prichodu jsem pojmenoval jednoduse write
- htmx posila post request fci write v routs.py
- ctecka rfid cipu funguje tak, ze se tvari jako klavesnice a proste zada 10 cislic a pak enter
## View
- sekce na zobrazovani prichodu
- view_class funguje podobne jako edit_class, s tim rozdilem, ze se vybira krome tridy jeste datum a proto je to udelany jako form
- view_student zobrazi pro daneho studenta prichody ve 3 festivalove dny (ty jsou definovane nahore v routs.py)