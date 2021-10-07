# MSEFCPython

Syslog 

Codes de catégorie :

| Code  |   Mot-clé    |              Description               |
|:-----:|:------------:|:--------------------------------------:|
|   0   | kern         | messages du noyau                      |
|   1   | user         | messages de l'espace utilisateur       |
|   2   | mail         | messages du système de messagerie      |
|   3   | daemon       | messages des processus d'arrière plan  |
|   4   | auth         | messages d'authentification            |
|   5   | syslog       | messages générés par syslogd lui-même  |
|   6   | lpr          | messages d'impressions                 |
|   7   | news         | messages d'actualités                  |
|   8   | uucp         | messages UUCP                          |
|   9   | cron         | Taches planifiées (at/cron)            |
|  10   | authpriv     | sécurité / élévation de privilèges     |
|  11   | ftp          | logiciel FTP                           |
|  12   | ntp          | Synchronisation du temps NTP           |
|  13   | security     | log audit                              |
|  14   | console      | log alert                              |
|  15   | solaris-cron | Taches planifiées (at/cron)            |
|  16   | local0       | Utilisation locale libre 0 (local0)    |
|  17   | local1       | Utilisation locale libre 1  (local1)   |
|  18   | local2       | Utilisation locale libre 2  (local2)   |
|  19   | local3       | Utilisation locale libre 3  (local3)   |
|  20   | local4       | Utilisation locale libre 4  (local4)   |
|  21   | local5       | Utilisation locale libre 5  (local5)   |
|  22   | local6       | Utilisation locale libre 6  (local6)   |
|  23   | local7       | Utilisation locale libre 7  (local7)   |

Niveau de gravité : 

| Code  |    Gravité     |     Mot-clé     |                                Description                                |
|:-----:|:--------------:|:---------------:|:-------------------------------------------------------------------------:|
|   0   | Emergency      | emerg (panic)   | Système inutilisable.                                                     |
|   1   | Alert          | alert           | Une intervention immédiate est nécessaire.                                |
|   2   | Critical       | crit            | Erreur critique pour le système.                                          |
|   3   | Error          | err (error)     | Erreur de fonctionnement.                                                 |
|   4   | Warning        | warn (warning)  | Avertissement (une erreur peut intervenir si aucune action n'est prise).  |
|   5   | Notice         | notice          | Événement normal méritant d'être signalé.                                 |
|   6   | Informational  | info            | Pour information.                                                         |
|   7   | Debugging      | debug           | Message de mise au point.                                                 |
