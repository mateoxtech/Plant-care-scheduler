<!-- Web aplikacija koja omogućuje korisniku upravljanje sobnim biljkama i njihovim rasporedom zalijevanja. -->

# Plant care scheduler
Plant care scheduler je web aplikacija koja omogućuje korisnicima upravljanje sobnim biljkama i da pomoću web aplikacije upravljaju njihovim rasporedom zalijevanja. Glavne funkcionalnosti ove web aplikacije su da pomoću nje korisnici prate i upravljaju svim potrebnim informacijama pomoću kojih bi pratili informacije i opis biljaka kao i olakšavanje brige o biljkama kao što su zadnje zalijevanje i učestalost zalijevanja biljaka. Informacije o biljkama se po potrebi mogu i ažurirati da bi korisnici što jednostavnije mogli voditi brigu o biljkama i njihovom zalijevanju. Ova web aplikacija omogućuje korisnicima da dodaju nove biljke kao i uređivanje informacija o svim biljkama koje su već pohranjene u aplikaciji. Korisniku je dostupna i statistika zalijevanja biljaka u aplikaciji kao i u grafovima: dani od zadnjeg zalijevanja, raspodjela vrsta biljaka i učestalost zalijevanja. (Kao i koliko biljaka se kasni sa zalijevanjem).

## Funkcionalnosti

- Dodavanje nove biljke  
- Uređivanje postojećih biljaka  
- Brisanje biljaka  
- Detaljan opis biljke  
- Filtriranje biljaka (vrsta, naziv, zadnje zalijevanje, interval zalijevanja...)  
- Statistika:
  - Dani od zadnjeg zalijevanja  
  - Raspodjela vrsta biljaka  
  - Učestalost zalijevanja  

<!-- Biljka (naziv biljke, vrsta biljke, datum dodavanja biljke, opis biljke, zadnje zalijevanje, učestalost zalijevanja) -->

## Tehnologije

- **Python 3.12**
- **Flask**
- **PonyORM**
- **SQLite**
- **Jinja2**
- **Chart.js**
- **Docker + Docker Compose**


## Usecase dijagram
![Use Case Diagram]([Plant care scheduler_usecase.png](https://github.com/mateoxtech/Plant-care-scheduler/blob/main/Plant%20Care%20Scheduler_usecase.png))

## Instalacija
```
cd ~Downloads
git clone https://github.com/mateoxtech
cd Plant-care-scheduler
```

## Docker
```
docker build --tag plantcare_app .
docker ps
docker run -p 8080:8080 plantcare_app
```

## Browser (za frontend)
```
docker-compose up --build
http://localhost:8080

```
