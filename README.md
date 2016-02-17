# sleepangel
Open smart clock project

# Description
Smart clock project I develop (with my spare time) a connected clock, which monitors sleep cycle (with captors), and wake up you at best moment. It can wake up you with informations like weather, news, bus schedule, etc.. Today it works only at home with WiFi but may be with mobile network in future.

**_Next description is in french_**

# Présentation

Le projet SleepAngel est un projet de réveil intelligent. L'objectif est de réaliser un réveil qui soit en mesure de surveiller votre sommeil, et de vous réveiller au meilleur moment, en fin d'un cycle. Pour vous réveiller le réveil vous donne des informations du jours qu'il récupéra sur le réseau.

# Fonctionnalités

- Open Source et Hackable
- Silencieux (pas de bruit de disque dur ou autre), ni de lumière LED pendant le sommeil
- N’émet pas de Wifi pendant le sommeil (juste au réveil pour récupérer les informations du jour, et en mode paramétrage)
- Les capteurs du sommeil ne se porte pas sur le corps (pas de bracelet) et communique avec des fils (pas rayonnement électromagnétique)
- WAF compliant ;-)

# Produits commerciaux existants

- [Withings Aura](http://www2.withings.com/us/en/products/aura)
  - - prix élève
  - - pas libre / modifiable
  - + très esthétiques
  - + capteurs sous le matelas

# Hardware

- Base:
  - Raspberry Pi
- Capteurs:
  - détecteur de mouvements “PIR”
  - détecteur de mouvements “accéléromètre”
- Son:
  - Ampli
  - Haut-Parleur
  - Relais, coupure de la ligne pour ne pas avoir de souffle
- Autres:
  - interrupteur pour action utilisateur
  - alimentation externe

# Prototype



