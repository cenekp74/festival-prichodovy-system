Prichodovy system na GEKOM filmovy festival 2024

# Poznamky
- funkce add slouzi k pridani novych studentu pomoci post requestu. pouzivam ji proste tak, ze ji docasne pridam do vyjimek ve funkci require_login, pridam co potrebuju a pak vyjimku odstranim
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
### Sekundarni server
- je moznost nastavit secondary server (v `__init__.py`), na ktery se bude posilat stejny post request
- sekundarni server pobezi jako presna kopie tohohle na jinym vps pro pripad, ze by primarni vps prestal fungovat
- na sekundarnim serveru by mel byt nastaveny jako sekundarni ten primarni
- v pripade vypadku 1. serveru se proste prejde na 2., pokud vse funguje jak ma tak tam budou stejny prichody jako byly na 1.
## View
- sekce na zobrazovani prichodu
- view_class funguje podobne jako edit_class, s tim rozdilem, ze se vybira krome tridy jeste datum a proto je to udelany jako form
- view_student zobrazi pro daneho studenta prichody ve 3 festivalove dny (ty jsou definovane nahore v routs.py)
## Zalohy
### lokalni
- pri cipovani (write) si muze client vybrat, ze chce ukladat lokalni zalohy
- lokalni zaloha znamena, ze po kazdych n cipnutich se stahne json soubor s casy a rfid vsech naskenovanych cipu
- pocet prichodu, po kterych se ma ukladat zaloha je definovany v write.js
- POZOR - pokud se zaloha uklada napr. po kazdych 5 cipnutich, cipnu 4krat a pak reloadnu, ZALOHA SE NEVYTVORI a data se neulozi do localu => napr. na konci cipovani se nejspis neulozi
### na serveru
- fce view_json vrati vsechny prichody v json formatu. takhle se da bud rucne nebo automaticky stahovat databaze a nekam zalohovat (muze napr. na pocitaci v IVT bezet script a 
### secondary server
- zaroven bezi 2 servery, write requesty se posilaji na oba
- je s tim hrozne srani s cross-origin pravidlama, vede to ke spouste odpornosti v kodu (napr. to, ze je nekolikrat na pevno dana adresa url obou serveru...)
kazdych par minut stahnout zalohu)
## Login
- standartni flask login pres wtforms, zkopirovany ze staryho projektu
- v before request je (docela hnusne) definovany, kdy je potreba login a kdy ne - chtelo by to predelat