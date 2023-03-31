import streamlit as st
import openai
from openai.error import AuthenticationError
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

GPT_SYSTEM_INSTRUCTIONS = '''Sana bitkinin adını, toprağın nem oranını, ph değerini ve sıcaklık bilgilerini vericem.
sana verilen bu veriler ile  bitki sağlık durumunu değerlendirmeni isteyeceğim.  Yani durumu nasıl normal mi gibi. Olması gereken değerler aralıklarını belirt. Ve neler yapmam gerektiğini söyle. Herşeyi maddeler olarak yaz. Sadece bilgi ver başka gereksiz şeyler söyleme.'''

def home_page():
    st.subheader('''Modern Eğitim Koleji''')
    st.title('''Bitki Sağlığı Programı'na Hoş Geldiniz!''')
    
    st.write('''

Bu program, bitki yetiştiriciliği ve bahçecilik uygulamalarında kullanıcıların bitki sağlığı ile ilgili bilgileri takip etmelerine, hastalıkları ve zararlıları kontrol etmelerine ve bitki yetiştiriciliği ile ilgili en son bilgileri takip etmelerine yardımcı olmak için tasarlanmıştır.

Ana sayfamız, kullanıcı dostu bir arayüz ve kullanışlı özellikler içerir. Burada, bitkilerinizin büyüme durumunu, su ve gübre ihtiyaçlarını, toprağın pH değerini ve nem içeriğini kolayca takip edebilirsiniz.

Ayrıca, programda bir bitki hastalıkları ve zararlıları kılavuzu da yer almaktadır. Bu kılavuz, bitki hastalıklarının belirtilerini, zararlıların görüntülerini ve nasıl kontrol edileceği konusunda tavsiyeleri içerir.

Programımızda ayrıca bitki yetiştiriciliği ile ilgili haberleri veya en son eğilimleri içeren bir bölüm de bulunmaktadır. Bu bölüm, bitki yetiştiricilerinin ve bahçıvanların sektördeki gelişmeleri takip etmelerine yardımcı olacaktır.

Programımızın amacı, bitki sağlığı ile ilgili bilgileri izlemeyi kolaylaştırmak ve bitki yetiştiriciliği ve bahçecilik uygulamalarını daha verimli hale getirmek için kullanıcı dostu bir platform sağlamaktır.

Bu nedenle, siz de Bitki Sağlığı Programı'na hoş geldiniz ve burada sağlıklı bitki büyümesi için gerekli bilgileri kolayca takip edebileceksiniz.''')

def page_one():
    bitki = st.text_input("BİTKİ ADI")
    ph = st.number_input("PH DEĞERİ", step=0.1, format="%.1f")
    sicaklik = st.number_input("SICAKLIK (°C)", step=0.1, format="%.1f")
    nem = st.number_input("Nem Oranı (%)", step=1)
    if st.button('Analiz Et'):
        if bitki and ph and sicaklik and nem:
            call_openai("Bitki adi: " + bitki + " ph degeri: " + str(ph) + " sicaklik: " + str(sicaklik) + " nem orani: " + str(nem))
        else:
            st.warning("Lütfen tüm değerleri giriniz.")

    
    
    

def page_two():

    # Web page scraping
    url = "https://www.agriculture.com/news/technology"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Set up translation
    translator = Translator(service_urls=["translate.google.com"])
    target_language = "tr"

    # Title and description
    st.title("Tarım Alanındaki Son Teknolojiler ve Gelişmeler")
    st.write("Bu uygulama, tarım alanındaki en son teknolojileri ve gelişmeleri göstermektedir.")

    # Display the latest developments
    st.header("Son Gelişmeler")
    news_items = soup.find_all("div", class_="recent-content-title-teaser")

    for item in news_items:
        title = item.find("span", class_="field-content").text.strip()
        description = item.find("div", class_="field-body").text.strip()

        # Translate the title and description
        translated_title = translator.translate(title, dest=target_language).text
        translated_description = translator.translate(description, dest=target_language).text

        st.subheader(translated_title)
        st.write("Açıklama:", translated_description)


def page_three():
    st.title('Akıllı Sulama')
    st.write('Ürünlere ne zaman ve ne kadar su uygulanacağını tahmin etmek için hava durumu verilerini kullanarak sulama sistemlerini optimize etmek için kullanılabilir.')

def page_four():
    st.title('Otomasyon')
    st.write('Ekim, hasat ve ekin büyümesini izleme gibi manuel görevleri otomatikleştirmek için kullanılabilir. Bu, çiftçilerin zamandan ve işçilik maliyetlerinden tasarruf etmesine ve insan hatası riskini azaltmasına yardımcı olabilir.')
def page_five():    
    st.title('Tahmine dayalı analitik planlama')
    st.write('Mahsul ve hayvancılık yönetimi kararlarını bilgilendirmek için çeşitli kaynaklardan büyük miktarda veriyi analiz edecek şekilde eğitilebilir. Bu, çiftçilerin operasyonlarını optimize etmelerine, verimleri artırmalarına ve maliyetleri düşürmelerine yardımcı olabilir.')

     


def call_openai(prompt):

    try:
        
        openai.api_key =  st.secrets["OPEN_API_KEY"] 
        response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": GPT_SYSTEM_INSTRUCTIONS},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1200
        )
    except Exception as e:
        st.error(repr(e))
        st.stop()

    code_response = response.choices[0].message.content

    st.write(code_response)



PAGES = {
    'Ana Sayfa': home_page,
    'Ölçme': page_one,
    'Haberler': page_two,
    'Akıllı Sulama': page_three,
    'Otomasyon': page_four,
    'Planlama': page_five,
}

st.sidebar.title('Bitki Sağlığı')
selection = st.sidebar.radio('', list(PAGES.keys()))

page = PAGES[selection]
page()