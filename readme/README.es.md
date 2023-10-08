# 🚀 Bot de Preguntas y Respuestas

¡Bienvenido a nuestro Bot de Comunidad de Preguntas y Respuestas y su Mini App! 🌐 Prepárate para sumergirte en un mundo sin fisuras de interacciones de preguntas y respuestas gracias a nuestra dinámica dupla: el bot de Telegram y la Mini App de Telegram. No estamos aquí solo para responder preguntas; estamos aquí para revolucionar la participación comunitaria. ¿Por qué esta categoría, preguntas? Bueno, no solo nosotros; el concurso de Telegram Mini App prácticamente gritó: "¡Vamos por el manejo comunitario!" Así que aquí estamos, dando a los propietarios de canales y a los usuarios ocasionales el poder de hacer y responder preguntas mientras mantienen sus identidades secretas.

## ✨ Características a raudales

- **Privacidad Primero**: ¿Jugamos al escondite? Ambas partes pueden mantener sus identidades en secreto, pero oye, la parte que responde también puede jugar al juego de revelar.
- **Magia del Buzón de Entrada**: Recibe preguntas, responde a ellas, ¡tan simple como eso!
- **Aventuras del Buzón de Salida**: Envía preguntas, obtén respuestas y disfruta de la alegría de la comunicación.
- **Perfiles de Proeza**: Echa un vistazo a los perfiles de otros usuarios y desata tu curiosidad.
- **Gestiona como un Jefe**: Elimina o edita preguntas como un profesional. Es tu mundo; nosotros solo vivimos en él.
- **Nación de Notificaciones**: Recibe un toque cuando lleguen preguntas o cuando respondan a tus ingeniosas respuestas.
- **Elegancia de Tematización**: Estamos a la moda. La Mini App luce el mismo tema que Telegram, haciendo que sea un paseo suave.
- **Batalla entre Bot y Mini App**: ¿Por qué limitarse? Usa el bot o la Mini App, tú decides.
- **Carnaval Comunitario**: Pregunta, responde, repite. Participa en un baile de preguntas y respuestas que facilita la gestión comunitaria, especialmente para los administradores encubiertos del canal.

## 🧩 El Gran Rompecabezas

Este espectáculo es más que una Mini App, ¡es una sinfonía de aplicaciones! Imagina esto: la Telegram Mini App, una maravilla web en VueJS y Nuxt, respaldada por el poderoso backend FastAPI en Python. Y no olvides el bot de Telegram, también impulsado por Python y relajándose en el backend. ¿Por qué? Vamos a desglosarlo:

- **Aislamiento de la Mini App**: Queremos que todos se unan a la fiesta, incluso aquellos menos experimentados en el mundo del desarrollo. Por eso aislamos la Mini App, haciéndola fácil de entender e integrar en otros proyectos.

- **Magia de la Modularidad**: El proyecto no es un enredo; es una obra maestra cuidadosamente elaborada, gracias a la organización modular y la flexibilidad.

- **Victoria de la Versatilidad**: Nuestra Telegram Mini App es el camaleón definitivo, demostrando que puede armonizar con cualquier backend. No hay monopolio de NodeJS aquí; elige el backend que mejor se adapte a tu onda.

¿Listo para sumergirte en la revolución de preguntas y respuestas? ¡Abrochaos los cinturones; va a ser un viaje espectacular! 🎉

## Mini Aplicación de Telegram

Consta de un total de 3 páginas:

- `index.vue`: La página de entrada que muestra las preguntas hechas al usuario. Los usuarios pueden responder a estas preguntas.
- `outbox.vue`: Muestra las preguntas enviadas por el usuario.
- `users/[id].vue`: Una página que muestra el perfil de otro usuario. Los usuarios también pueden hacer preguntas en esta página.

Esta mini aplicación proporciona un servidor interno con Nitro. En lugar de utilizar FastAPI, se pueden realizar consultas a la base de datos utilizando este servidor, pero requiere SSR. Actualmente, se utiliza la versión estáticamente construida de la Mini Aplicación.

### Autenticación y Autorización

Cuando los usuarios inician la Mini Aplicación en Telegram, su información de usuario se comparte con la Mini Aplicación si aceptan los términos. Los datos proporcionados por Telegram se confirman con la clave secreta del bot y un hash de la integridad de los datos proporcionados, verificando que realmente son proporcionados por Telegram. Consulta el archivo [backend/api/utils/web_app_data_validator.py](backend/api/utils/web_app_data_validator.py) para obtener más información.

A partir de este punto, se crea un JWT en FastAPI. Cada usuario y pregunta tienen un valor de "enlace", y estos datos generados aleatoriamente se utilizan en lugar de un ID. La carga útil del JWT incluye el valor de enlace del usuario.

### Dependencia Principal de la Mini Aplicación
- vue-tg: Una biblioteca envolvente impresionante y muy simple para elementos utilizados en la Mini Aplicación. [Échale un vistazo aquí](https://www.npmjs.com/package/vue-tg) para aprender más sobre cómo usarla. Iba a escribir mi propia biblioteca envolvente, pero encontré esta y era perfecta para mis necesidades, así que no necesitamos reinventar la rueda. En cambio, podemos centrarnos en un proyecto de ejemplo que ayudará a los desarrolladores a comenzar con la Mini Aplicación de Telegram.

#### Uso Ejemplar
Para mostrar un botón principal y un botón de retroceso, echemos un vistazo al siguiente código de [frontend/components/QAForm.vue](frontend/components/QAForm.vue). Tan pronto como Vue renderice la página, mostrará automáticamente los botones. La propiedad `progress` se utiliza para mostrar un indicador de carga en el botón principal. La propiedad `disabled` se utiliza para desactivar el botón principal. La propiedad `text` se utiliza para establecer el texto del botón principal. El evento `@click` se utiliza para emitir un evento al componente principal. El evento `@click` del botón de retroceso se utiliza para llamar al método `onCancel` y cerrar la ventana emergente del formulario.

```
<MainButton 
  :progress="progressing"
  :disabled="disabled"
  :text="mainButtonText"
  @click="$emit('submitQAForm', text)" />

<BackButton @click="onCancel" />
```

#### Colores del Tema y Variables del Viewport

Al igual que estamos utilizando componentes proporcionados por Telegram, también podemos utilizar los colores del tema proporcionados por Telegram. Si bien los colores del tema están disponibles en los datos iniciales, también estarán disponibles como variables CSS y puedes encontrar una lista de ellas a continuación:

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


Puedes usarlo en tu CSS de la siguiente manera:

```
body {
  background-color: var(--tg-theme-bg-color);
}
```

Como estamos utilizando TailwindCSS en este proyecto, podemos usar los colores del tema como estilos en línea de la siguiente manera:

```
<div class="bg-[var(--tg-theme-secondary-bg-color)]"></div>
```

Ten en cuenta que no estamos limitados a estilos en línea. Consulta la documentación de TailwindCSS para obtener más detalles.

# Empezando

1. Duplica y edita los archivos de entorno `.env.example` y `.db.env.example` cambiando el nombre a `.env` y `.db.env` respectivamente.

2. Edita `nuxt.config.ts` y cambia `runtimeConfig.public.botUsername` al nombre de usuario de tu bot.

Para ejecutar:

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```
