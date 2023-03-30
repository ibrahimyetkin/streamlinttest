import streamlit as st
import openai
from openai.error import AuthenticationError

GPT_SYSTEM_INSTRUCTIONS = '''Sana bitkinin adını, toprağın nem oranını, ph değerini ve sıcaklık bilgilerini vericem.
sana verilen bu veriler ile  bitki sağlık durumunu değerlendirmeni isteyeceğim.  Yani durumu nasıl normal mi gibi. Ve neler yapmam gerektiğini söylemeni istiyorum.  Sadece bilgi ver başka gereksiz şeyler söyleme.'''

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
    st.title('2. Sayfa')
    st.write('Bu çok sayfalı bir Streamlit uygulamasının ikinci sayfasıdır.')

def page_three():
    st.title('2. Sayfa')
    st.write('Bu çok sayfalı bir Streamlit uygulamasının ikinci sayfasıdır.')

def call_openai(prompt):

    try:
        
        openai.api_key = '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'
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
    'Zararlılar İle Mücadele': page_three
}

st.sidebar.title('Bitki Sağlığı')
selection = st.sidebar.radio('', list(PAGES.keys()))

page = PAGES[selection]
page()