# 🚀 Bot de Questions et Réponses

Bienvenue sur notre Bot et Mini App de la Communauté Q&A ! 🌐 Préparez-vous à plonger dans un monde d'interactions fluides de questions et réponses grâce à notre duo dynamique : le bot Telegram et la Mini App Telegram. Nous ne sommes pas là seulement pour répondre aux questions ; nous sommes là pour révolutionner l'engagement communautaire. Pourquoi cette catégorie en particulier, demanderez-vous ? Eh bien, ce n'est pas seulement nous ; le concours de Telegram Mini App criait pratiquement : "Plongez dans la gestion communautaire !" Alors nous voilà, offrant aux propriétaires de chaînes et aux utilisateurs occasionnels le pouvoir de poser et de répondre aux questions tout en préservant leur identité secrète.

## ✨ Des fonctionnalités à foison

- **La vie privée avant tout** : Jouons à cache-cache. Les deux parties peuvent cacher leur identité, mais hé, la partie qui répond peut aussi choisir de révéler son identité.
- **La magie de la boîte de réception** : Recevez des questions, répondez-y - simple comme bonjour !
- **Les aventures de la boîte d'envoi** : Envoyez des questions, obtenez des réponses et savourez la joie de la communication.
- **Les profils en vedette** : Jetez un coup d'œil aux profils des autres utilisateurs et libérez votre curiosité.
- **Gérez comme un patron** : Supprimez ou modifiez les questions que vous avez reçues - c'est votre monde ; nous vivons simplement dedans.
- **Le royaume des notifications** : Recevez une alerte lorsque vous recevez une question ou lorsque votre question est répondue.
- **L'élégance de la personnalisation** : Nous sommes à la mode. La Mini App utilise le même thème que Telegram, offrant une expérience sans couture.
- **Le duel entre le bot et la Mini App** : Pourquoi se limiter ? Utilisez le bot ou la Mini App, c'est vous qui décidez.
- **Le carnaval communautaire** : Posez des questions, répondez, répétez. Participez à une danse de questions et réponses qui facilite la gestion de la communauté, surtout pour les administrateurs de chaînes qui peuvent maintenant interagir avec leur communauté plus facilement tout en gardant leur identité cachée.

## 🧩 Le grand casse-tête

Ce spectacle n'est pas simplement une Mini App - c'est une symphonie d'applications ! Imaginez ceci : la Telegram Mini App, une merveille web en VueJS et Nuxt, alimentée par l'application FastAPI dans le backend en Python. Et n'oublions pas le bot Telegram, également écrit en Python et se détendant dans le backend. Pourquoi ? Explorons cela plus en détail :

- **L'isolement de la Mini App** : Nous voulons que tout le monde participe à la fête, même ceux moins expérimentés dans le monde du développement. C'est pourquoi nous avons isolé la Mini App, la rendant facile à comprendre et à intégrer dans d'autres projets.
  
- **La magie de la modularité** : Le projet n'est pas un enchevêtrement ; c'est un chef-d'œuvre soigneusement élaboré, grâce à l'organisation modulaire et à la flexibilité.

- **La victoire de la polyvalence de la Telegram Mini App** : L'intention était de montrer que la Telegram Mini App est adaptable et peut être utilisée avec n'importe quel backend, offrant aux développeurs la liberté de choisir le backend qui convient le mieux à leurs besoins. Elle n'est pas limitée à NodeJS et peut être utilisée avec n'importe quel backend.

Prêt à plonger dans la révolution des questions et réponses ? Attachez vos ceintures ; ça va être un voyage incroyable ! 🎉

## Mini Application Telegram

Composée au total de 3 pages :

- `index.vue` : La page d'entrée affichant les questions posées à l'utilisateur. Les utilisateurs peuvent répondre à ces questions.
- `outbox.vue` : Affiche les questions envoyées par l'utilisateur.
- `users/[id].vue` : Une page montrant le profil d'un autre utilisateur. Les utilisateurs peuvent également poser des questions sur cette page.

Cette mini-application fournit un serveur interne avec Nitro. Au lieu d'utiliser FastAPI, des requêtes peuvent être effectuées vers la base de données en utilisant ce serveur, mais cela nécessite SSR. Actuellement, la version statiquement construite de la Mini Application est utilisée.

### Authentification et Autorisation

Lorsque les utilisateurs lancent la Mini Application sur Telegram, leurs informations d'utilisateur sont partagées avec la Mini Application s'ils acceptent les conditions. Les données fournies par Telegram sont confirmées avec la clé secrète du bot et un hash de l'intégrité des données fournies, vérifiant ainsi qu'elles sont effectivement fournies par Telegram. Consultez le fichier [backend/api/utils/web_app_data_validator.py](backend/api/utils/web_app_data_validator.py) pour plus d'informations.

À partir de ce point, un JWT est créé sur FastAPI. Chaque utilisateur et chaque question ont une valeur de "lien", et ces données générées de manière aléatoire sont utilisées au lieu d'un ID. La charge utile du JWT inclut la valeur de lien de l'utilisateur.

### Dépendance Principale de la Mini Application
- vue-tg : Une bibliothèque d'enrobage impressionnante et très simple pour les éléments utilisés dans la Mini Application. [Consultez-la ici](https://www.npmjs.com/package/vue-tg) pour en savoir plus sur son utilisation. J'allais écrire ma propre bibliothèque d'enrobage, mais j'ai trouvé celle-ci et elle était parfaite pour mes besoins, et nous n'avons pas besoin de réinventer la roue. Au lieu de cela, nous pouvons nous concentrer sur un projet exemple qui aidera les développeurs à démarrer avec la Mini Application Telegram.

#### Exemple d'Utilisation
Pour afficher un bouton principal et un bouton de retour, jetons un coup d'œil au code suivant de [frontend/components/QAForm.vue](frontend/components/QAForm.vue). Dès que Vue rend la page, les boutons s'afficheront automatiquement. La propriété `progress` est utilisée pour afficher un indicateur de chargement sur le bouton principal. La propriété `disabled` est utilisée pour désactiver le bouton principal. La propriété `text` est utilisée pour définir le texte du bouton principal. L'événement `@click` est utilisé pour émettre un événement au composant parent. L'événement `@click` du bouton de retour est utilisé pour appeler la méthode `onCancel` et fermer la fenêtre contextuelle du formulaire.

```
<MainButton 
  :progress="progressing"
  :disabled="disabled"
  :text="mainButtonText"
  @click="$emit('submitQAForm', text)" />

<BackButton @click="onCancel" />
```

#### Couleurs du Thème et Variables du Viewport

Tout comme nous utilisons des composants fournis par Telegram, nous pouvons également utiliser les couleurs du thème fournies par Telegram. Bien que les couleurs du thème soient disponibles dans les données initiales, elles seront également disponibles en tant que variables CSS et vous pouvez trouver une liste ci-dessous :

```
html {
  --tg-theme-button-text-color: #ffffff;
  --tg-theme-link-color: #f83b4c;
  --tg-theme-button-color: #f83b4c;
  --tg-color-scheme: dark;
  --tg-theme-bg-color: #3e2222;
  --tg-theme-secondary-bg-color: #271616;
  --tg-theme-text-color: #ffffff;
  --tg-theme-hint-color: #b1c3d5;
  --tg-viewport-height: 100vh;
  --tg-viewport-stable-height: 100vh;
}
```


Vous pouvez l'utiliser dans votre CSS comme ceci :

```
body {
  background-color: var(--tg-theme-bg-color);
}
```

Comme nous utilisons TailwindCSS dans ce projet, nous pouvons utiliser les couleurs du thème comme styles en ligne comme ceci :

```
<div class="bg-[var(--tg-theme-secondary-bg-color)]"></div>
```

Veuillez noter que nous ne sommes pas limités aux styles en ligne. Consultez la documentation de TailwindCSS pour plus de détails.

# Démarrage

1. Dupliquez et éditez les fichiers d'environnement `.env.example` et `.db.env.example` en les renommant respectivement `.env` et `.db.env`.

2. Éditez `nuxt.config.ts` et changez `runtimeConfig.public.botUsername` par le nom d'utilisateur de votre bot.

Pour exécuter :

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```
