<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/Logo-diginamic-color-blk.png">
    <img src="assets/Logo-diginamic-color.svg" alt="Diginamic Formation" width="358">
  </picture>
</p>

# Les fondamentaux de la cybersécurité et de la sécurité informatique

Une journée pour acquérir les bases de la sécurité des systèmes d'information,
vues depuis le poste de celles et ceux qui manipulent des données et
construisent des modèles d'IA. Le cours se suit **en autonomie** : chaque
chapitre alterne une partie de théorie courte et une mise en pratique
(exercice, TP en Python ou étude de cas), dont la correction est repliée sous
l'énoncé.

## 🎯 Objectifs pédagogiques

À la fin de cette journée, vous saurez :

1. Expliquer les notions de base de la sécurité - actif, menace, vulnérabilité,
   risque - et les critères **DICP** (disponibilité, intégrité, confidentialité,
   preuve).
2. Mener une **analyse de risques** simple et modéliser les menaces d'un
   pipeline de données avec la méthode **STRIDE**.
3. Choisir le bon outil cryptographique - **hachage, chiffrement symétrique et
   asymétrique, signature** - et le mettre en œuvre en Python.
4. Sécuriser l'**authentification** et le **contrôle d'accès**, et gérer
   correctement des secrets.
5. Reconnaître et corriger les vulnérabilités applicatives les plus courantes
   (**OWASP Top 10**), dont celles propres à l'écosystème data (`pickle`).
6. Protéger des données personnelles : **pseudonymisation**,
   **anonymisation**, obligations du **RGPD**.
7. Identifier les menaces spécifiques aux **systèmes d'IA** - empoisonnement,
   évasion, injection de prompt - et les parades associées.
8. Exploiter des **journaux** pour détecter une attaque, et connaître les
   étapes d'une **réponse à incident**.

## ❔ Pourquoi ce cours en EISI Data-IA ?

Les données sont la cible de la plupart des attaques : on vole des bases
clients, on chiffre des entrepôts pour obtenir une rançon, on revend des jeux
d'entraînement. Un·e data engineer ou un·e data scientist manipule chaque jour
les actifs les plus convoités de l'entreprise, avec des outils - notebooks,
fichiers `pickle`, clés d'API, modèles téléchargés - qui ouvrent autant de
portes. Et les systèmes d'IA ajoutent leurs propres failles, que les attaquants
exploitent déjà.

La sécurité n'est donc pas l'affaire d'une équipe à part : elle se joue dans
chaque requête SQL, chaque jeu de données partagé, chaque modèle mis en
production. Ce cours en pose les fondations.

## Prérequis

- Python : lire et écrire un script, utiliser `pandas`.
- SQL : écrire une requête `SELECT` avec une clause `WHERE`.
- Ligne de commande et Docker : lancer un conteneur, ouvrir un terminal.
- Notions de réseau : adresse IP, port, HTTP.

## Comment suivre ce cours

1. Suivez les chapitres **dans l'ordre** : chacun s'appuie sur le précédent.
2. Dans chaque chapitre, lisez la théorie, puis faites l'exercice **avant**
   d'ouvrir la correction.
3. Les fichiers des TP sont dans le dossier `tp/` du dépôt. Le
   [chapitre 00](00-Preparer-son-environnement.md) explique comment les
   lancer.
4. Terminez par le [quiz final](09-Quiz-final.md) : visez au moins 15 bonnes
   réponses sur 20.

> ⚖️ **Cadre légal.** Toutes les attaques de ce cours se pratiquent sur
> **vos propres conteneurs**, avec des données fictives. Accéder ou se
> maintenir sans droit dans un système d'autrui est un délit (articles 323-1
> et suivants du Code pénal), même "pour tester".

## Le parcours

| # | Étape | Durée | Ce qu'on y fait |
|---|---|---|---|
| [00](00-Preparer-son-environnement.md) | Préparer son environnement | 10 min | installer le laboratoire Docker, vérifier qu'il fonctionne |
| [01](01-Panorama-et-notions-cles.md) | Panorama et notions clés | 25 min | les menaces actuelles, les attaquants, DICP, actif / menace / vulnérabilité / risque - *exercice : classer des incidents réels* |
| [02](02-Analyse-de-risques-et-modelisation-des-menaces.md) | Analyse de risques et modélisation des menaces | 25 min | matrice de risques, EBIOS RM, STRIDE - *exercice : STRIDE sur un pipeline ML* |
| [03](03-Cryptographie-appliquee.md) | Cryptographie appliquée | 45 min | hachage, sel, chiffrement symétrique et asymétrique, signature, TLS - *TP : casser une fuite de mots de passe, stocker correctement, chiffrer ; signer en option* |
| [04](04-Authentification-et-controle-d-acces.md) | Authentification et contrôle d'accès | 30 min | facteurs, MFA, mots de passe, JWT, moindre privilège, secrets - *TP : forcer un JWT mal signé, débusquer des secrets* |
| [05](05-Securite-des-applications.md) | Sécurité des applications | 45 min | OWASP Top 10, injection SQL, contrôle d'accès défaillant, désérialisation - *TP : attaquer puis corriger une API de données ; modèle `pickle` piégé en option* |
| [06](06-Protection-des-donnees-et-RGPD.md) | Protection des données et RGPD | 30 min | classification, pseudonymisation, anonymisation, k-anonymat, RGPD - *TP : pseudonymiser et ré-identifier un jeu de données* |
| [07](07-Securite-de-l-IA.md) | Sécurité des systèmes d'IA | 45 min | empoisonnement, évasion, inférence, injection de prompt, OWASP LLM, AI Act - *TP : empoisonner un modèle (porte dérobée en option), détourner un assistant* |
| [08](08-Detection-et-reponse-aux-incidents.md) | Détection et réponse aux incidents | 30 min | défense en profondeur, journalisation, SIEM, réponse à incident, sauvegardes - *TP : enquêter dans des journaux web* |
| [09](09-Quiz-final.md) | Quiz final | 15 min | 20 questions pour valider la journée |
| [A](A-Glossaire-et-ressources.md) | Glossaire et ressources | - | le vocabulaire du cours, les références pour aller plus loin |

Durée totale : **5 heures de travail**, réparties sur la journée avec des
pauses. Les étapes marquées *facultatives* et les *bonus* ne sont pas comptés :
gardez-les pour la fin, ou pour plus tard.

### Planning type

| Horaire | Activité |
|---|---|
| 9 h 00 - 9 h 35 | 00 - Environnement, 01 - Panorama |
| 9 h 35 - 10 h 00 | 02 - Analyse de risques |
| 10 h 00 - 10 h 15 | ☕ Pause |
| 10 h 15 - 11 h 00 | 03 - Cryptographie |
| 11 h 00 - 11 h 10 | ☕ Pause |
| 11 h 10 - 11 h 40 | 04 - Authentification |
| 11 h 40 - 12 h 00 | Marge : finir les TP du matin |
| 12 h 00 - 13 h 30 | 🍽️ Déjeuner |
| 13 h 30 - 14 h 15 | 05 - Sécurité des applications |
| 14 h 15 - 14 h 45 | 06 - Données et RGPD |
| 14 h 45 - 15 h 00 | ☕ Pause |
| 15 h 00 - 15 h 45 | 07 - Sécurité de l'IA |
| 15 h 45 - 15 h 55 | ☕ Pause |
| 15 h 55 - 16 h 25 | 08 - Détection et réponse |
| 16 h 25 - 16 h 40 | 09 - Quiz final |
| 16 h 40 - 17 h 00 | Marge : bonus, relecture des points faibles du quiz |
