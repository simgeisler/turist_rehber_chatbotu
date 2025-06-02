# 🗺️ Turist Rehberi Chatbotu

Bu proje, turistlerin seyahat ettikleri destinasyonlarda ihtiyaç duydukları bilgileri sunmak amacıyla geliştirilmiş yapay zekâ tabanlı bir turist rehber chatbotudur. Chatbot, turistlerin seyahatleri boyunca ihtiyaç duyabilecekleri bilgileri hızlı, doğru ve kullanıcı dostu bir şekilde sunmayı amaçlamaktadır.

---

## 🎯 Hedef Kitle ve Proje Amacı

Projenin hedef kitlesi, **yabancı ve yerli turistler** olarak belirlenmiştir. Bu chatbot ile turistlerin hem **turistik ziyaretlerini planlamaları** hem de bölgeye geldikten sonra **anlık bilgi ihtiyaçlarını karşılayabilmeleri** hedeflenmiştir.

Chatbot, seyahat öncesinden başlayarak seyahat süresine kadar olan tüm süreçte kullanıcıya rehberlik eder. Özellikle ulaşım, konaklama, gezilecek yerler, etkinlikler, ve acil durum bilgileri gibi kritik konularda hızlı ve doğru bilgi sunarak, turistlerin şehir deneyimini daha konforlu ve verimli hale getirir.

Tasarım sürecinde, turistlerin ihtiyaç duyabileceği tüm veriler bir araya getirilmiş; kullanıcı dostu ve bağlam odaklı bir yapı oluşturulmuştur.

---

## 📌 Proje Akışı

Bu turist rehber chatbot projesi aşağıdaki adımlar doğrultusunda gerçekleştirilmiştir:

1. **İhtiyaç Analizi ve Intent Belirleme**  
   - Turistlerin bilgi ihtiyaçlarına yönelik 11 farklı **intent (niyet)** kategorisi belirlenmiştir.  
   - Bu kategoriler: ulaşım, konaklama, vize/ belgeler, restoran/kafe, hava durumu, etkinlikler, gezilecek yerler, acil yardım, döviz bilgisi, selamlaşma ve vedalaşma.

2. **Veri Seti Oluşturma**  
   - Yapay zeka yardımı ile Excel formatında (.xlsx) **1000 satırlık veri seti** üretilmiştir.
   - Veri seti, her intent için çeşitli senaryolar ve doğal dil çeşitliliği göz önünde bulundurularak oluşturulmuştur.

3. **Verinin Okunması** 
   - Bu aşamada, kullanıcı soru ve intent bilgilerini içeren intents.xlsx adlı Excel dosyası pandas kütüphanesi kullanılarak okunmuştur. 

     ```python
     import pandas as pd

     file_path = "intents.xlsx"  
     df = pd.read_excel(file_path)
     ```

   - Ardından her bir satırdaki veri, LangChain kütüphanesinin Document sınıfı kullanılarak belge nesnelerine dönüştürülmüştür. Her belge, kullanici_soru sütunundaki metni içerik olarak almış, intent_basligi ve satır numarası ise metadata bilgisi olarak eklenmiştir. Bu işlem sayesinde veri, doğal dil işleme uygulamalarında kullanılmak üzere yapılandırılmış hale getirilmiştir.

     ```python
     from langchain_core.documents import Document

     docs = []
     for idx, row in df.iterrows():
      content = row["kullanici_soru"]
      metadata = {"intent": row["intent_basligi"], "row_id": idx}
      doc = Document(page_content=content, metadata=metadata)
      docs.append(doc)
     ```
   
4. **Veri Setinin Eğitim ve Test Olarak Bölünmesi**  
   - Veri seti, **eğitim** ve **test** verisi olarak ikiye ayrılmıştır. Her iki projede de aynı test verisinin elde edilebilmesi için bölme işlemi sırasında sabit bir kök değer (seed) kullanılmıştır. 
   - Eğitim verisi kullanılarak modeller eğitilmiş ve test verisiyle performansları değerlendirilmiştir. 
   - Değerlendirme metrikleri:  
     - **Accuracy (Doğruluk)**  
     - **Recall (Duyarlılık)**  
     - **Precision (Hassasiyet)**  
     - **F1 Score**

5. **RAG (Retrieval-Augmented Generation) Entegrasyonu**  
   - Chatbotun daha bilgi temelli yanıtlar verebilmesi için **RAG (Retrieval-Augmented Generation)** mimarisi kullanılmıştır.
   - RAG mimarisi ile kullanıcının sorusu vektör veritabanına aktarılır, alakalı belgeler çekilir ve model bu belgeleri referans alarak yanıt üretir.  
   - Bu sayede daha güvenilir ve bağlama uygun cevaplar sağlanır.

6. **İki Ayrı LLM ile Uygulama Geliştirme**  
   Proje, iki farklı LLM (Large Language Model) altyapısı ile ayrı ayrı geliştirilmiştir:

   - 🔹 **Google tarafından geliştirilen `gemini-2.0-flash` modeli (Gemini API)**  
   - 🔹 **OpenAI tarafından geliştirilen `gpt-4o` modeli (OpenAI API)**

   Her model için proje oluşturulmuş ve aynı veri setiyle test edilmiştir.

7. **Performans Karşılaştırması**  
   - İki LLM altyapısının test verisi ile elde edilen sonuçları karşılaştırılmıştır.  
   - Metrik karşılaştırmaları doğruluk, hassasiyet, duyarlılık ve F1 skoruna göre yapılmıştır.  
   - Hangisinin bağlamı daha iyi anladığı, hız farkları ve kullanıcı deneyimi de gözlemlenmiştir.

8. **Arayüz Geliştirme (Streamlit)**  
   - Kullanıcıların chatbotu rahatça deneyimleyebilmesi için **Streamlit** kullanılarak görsel bir arayüz oluşturulmuştur. 

---

## 🧭 Chatbot

Chatbot, kullanıcıların farklı bilgi ihtiyaçlarını karşılamak üzere aşağıdaki **11 intent başlığı** ile yapılandırılmıştır:

1. **Ulaşım** – Otobüs, metro, tramvay, taksi gibi şehir içi ulaşım bilgileri  
2. **Konaklama** – Oteller, pansiyonlar ve diğer konaklama seçenekleri  
3. **Vize ve Belgeler** – Vize işlemleri, evrak gereklilikleri  
4. **Restoran ve Kafeler** – Restoran/kafe hakkında bilgiler ve önerilen mekânlar  
5. **Hava Durumu** – Anlık ve tahmini hava bilgileri  
6. **Etkinlikler** – Konserler, sergiler, festivaller gibi güncel etkinlikler  
7. **Gezilecek Yerler** – Tarihi, kültürel ve turistik noktalar  
8. **Acil Yardım** – Hastane, polis, itfaiye gibi kritik hizmetler  
9. **Döviz Bilgisi** – Güncel döviz kuru ve bozdurma noktaları  
10. **Selamlaşma** – Sohbet başlatma ve karşılama cümleleri  
11. **Vedalaşma** – Sohbeti sonlandırma ve iyi dilekler

---

## 🤖 Kullanılan Modeller

### 🔹 Neden Bu Modeller Seçildi?

- **OpenAI GPT-4o:**  
  GPT-4o, gelişmiş doğal dil işleme yetenekleri ve yüksek doğruluk seviyesi sayesinde, 1000 satırlık intent veri setinde kullanıcıların farklı ifadelerini etkili şekilde anlayıp doğru yanıtlar verebilmekte oldukça başarılıdır. Ayrıca çoklu dil desteği, hem yerli hem de yabancı turistlere hizmet sunmak için ideal olmasını sağlamaktadır. Bu nedenlerle proje kapsamında GPT-4o modeli tercih edilmiştir.

- **Google Gemini (gemini-2.0-flash):**  
  Gerçek zamanlı uygulamalar için optimize edilmiş hızlı ve düşük gecikmeli yapısıyla, projede hızlı ve güvenilir yanıt üretimi sağlamak amacıyla seçilmiştir. Google’ın güçlü bulut altyapısı da ölçeklenebilirlik ve güvenilirlik avantajı sunmaktadır.

---

### 🔹 OpenAI API Anahtarı Alımı ve Entegrasyon Bilgisi

1. [OpenAI platformuna](https://platform.openai.com/signup) gidilerek kayıt olunur ve API Keys sayfasından “Create new secret key” ile anahtar oluşturulur. 
2. Proje dizinine `.env` dosyası oluşturulur ve aşağıdaki kod eklenir:

```bash
OPENAI_API_KEY=sk-...buraya-senin-keyin...
```

3. Metinleri sayısal vektörlere dönüştürmek için OpenAI Generative AI Embeddings ile Embeddings aşağıdaki gibi oluşturulur:

```python
from langchain.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
```
4. LLM bilgileri girilerek LLM aşağıdaki gibi tetiklenir:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.3,
    max_tokens=500
)
response = llm.invoke("LangChain nedir?")
print(response)
```

---

### 🔹 Google Gemini API Anahtarı Alımı ve Entegrasyon Bilgisi

1. [Google AI Studio](https://makersuite.google.com/) adresine gidilerek hesap oluşturulur ve API Keys sayfasından “Create API key” ile anahtar oluşturulur. 
2. Proje dizinine `.env` dosyası oluşturulur ve aşağıdaki kod eklenir:

```bash
GOOGLE_API_KEY=sk-...buraya-senin-keyin...
```

3. Metinleri sayısal vektörlere dönüştürmek için Google Generative AI Embeddings ile Embeddings aşağıdaki gibi oluşturulur:

```python
from langchain_google_genai import GoogleGenerativeAIEmbeddings

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
```
4. LLM bilgileri girilerek LLM aşağıdaki gibi tetiklenir:

```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
    max_tokens=500
)
response = llm.invoke("...")
print(response)
```

---

## 📊 Performans Metrikleri

Bu projede kullanılan her iki model için performans değerlendirmesi yapılmıştır. 1000 satırlık veri seti eğitim (%80) ve test (%20) olarak ayrılmıştır. Aşağıdaki metrikler test veri seti ile her bir model için ayrı ayrı hesaplanmıştır:

- **Doğruluk (Accuracy)**  
- **Duyarlılık (Recall)**  
- **Hassasiyet (Precision)**  
- **F1-Skoru (F1 Score)**

---

### OpenAI (GPT-4o) Performans Metrikleri

Modele Ait Performans Metrikleri: 

![OpenAI Performans Metrikleri](https://github.com/user-attachments/assets/3f4f2159-79bc-463f-8da7-089b1e59682f)

Karışıklık Matrisi:

![OpenAI Karışıklık Matrisi](https://github.com/user-attachments/assets/5fedf69f-a892-4a2c-8f90-61555fe8d167)

---

### Google Gemini (gemini-2.0-flash) Performans Metrikleri

Modele Ait Performans Metrikleri:

![Gemini Performans Metrikleri](https://github.com/user-attachments/assets/5b7855b3-6c6f-45d1-b106-14bffa14e545)

Karışıklık Matrisi:

![Gemini Karışıklık Matrisi](https://github.com/user-attachments/assets/4e79c690-24bf-45c4-9432-2e658f5015da)

---

### Karşılaştırmalı Değerlendirme

İki modele ait karşılaştırm tablosu aşağıda verilmiştir.

| Model     | Precision | Recall | F1 Score | Accuracy |
|-----------|-----------|--------|----------|----------|
| **GPT-4o**    | 0.96      | 0.96   | 0.96     | 0.96     |
| **Gemini-2.0-flash** | 0.72      | 0.66   | 0.66     | 0.66     |


**🔹 Precision (Kesinlik)**  
Precision, modelin pozitif olarak tahmin ettiği örneklerin ne kadarının gerçekten doğru olduğunu ölçer.  
- **GPT-4o**, %96 precision değeri ile neredeyse tüm pozitif tahminlerinde isabetli sonuç vermektedir.  
- **Gemini-2.0-flash**, %72 precision değeri hatalı pozitif sonuçların daha fazla olduğunu göstermektedir.  
Bu metrikte GPT-4o modeli, daha doğru ve güvenilir pozitif sınıflandırmalar yapabilmektedir.

**🔹 Recall (Duyarlılık)**  
Recall, gerçekten pozitif olan örneklerin ne kadarının doğru tahmin edildiğini gösterir.  
- **GPT-4o**, %96 recall ile veri içerisindeki doğru sınıfların çoğunu kaçırmadan tespit edebilmektedir.  
- **Gemini-2.0-flash** modelinin recall değeri %66 olup, birçok doğru sınıfı atladığını göstermektedir.  
Bu metrikte de GPT-4o, daha başarılı bir yakalama yeteneğine sahiptir.

**🔹 F1 Score**  
F1 skoru, precision ve recall metriklerinin harmonik ortalamasıdır ve sınıflar arası dengesizlikte modelin genel performansını gösterir.  
- **GPT-4o**, %96 F1 skoru ile oldukça dengeli ve güçlü bir sınıflandırma başarımı sunar.  
- **Gemini-2.0-flash**, %66 F1 skoruna sahiptir, bu da hem doğru tahmin oranının hem de kaçırma oranının daha yüksek olduğunu gösterir.  
GPT-4o, bu metrikte de çok daha kararlı ve dengeli sonuçlar sunmaktadır.

**🔹 Accuracy (Doğruluk)**  
Accuracy, modelin yaptığı tüm tahminler arasında kaç tanesinin doğru olduğunu gösteren genel başarı oranıdır.  
- **GPT-4o** modeli, %96 doğruluk oranı ile oldukça yüksek başarı sergilemektedir.  
- **Gemini-2.0-flash** modeli ise %66 doğruluk oranı ile önemli ölçüde daha düşük bir genel performansa işaret etmektedir. 
Bu metrik, GPT-4o'nun genel doğruluk açısından daha üstün olduğunu açıkça ortaya koymaktadır.

**Sonuç:**
- OpenAI (GPT-4o), turist rehberi chatbotu için çok daha başarılı bir seçimdir. Özellikle çoklu sınıflarda yüksek başarı ve kararlılık göstermektedir.Google Gemini (gemini-2.0-flash), belirli basit sorular için yeterli gelmiştir ancak anlam çeşitliliği yüksek ve bağlamlı cümlelerde performansı düşük çıkmıştır. Gemini modeli daha az doğru tahminler yapmakta ve özellikle birbirine yakın sınıflarda ciddi karışıklık yaşamaktadır. Yetersiz genelleme ve yanlış sınıf tahminleri mevcuttur. 
 
- Google Gemini (gemini-2.0-flash) modelinin bu projede OpenAI (GPT-4o)’ya kıyasla daha düşük performans göstermesinin iki temel nedeni olabilir.İlk olarak, Gemini-2.0-flash modeli Google tarafından daha çok hız ve verimlilik odaklı geliştirilen hafif bir modeldir. Bu nedenle, çok sınıflı ve bağlam gerektiren detaylı sınıflandırma görevlerinde yüksek doğruluk sağlamakta zorlanabilir. İkinci olarak, veri setindeki bazı intent kategorileri arasında anlamsal yakınlıklar bulunmaktadır. Örneğin, "gezilecek_yerler" ve "etkinlikler" gibi benzer niyetler arasında net bir ayrım yapılmaması modelin sınıflar arasında karışıklık yaşamasına yol açabilir. Bu karışıklıklar, özellikle bağlamı daha yüzeysel ele alan modeller için yanıltıcı olabilir. Bu nedenle, intentlerin daha net tanımlanması ve karışıklığa yol açabilecek örneklerin yeniden gözden geçirilmesi ile model performansı doğrudan iyileştirebilir. Performans düşüklüğünün hem modelin mimari sınırlarından hem de veri setindeki intentlerin daha net ayrıştırılmamasından kaynaklanabileceği değerlendirilmektedir.
 
- **OpenAI GPT-4o**, bağlam anlama, çok dilli destek ve yüksek doğruluk açısından öne çıkmıştır. **Google Gemini Flash**, yüksek hız gerektiren gerçek zamanlı uygulamalar için uygundur ancak bağlam çözümleme ve çok dilli destek açısından sınırlı kalmaktadır. Her iki model de farklı senaryolarda fayda sağlamaktadır. Projenin gereksinimlerine göre hibrit kullanım düşünülebilir.

---

## 🖥️ Streamlit ile Chatbot Arayüzü

Projede, her iki model için de kullanıcıların soru sorabileceği ve anlık yanıt alabileceği birer **chatbot arayüzü** geliştirilmiştir. Arayüzler, Python tabanlı **Streamlit** kullanılarak oluşturulmuştur.Kullanıcı arayüzü sayesinde kullanıcılar kolayca soru sorabilir ve modelin yanıtlarını anlık olarak görebilir.

Her bir proje için ayrı bir `app.py` dosyası hazırlanmıştır. Bu dosyalar, terminal üzerinden aşağıdaki komutla çalıştırılarak arayüz başlatılabilir:

```bash
streamlit run app.py
```

Aşağıda streamlit chatbot arayüzünde kullanıcı sorusu ve chatbot cevabının yer aldığı ekran görüntüsü yer almaktadır:

![Uygulama Arayüzü Soru](https://github.com/user-attachments/assets/8b4d6a39-f993-4f88-99e1-7275b2a162a5)

![Uygulama Arayüzü Cevap](https://github.com/user-attachments/assets/3893e832-4e43-4088-ad58-443a1621c0d9)

---