# Sleepangel Reborn

## Objectifs

* Nouveau capteur de mouvement de type accéléromètre
* Affichage de l’heure sur un écran
* Nouveau boîtier et design
* Autonome (utilisable sans accès réseau distant)
* Système de détection de coupure de courant
* Simple buzzer comme sonnerie
* Commande d’un relais à distance par liaison radio

## Notes de réalisation

### Accéléromètre MMA8451

Lecture des registres avec le Bus Pirate:
```
  I2C>[0x38 0x2a 0x3]       # Passage en mode Active and Fast Mode
  I2C START BIT
  WRITE: 0x38 ACK 
  WRITE: 0x2A ACK 
  WRITE: 0x03 ACK 
  I2C STOP BIT
  I2C>[0x39 rrrrrrr]        # Lecture des premiers registres de position
  I2C START BIT
  WRITE: 0x39 ACK 
  READ: 0xFF 
  READ:  ACK 0xD8 
  READ:  ACK 0x10 
  READ:  ACK 0xCF 
  READ:  ACK 0x9B 
  READ:  ACK 0xD8 
  READ:  ACK 0x0F 
  NACK
  I2C STOP BIT
  I2C>[0x39 rrrrrrr]
  I2C START BIT
  WRITE: 0x39 ACK 
  READ: 0xFF 
  READ:  ACK 0xF5 
  READ:  ACK 0x1B 
  READ:  ACK 0xC7 
  READ:  ACK 0xBB 
  READ:  ACK 0xF5 
  READ:  ACK 0x1B 
  NACK
  I2C STOP BIT
```
