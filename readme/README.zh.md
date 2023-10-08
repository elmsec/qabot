# 🚀 问答机器人

欢迎来到我们的问答社区机器人和迷你应用！ 🌐 在我们的 Telegram 机器人和 Telegram 迷你应用的动态组合的帮助下，准备好进入无缝问答互动的世界。我们不仅仅是为了回答问题，更是为了在社区互动方面进行创新。为什么选择这个类别呢？嗯，不仅仅是因为我们，Telegram 迷你应用大赛也差不多喊着：“投入到社区管理中去！” 所以，我们在这里，为频道所有者和普通用户提供一个在保护隐私的同时接收和提出问题的机会。

## ✨ 无限功能

- **隐私优先**：双方都可以隐藏他们的身份，而回答方也可以选择是否公开他们的身份。
- **收件箱的魔法**：用户可以接收来自其他用户的问题并回答它们。
- **发件箱的冒险**：用户可以向其他用户发送问题并查看答案。
- **个人资料**：用户可以查看其他用户的个人资料。
- **问题管理**：用户可以删除他们收到的问题或编辑他们对这些问题的回答。
- **通知**：用户可以在收到问题或问题被回答时收到通知。
- **集成主题支持**：迷你应用使用与 Telegram 应用相同的主题，提供无缝体验。
- **机器人 UI 和迷你应用 UI**：用户可以使用机器人或迷你应用与平台互动。所以他们不局限于一个选择。
- **社区参与**：用户可以向其他用户提问，其他用户也可以回答其他用户的问题。这使得对于频道管理员来说尤其是与社区更轻松互动，同时保持他们的身份不可见。

它由多个应用程序组成。例如，Telegram 迷你应用本质上是前端文件夹中的 Web 应用程序。迷你应用使用 VueJS 和 Nuxt 编写。它由后端文件夹中的 Python 编写的 FastAPI 应用程序提供支持。此外，还有一个独立于迷你应用的 Python 编写的 Telegram 机器人。这些决策是基于以下目标制定的：

- 为了隔离迷你应用以提高可访问性：目标是尽可能地将**迷你应用**分开，使其即使对于经验较少的开发人员也易于理解和使用。这样一来，它可以无缝集成到其他项目中。

- 为了增强项目的模块性：将项目分解为更易管理的模块可以更好地组织和灵活性。

- 为了展示 Telegram 迷你应用的多样性：展示 Telegram 迷你应用是适应性强大的，并可以与任何后端一起使用，为开发人员提供选择后端的自由。它不仅仅局限于 NodeJS，可以与任何后端一起使用。

## 电报迷你应用

总共包含3个页面：

- `index.vue`：显示用户提出的问题的入口页面。用户可以回答这些问题。
- `outbox.vue`：显示用户发送的问题。
- `users/[id].vue`：显示另一用户的个人资料的页面。用户也可以在此页面提问。

这个迷你应用使用 Nitro 提供了一个内部服务器。与使用 FastAPI 不同，可以使用此服务器向数据库进行查询，但这需要 SSR。目前，使用 Mini App 的静态构建版本。

### 身份验证和授权

当用户在电报上启动 Mini App 时，如果他们接受条款，他们的用户信息将与 Mini App 分享。电报提供的数据通过机器人的秘密密钥和提供的数据完整性的哈希进行确认，以验证它确实是由电报提供的。有关更多信息，请查看文件 [backend/api/utils/web_app_data_validator.py](backend/api/utils/web_app_data_validator.py)。

从这一点开始，在 FastAPI 上创建了一个 JWT。每个用户和问题都有一个“链接”值，而这个随机生成的数据被用来代替 ID。JWT 负载包括用户的链接值。

### 主要 Mini App 依赖
- vue-tg：用于 Mini App 中使用的元素的出色且非常简单的包装库。[点击这里](https://www.npmjs.com/package/vue-tg)了解更多如何使用它的信息。我本来打算写自己的包装库，但我找到了这个，它完全符合我的需求，我们无需重新发明轮子。相反，我们可以专注于一个示例项目，帮助开发人员开始使用电报 Mini App。

#### 示例用法
为了显示主按钮和返回按钮，让我们查看 [frontend/components/QAForm.vue](frontend/components/QAForm.vue) 中的以下代码。一旦 Vue 渲染页面，它将自动显示按钮。`progress` 属性用于在主按钮上显示加载指示器。`disabled` 属性用于禁用主按钮。`text` 属性用于设置主按钮的文本。`@click` 事件用于向父组件发射事件。返回按钮的 `@click` 事件用于调用 `onCancel` 方法关闭表单弹出窗口。

```
<MainButton 
  :progress="progressing"
  :disabled="disabled"
  :text="mainButtonText"
  @click="$emit('submitQAForm', text)" />

<BackButton @click="onCancel" />
```

#### 主题颜色和视口变量

就像我们使用电报提供的组件一样，我们还可以使用电报提供的主题颜色。虽然主题颜色在初始数据中可用，但它也将作为 CSS 变量可用，您可以在下面找到它们的列表：

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


您可以在您的 CSS 中像这样使用它：

```
body {
  background-color: var(--tg-theme-bg-color);
}
```

由于在这个项目中我们使用 TailwindCSS，我们可以像这样将主题颜色用作内联样式：

```
<div class="bg-[var(--tg-theme-secondary-bg-color)]"></div>
```

请注意，我们不仅限于内联样式。查看 TailwindCSS 文档以获取更多详细信息。

# 入门指南

1. 复制并编辑环境文件 `.env.example` 和 `.db.env.example`，将它们重命名为 `.env` 和 `.db.env`。

2. 编辑 `nuxt.config.ts` 并将 `runtimeConfig.public.botUsername` 更改为您的机器人的用户名。

要运行：

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```
