# 🚀 Frage- und Antwort-Bot

Willkommen auf unserer Plattform für die Q&A-Community! 🌐 Bereiten Sie sich darauf vor, in eine Welt reibungsloser Interaktionen von Fragen und Antworten einzutauchen, dank unseres dynamischen Duos: dem Telegram-Bot und der Telegram Mini-App. Wir sind nicht nur hier, um Fragen zu beantworten; wir sind hier, um das community-Engagement zu revolutionieren. Warum gerade diese Kategorie, werden Sie fragen? Nun, das sind nicht nur wir; der Telegram Mini-App-Wettbewerb hat praktisch geschrien: "Taucht ein in das Community-Management!" Also, hier sind wir, und bieten sowohl den Kanalbesitzern als auch den Gelegenheitsnutzern die Möglichkeit, Fragen zu stellen und zu beantworten, während ihre Identität geheim bleibt.

## ✨ Funktionen im Überfluss

- **Privatsphäre zuerst** : Spielen wir Verstecken. Beide Parteien können ihre Identität verbergen, aber hey, die antwortende Partei kann sich auch dazu entscheiden, ihre Identität preiszugeben.
- **Die Magie des Posteingangs** : Erhalten Sie Fragen, antworten Sie darauf - einfach wie Hallo!
- **Die Abenteuer des Postausgangs** : Senden Sie Fragen, erhalten Sie Antworten und genießen Sie die Freude der Kommunikation.
- **Profile im Rampenlicht** : Werfen Sie einen Blick auf die Profile anderer Benutzer und lassen Sie Ihrer Neugier freien Lauf.
- **Managen wie ein Boss** : Löschen oder bearbeiten Sie die erhaltenen Fragen - das ist Ihre Welt; wir leben nur darin.
- **Das Königreich der Benachrichtigungen** : Erhalten Sie eine Benachrichtigung, wenn Sie eine Frage erhalten oder wenn Ihre Frage beantwortet wird.
- **Die Eleganz der Anpassung** : Wir sind im Trend. Die Mini-App verwendet dasselbe Thema wie Telegram und bietet ein nahtloses Erlebnis.
- **Das Duell zwischen dem Bot und der Mini-App** : Warum sich einschränken? Verwenden Sie den Bot oder die Mini-App - Sie entscheiden.
- **Der Community-Carnival** : Stellen Sie Fragen, antworten Sie, wiederholen Sie. Nehmen Sie an einem Tanz von Fragen und Antworten teil, der die Community-Verwaltung erleichtert, insbesondere für Kanaladministratoren, die nun leichter mit ihrer Community interagieren können, während ihre Identität verborgen bleibt.

## 🧩 Das große Puzzle

Diese Show ist nicht nur eine Mini-App - es ist eine Symphonie von Anwendungen! Stellen Sie sich vor: Die Telegram Mini-App, ein Webwunder in VueJS und Nuxt, unterstützt von der leistungsstarken FastAPI-Anwendung im Backend in Python. Und vergessen Sie nicht den Telegram-Bot, ebenfalls in Python geschrieben und im Hintergrund entspannend. Warum? Lassen Sie uns das genauer betrachten:

- **Die Isolation der Mini-App** : Wir möchten, dass alle an der Party teilnehmen, auch diejenigen, die weniger Erfahrung in der Entwicklerwelt haben. Deshalb haben wir die Mini-App isoliert, um sie verständlich und leicht in andere Projekte integrierbar zu machen.

- **Die Magie der Modularität** : Das Projekt ist kein Wirrwarr; es ist ein sorgfältig ausgearbeitetes Meisterwerk dank modularer Organisation und Flexibilität.

- **Der Sieg der Vielseitigkeit der Telegram Mini-App** : Die Absicht war zu zeigen, dass die Telegram Mini-App anpassungsfähig ist und mit jedem Backend verwendet werden kann, wodurch Entwicklern die Freiheit gegeben wird, das Backend auszuwählen, das am besten zu ihren Bedürfnissen passt. Es ist nicht auf NodeJS beschränkt und kann mit jedem Backend verwendet werden.

Bereit, in die Revolution der Fragen und Antworten einzutauchen? Schnallen Sie sich an; das wird eine unglaubliche Reise! 🎉


## Telegram Mini App

Bestehend aus insgesamt 3 Seiten:

- `index.vue`: Die Einstiegsseite zeigt die dem Benutzer gestellten Fragen an. Benutzer können auf diese Fragen antworten.
- `outbox.vue`: Zeigt die vom Benutzer gesendeten Fragen an.
- `users/[id].vue`: Eine Seite, die das Profil eines anderen Benutzers zeigt. Benutzer können auch auf dieser Seite Fragen stellen.

Diese Mini-App bietet einen internen Server mit Nitro. Anstelle von FastAPI können Abfragen an die Datenbank über diesen Server gestellt werden, er erfordert jedoch SSR. Derzeit wird die statisch erstellte Version der Mini-App verwendet.

### Authentifizierung & Autorisierung

Wenn Benutzer die Mini-App auf Telegram starten, werden ihre Benutzerinformationen mit der Mini-App geteilt, wenn sie den Bedingungen zustimmen. Die von Telegram bereitgestellten Daten werden mit dem geheimen Schlüssel des Bots und einem Hash der Integrität der bereitgestellten Daten bestätigt, um zu überprüfen, dass sie tatsächlich von Telegram stammen. Überprüfen Sie die Datei [backend/api/utils/web_app_data_validator.py](backend/api/utils/web_app_data_validator.py) für weitere Informationen.

Ab diesem Punkt wird auf FastAPI ein JWT erstellt. Jeder Benutzer und jede Frage haben einen "Link"-Wert, und diese zufällig generierten Daten werden anstelle einer ID verwendet. Die JWT-Payload enthält den Link-Wert des Benutzers.

### Hauptabhängigkeit der Mini-App
- vue-tg: Eine großartige und sehr einfache Wrapper-Bibliothek für Elemente, die in der Mini-App verwendet werden. [Schau es dir hier an](https://www.npmjs.com/package/vue-tg), um mehr darüber zu erfahren, wie es verwendet wird. Ich wollte meine eigene Wrapper-Bibliothek schreiben, habe aber diese gefunden und sie war perfekt für meine Bedürfnisse, und wir müssen das Rad nicht neu erfinden. Stattdessen können wir uns auf ein Beispielprojekt konzentrieren, das Entwicklern den Einstieg in die Telegram Mini-App erleichtert.

#### Beispielverwendung
Um einen Haupt- und einen Zurück-Button anzuzeigen, werfen wir einen Blick auf den folgenden Code aus [frontend/components/QAForm.vue](frontend/components/QAForm.vue). Sobald Vue die Seite rendert, werden die Buttons automatisch angezeigt. Die `progress`-Eigenschaft wird verwendet, um einen Ladeindikator auf dem Hauptbutton anzuzeigen. Die `disabled`-Eigenschaft wird verwendet, um den Hauptbutton zu deaktivieren. Die `text`-Eigenschaft wird verwendet, um den Text des Hauptbuttons festzulegen. Das `@click`-Event wird verwendet, um ein Event an das übergeordnete Komponente zu senden. Das `@click`-Event des Zurück-Buttons wird verwendet, um die Methode `onCancel` aufzurufen und das Formular-Popup zu schließen.

```
<MainButton 
  :progress="progressing"
  :disabled="disabled"
  :text="mainButtonText"
  @click="$emit('submitQAForm', text)" />

<BackButton @click="onCancel" />
```

#### Theme-Farben und Viewport-Variablen

Wie wir Komponenten von Telegram verwenden, können wir auch die von Telegram bereitgestellten Theme-Farben verwenden. Während die Theme-Farben in den Initialdaten verfügbar sind, stehen sie auch als CSS-Variablen zur Verfügung. Hier finden Sie eine Liste davon:

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


Sie können es in Ihrem CSS so verwenden:

```
body {
  Hintergrundfarbe: var(--tg-theme-bg-color);
}
```

Da wir in diesem Projekt TailwindCSS verwenden, können wir die Theme-Farben als Inline-Styles wie folgt verwenden:

```
<div class="bg-[var(--tg-theme-secondary-bg-color)]"></div>
```

Beachten Sie bitte, dass wir nicht auf Inline-Styles beschränkt sind. Schauen Sie sich die TailwindCSS-Dokumentation für weitere Details an.

# Erste Schritte

1. Duplizieren und bearbeiten Sie die Umgebungsdateien `.env.example` und `.db.env.example`, benennen Sie sie in `.env` und `.db.env` um.

2. Bearbeiten Sie `nuxt.config.ts` und ändern Sie `runtimeConfig.public.botUsername` auf den Benutzernamen Ihres Bots.

Zum Ausführen:

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```
