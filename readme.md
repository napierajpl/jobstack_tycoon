Pierwotny prompt dla Chata GPT

Poniżej jest projekt gry, którą należy napisać w Pythonie używając klas i metod i zasad OOP.

Customer
Pojawia się co turę z potrzebą zatrudnienia X pracusiów na Y dni. Ma na to określone widełki budżetowe (Z). Maksymalna stawka, którą jest gotów zapłacić za godzinę pracy i minimalna.
Jeden dzień to 8 godzin pracy
X = 1 do 50, ale 80% przypadków to 1 do 10
Y = 1 do 14
Z min. = 10 do 15
Z max = 15 do 25
Z min musi być zawsze mniejsze od Z max

Gracz ma zaproponować ile customer musi zapłacić za godzinę pracy pracusia ryzykując, że nie dojdzie do kontraktu. 

Worker (pracuś)
Pojawia się i przegląda oferty pracy. swoje widełki zarobkowe za które gotów jest pracować.
Możemy mu zaproponować robotę. 
Z min. = 8 do 14
Z max = nieograniczone - im więcej tym lepiej
Z min musi być zawsze mniejsze od Z max

Gra opiera się o tury. W każdej turze następują wydarzenia
- losowany jest customer o konkretnych parametrach, który przychodzi z zapotrzebowaniem na pracusiów
- gracz proponuje bill rate i pay rate
- customerzy zgadzają się na stawki i oferta idzie do pracusia (ew. oferta jest odrzucana przez customera)
- losowani są pracusie z ich parametrami, którzy decydują się na pracę lub nie
- odbywa się tura pracy
- gracz płaci pracusiom i wystawia fakturę customerowi
- Gracz zatrzymuje różnicę między pay rate a bill rate. To jest jego wynik (score). Jeśli nie dojdzie do pracy bo customer nie zaakceptuje warunków lub żaden pracuś się nie zgodzi pracować - score = 0
- Przechodzimy do kolejnej tury. 

Odpowiadaj po angielsku




