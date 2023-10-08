# 🚀 Soru ve Cevap Botu

Hoş geldiniz Q&A Topluluk Botu ve Mini Uygulamamıza! 🌐 Telegram botu ve Telegram Mini Uygulama ile soru-cevap etkileşimini sorunsuz bir şekilde yaşamanız için buradayız. Sadece soruları cevaplamak için değil, topluluk etkileşimini devrimleştirmek için buradayız. Neden bu kategori derseniz? Hani biz değil, Telegram Mini Uygulama yarışması adeta bağırdı: "Topluluk yönetimine yönelin!" İşte buradayız, kanal sahiplerine ve sıradan kullanıcılara soru sorma ve cevap verme gücünü verirken gizli kimliklerini korumalarını sağlıyoruz.

## ✨ Özelliklerle Dolu

- **Gizlilik Önce**: Saklambaç oynamaya var mısınız? Her iki taraf da kimliklerini gizleyebilir, ama eyvah, cevap veren taraf da kimliğini açığa çıkarabilir.
- **Gelen Kutu Büyüsü**: Sorular alın, cevap verin - basitçe!
- **Giden Kutu Maceraları**: Sorular gönderin, cevaplar alın ve iletişim keyfini çıkarın.
- **Profil Yeteneği**: Diğer kullanıcıların profillerine göz atın ve merakınızı serbest bırakın.
- **Patron Gibi Yönetme**: Soruları silin veya cevapları düzenleyin - Bu sizin dünyanız; biz sadece burada yaşıyoruz.
- **Bildirim Krallığı**: Sorular geldiğinde veya sorularınız cevaplandığında bildirim alın.
- **Temaya Entegrasyon**: Moda ileri. Mini Uygulama, Telegram ile aynı temayı kullanarak sorunsuz bir deneyim sunar.
- **Bot vs. Mini Uygulama Gösterisi**: Neden kendinizi sınırlayasınız? Botu veya Mini Uygulamayı kullanın - sizin kararınız.
- **Topluluk Karnavalı**: Soru sor, cevapla, tekrarla. Topluluk yönetimini kolaylaştıran bir soru-cevap dansına katılın, özellikle gizli kanal yöneticileri için.

## 🧩 Büyük Bulmaca

Bu gösteri sadece bir Mini Uygulama değil - bir dizi uygulamanın simfonisi! Düşünün: Telegram Mini Uygulama, VueJS ve Nuxt'ta bir web harikası, Python'da yazılmış güçlü FastAPI backend tarafından destekleniyor. Ve Telegram botunu unutma, o da Python güçlendiriliyor ve arka planda rahatlıyor. Neden? Hadi bunu ayrıntılı bir şekilde inceleyelim:

- **Mini Uygulama İzolasyonu**: Herkesin partiye katılmasını istiyoruz, hatta geliştirme dünyasında daha az deneyime sahip olanlar. Bu yüzden Mini Uygulamayı izole ettik, anlaşılması ve diğer projelere entegre edilmesi kolay olsun diye.

- **Modüler Büyü**: Proje bir yığın olmadan dikkatlice hazırlanmış bir başyapıya dönüştü, modüler organizasyon ve esneklik sayesinde.

- **Telegram Mini Uygulama'nın Çeşitlilik Zaferi**: Telegram Mini Uygulama'nın uyumlu ve herhangi bir backend ile kullanılabileceğini sergilemek istedik, geliştiricilere ihtiyaçlarına en uygun backend'i seçme özgürlüğü tanıdık. NodeJS ile sınırlı değil, herhangi bir backend ile kullanılabilir.

Soru ve cevap devrimine dalışa hazır mısınız? Kemerlerinizi bağlayın; harika bir yolculuk olacak! 🎉

## Telegram Mini Uygulama

Toplamda 3 sayfadan oluşuyor:

- `index.vue`: Kullanıcıya sorulan soruları gösteren giriş sayfası. Kullanıcılar bu sorulara cevap verebilir.
- `outbox.vue`: Kullanıcı tarafından gönderilen soruları görüntüler.
- `users/[id].vue`: Başka bir kullanıcının profilini gösteren sayfa. Kullanıcılar bu sayfada aynı zamanda soru sorabilirler.

Bu mini uygulama Nitro ile dahili bir sunucu sağlıyor. FastAPI yerine, bu sunucu üzerinden veritabanına sorgular yapılabilir, ancak SSR gerektirir. Şu anda, Mini Uygulamanın statik olarak oluşturulmuş sürümü kullanılıyor.

### Kimlik Doğrulama ve Yetkilendirme

Kullanıcılar Telegram'da Mini Uygulamayı başlattığında, kullanıcı bilgileri şartları kabul ederlerse Mini Uygulama ile paylaşılır. Telegram tarafından sağlanan veriler, botun gizli anahtarı ve sağlanan verilerin bütünlüğünün bir hash'i ile onaylanır, böylece gerçekten Telegram tarafından sağlandığı doğrulanır. Daha fazla bilgi için [backend/api/utils/web_app_data_validator.py](backend/api/utils/web_app_data_validator.py) dosyasına bakabilirsiniz.

Bu noktadan itibaren FastAPI'de bir JWT oluşturulur. Her kullanıcının ve sorunun bir "bağlantı" değeri vardır ve bu rastgele oluşturulan veri, bir Kimlik yerine kullanılır. JWT yükü, kullanıcının bağlantı değerini içerir.

### Ana Mini Uygulama Bağımlılığı
- vue-tg: Mini Uygulamada kullanılan elementler için harika ve çok basit bir sarmalayıcı kütüphane. [Buradan inceleyin](https://www.npmjs.com/package/vue-tg) ve nasıl kullanılacağını daha fazla öğrenin. Kendi sarmalayıcı kütüphanemi yazacaktım, ama bunu buldum ve ihtiyaçlarıma tam uyduğu için tekerleği yeniden icat etmeye gerek yoktu. Bunun yerine, Telegram Mini Uygulaması ile geliştiricilere başlamalarına yardımcı olacak bir örnek proje üzerine odaklanabiliriz.

#### Örnek Kullanım
Ana düğmeyi ve geri düğmesini göstermek için [frontend/components/QAForm.vue](frontend/components/QAForm.vue) dosyasındaki aşağıdaki kodları inceleyelim. Vue sayfayı renderladığında, düğmeler otomatik olarak gösterilecektir. `progress` özelliği, ana düğmede bir yükleme göstergesi göstermek için kullanılır. `disabled` özelliği, ana düğmeyi devre dışı bırakmak için kullanılır. `text` özelliği, ana düğmenin metnini ayarlamak için kullanılır. `@click` etkinliği, üst bileşene bir etkinlik yayınlamak için kullanılır. Geri düğmesinin `@click` etkinliği, form penceresini kapatmak için `onCancel` yöntemini çağırmak için kullanılır.

```
<MainButton 
  :progress="progressing"
  :disabled="disabled"
  :text="mainButtonText"
  @click="$emit('submitQAForm', text)" />

<BackButton @click="onCancel" />
```

#### Tema Renkleri ve Görünüm Değişkenleri

Telegram tarafından sağlanan bileşenleri kullanmak gibi, Telegram tarafından sağlanan tema renklerini de kullanabiliriz. Tema renkleri başlangıç verilerinde mevcut olsa da, CSS değişkenleri olarak da kullanılabilir ve bunların bir listesini aşağıda bulabilirsiniz:

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


Bunu CSS'de şu şekilde kullanabilirsiniz:

```
body {
  background-color: var(--tg-theme-bg-color);
}
```

Bu projede TailwindCSS kullanıyoruz, bu nedenle temaları iç içe stiller olarak şu şekilde kullanabiliriz:

```
<div class="bg-[var(--tg-theme-secondary-bg-color)]"></div>
```

Lütfen, iç içe stillerle sınırlı olmadığımızı unutmayın. Daha fazla bilgi için TailwindCSS belgelerine göz atın.

# Başlangıç

1. `.env.example` ve `.db.env.example` dosyalarını kopyalayın ve düzenleyerek sırasıyla `.env` ve `.db.env` olarak yeniden adlandırın.

2. `nuxt.config.ts` dosyasını düzenleyin ve `runtimeConfig.public.botUsername`'yi botunuzun kullanıcı adına değiştirin.

Çalıştırmak için:

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```
