# 🚀 Q&A Bot

Welcome to the Q&A Community Bot and Mini App extravaganza! 🌐 Get ready for a rollercoaster of seamless Q&A interactions, all thanks to our dynamic duo: the Telegram bot and the Telegram Mini App. 

We're not just here to answer questions; we're here to revolutionize community engagement. Why this category, you ask? Well, it's not just us; the Telegram Mini App contest practically shouted, "Go for community management!" So here we are, giving channel owners and casual users the power to ask and answer questions while keeping their secret identities intact.

**This project is a submission for the [Telegram Mini App Contest](https://t.me/contest/327).**


<!-- ar, de, es, fr, jp, kr, ru, tr, uk, zh -->
### See this readme in other languages:
- [Deutsch](readme/README.de.md)
- [Español](readme/README.es.md)
- [Français](readme/README.fr.md)
- [Русский](readme/README.ru.md)
- [Türkçe](readme/README.tr.md)
- [Українська](readme/README.uk.md)
- [简体中文](readme/README.zh.md)
- [日本語](readme/README.jp.md)
- [العربية](readme/README.ar.md)
- [한국어](readme/README.kr.md)
- Request a language by opening an issue!

## ✨ Features Galore

- **Privacy First**: Hide and seek, anyone? Both parties can keep their identities under wraps and stay anonymous, but hey, the answering party can also play the reveal game and show their identity.
- **Inbox Magic**: Receive questions, answer them, simple as that!
- **Outbox Adventures**: Send questions, get answers, and revel in the joy of communication.
- **Profile Prowess**: Peek into other users' profiles and unleash your curiosity.
- **Manage Like a Boss**: Delete or edit questions like a pro. It's your world; we're just living in it.
- **Notification Nation**: Get pinged when questions arrive or when your genius answers are recognized.
- **Theming Elegance**: We're fashion-forward. The Mini App rocks the same theme as Telegram, making it a smooth ride.
- **Bot vs. Mini App Showdown**: Why limit yourself? Use the bot or the Mini App—it's your call.
- **Community Carnival**: Ask, answer, repeat. Engage in a Q&A dance that makes community management a breeze, especially for undercover channel admins.


## 🧩 The Grand Puzzle

This spectacle is more than just a Mini App—it's a symphony of applications! Picture this: the Telegram Mini App, a web wonder in VueJS and Nuxt, flanked by the mighty FastAPI backend in Python. And don't forget the Telegram bot, also Python-powered and chillin' in the backend. Why? Let's break it down:

- **Mini App Isolation**: We want everyone to join the party, even those less experienced in the dev world. That's why we isolated the Mini App, making it a breeze to understand and integrate into other projects.

- **Modularity Magic**: The project isn't a tangled mess—it's a carefully crafted masterpiece, thanks to modular organization and flexibility.

- **Versatility Victory Lap**: Our Telegram Mini App is the ultimate chameleon, proving it can groove with any backend. No NodeJS monopoly here; choose the backend that suits your vibe.

Ready to dive into the Q&A revolution? Buckle up; it's going to be one heck of a ride! 🎉


## Telegram Mini App

It comprises a total of 3 pages:

- `index.vue`: The entry page showing the questions asked to the user. Users can respond to these questions.
- `outbox.vue`: Displays the questions sent by the user.
- `users/[id].vue`: A page showing profile of another user. Users can also ask questions on this page.

This mini app provides an internal server with Nitro. Instead of using FastAPI, queries can be made to the database using this server, but it requires SSR. Currently, the statically built version of the Mini App is used.

### Authentication & Authorization

When users initiate the Mini App on Telegram, their user information is shared with the Mini App if they accept the terms. The data provided by Telegram is confirmed with the bot's secret key and a hash of the provided data's integrity, verifying that it is indeed provided by Telegram. Check the file [backend/api/utils/web_app_data_validator.py](backend/api/utils/web_app_data_validator.py) for more information.

From this point, a JWT is created on FastAPI. Each user and question have a "link" value, and this randomly generated data is used instead of an ID. The JWT payload includes the user's link value.

### Main Mini App Dependency
- vue-tg: An awesome and very simple wrapper library for elements used in the Mini App. [Check it out here](https://www.npmjs.com/package/vue-tg) to learn more about how to use it. I was going to write my own wrapper library, but I found this one and it was perfect for my needs and we don't need to reinvent the wheel. Instead, we can focus on a sample project that will help developers get started with the Telegram Mini App.

#### Example usage
To show a main button and a back button, let's check out the following code from [frontend/components/QAForm.vue](frontend/components/QAForm.vue). As soon as Vue renders the page, it will automatically show the buttons. The `progress` prop is used to show a loading indicator on the main button. The `disabled` prop is used to disable the main button. The `text` prop is used to set the text of the main button. The `@click` event is used to emit an event to the parent component. The `@click` event of the back button is used to call the `onCancel` method to close the form popup.

```
<MainButton 
  :progress="progressing"
  :disabled="disabled"
  :text="mainButtonText"
  @click="$emit('submitQAForm', text)" />

<BackButton @click="onCancel" />
```

#### Theme colors and viewport variables

Just like we are using components provided by Telegram, we can also use the theme colors provided by Telegram. While the theme colors are available in the initial data, it will also be available as CSS variables and you can find a list of them below:

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



You can use it in your CSS like this:

```
body {
  background-color: var(--tg-theme-bg-color);
}
```

As we are using TailwindCSS in this project, we can use the theme colors as inline styles like this:

```
<div class="bg-[var(--tg-theme-secondary-bg-color)]"></div>
```

Please note that we are not limited to inline styles. Check out the TailwindCSS documentation for more details.

# Getting started

1. Duplicate and edit the env files `.env.example` and `.db.env.example` renaming to `.env` and `.db.env` respectively.

2. Edit `nuxt.config.ts` and change `runtimeConfig.public.botUsername` to your bot's username.

To run:

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

---

## Bot (Mini App) Information
```
The Q&A Community Bot and Mini App is an innovative platform designed for seamless question-and-answer interactions within the Telegram ecosystem. Combining the capabilities of a Telegram bot and a Telegram Mini App, the project caters to both channel owners and regular users, offering a unique Telegram space for asking and answering questions while prioritizing privacy. Hence, individuals, particularly channel owners, have the option to conceal their identity while receiving questions. Additionally, they can manage and edit their questions and answers. The mini app also has other features like in-app Telegram notifications for new events (new question, answer).

https://t.me/exampleQAbot
```

### Live demo link

[https://t.me/exampleQAbot](https://t.me/exampleQAbot)

