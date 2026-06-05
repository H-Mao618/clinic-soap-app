import streamlit as st



# 設定網頁標題

st.set_page_config(page_title="門診病歷快速生成器", layout="wide")

st.title("🩺 門診病歷快速生成器 (SOAP)")

st.caption("本機端單機運行，100% 確保病患隱私安全")



# 使用 Streamlit 的左右分欄功能

col1, col2 = st.columns([1, 1])



with col1:
   
    st.header("📋 症狀與檢查點選")

 
   
    # 1. 基本資訊
    
    st.subheader("基本資訊")
    
    age = st.number_input("年齡", min_value=0, max_value=120, value=40)
    
    gender = st.selectbox("性別", ["Male", "Female"])
 
    vital_sign =  st.text_input("生命徵象", value="130/80, 70")
  
    

    # 2. Subjective (主訴與症狀)
    
    st.subheader("Subjective (S)")
    
    cc_cough = st.checkbox("Cough (咳嗽)")
    
    cc_fever = st.checkbox("Fever (發燒)")
    
    cc_dyspnea = st.checkbox("Dyspnea (呼吸困難)")
    

    cc_abd_pain = st.checkbox("Abdominal pain (腹痛)")
 

    # 條件式連動：如果勾選腹痛，才顯示疼痛部位輸入框
    
    abd_location = []
    
    if cc_abd_pain:
        
        abd_location = st.multiselect(
            
            "請選擇腹痛具體位置(可多選)", 

            ["epigastric pain", "RUQ pain", "LUQ pain", "RLQ pain", "lower abd pain", "LLQ pain", "diffuse abd pain"]

        )

    # 條件式連動：如果勾選發燒，才顯示體溫輸入框
    
    bt = 36.5
    
    if cc_fever:
        
        bt = st.number_input("Body Temperature (°C)", min_value=35.0, max_value=42.0, value=38.2, step=0.1)
        
    
    
    # 3. Objective (理學檢查)
    
    st.subheader("Objective (O)")
    
    pe_throat = st.checkbox("Throat: Infected/Injected (喉嚨紅腫)")
    
    pe_breathing = st.selectbox("Breathing Sound (呼吸音)", ["Clear", "Wheezing (喘鳴音)", "Rales (濕囉音)"])

   

    # 這裡順便幫您加一個腹部理學檢查的連動，如果點腹痛，就預設跳出壓痛選項
    
    pe_tenderness = "no tenderness"
    
    if cc_abd_pain:
        
        pe_tenderness = st.selectbox("Abdomen PE (觸診)", ["no tenderness", "tenderness (+)", "rebounding tenderness (+)"])
    pe_bowel_sound = st.selectbox("Bowel sound (腸音)", ["normo-active BS", "hyper-active BS", "hypo-active BS"])  

    # 4. Sonography exam
    st.divider()
    st.subheader("📸 超音波檢查結果 (Sono)")
    do_sono = st.checkbox("執行超音波檢查(Performed Sonography)")

    sono_type = "Abdominal Sonography"
    sono_findings = []
    if do_sono:
        sono_type = st.selectbox("超音波項目", ["Abdominal Sono", "Thyroid Sono", "Breast Sono"])

        # 根據不同的超音波項目，給予對應的常用 findings 勾選
        if sono_type == "Abdominal Sono":
            if st.checkbox("Fatty liver (脂肪肝)"): sono_findings.append("Mild fatty liver noted.")
            if st.checkbox("Gallstone (膽結石)"): sono_findings.append("A gallbladder stone about 1.2cm with acoustic shadow.")
            if st.checkbox("GB wall thickening (膽囊壁變厚)"): sono_findings.append("Gallbladder wall thickening noted, acute cholecystitis cannot be ruled out.")
            if st.checkbox("Renal stone (腎結石)"): sono_findings.append("Right renal stone noted.")




# 在右側即時組合並顯示病歷

with col2:
    
    st.header("📝 產出報告區")

    # 🌟 建立兩個分頁：一個放 SOAP，一個放 Sono 報告
    tab_soap, tab_sono = st.tabs(["📄 門診病歷 (SOAP)", "📊 超音波報告 (Sono Report)"])
   
    # --- Tab 1: SOAP 病歷組合邏輯 ---
    with tab_soap:
        st.write("您可以直接複製下方文字貼回 HIS 的 SOAP 欄位：")
        soap_text = ""

    # S 區塊
    
        soap_text += f"[Subjective]\n"
    
        soap_text += f"This {age}-year-old {gender} presented with "
    
        symptoms = []
    
        if cc_cough: symptoms.append("cough")
    
        if cc_fever: symptoms.append(f"fever (BT: {bt}°C)")
    
        if cc_dyspnea: symptoms.append("dyspnea")
    
    

    # 處理腹痛的文字邏輯：如果有選位置，就直接用位置的字串
    
        if cc_abd_pain and abd_location:
        
            symptoms.extend(abd_location)
    
    
        elif cc_abd_pain and not abd_location:
            symptoms.append("abdominal pain")
        if symptoms:
        
            soap_text += ", ".join(symptoms) + ".\n"
    
        else:
        
            soap_text += "no special discomfort today.\n"
        
        soap_text += "\n"

    # O 區塊
    
        soap_text += f"[Objective]\n"
    
        if vital_sign:
        
            soap_text += f"- Vital signs: {vital_sign}\n"

        if pe_throat:
        
            soap_text += "- Throat: Throat injection (+)\n"
    
        else:
        
            soap_text += "- Throat: Not injected\n"
    
        soap_text += f"- Chest: Breathing sound: {pe_breathing}\n"
    
    
    # 如果有腹痛，在 Objective 也自動補上腹部觸診結果
    
        if cc_abd_pain:
        
            soap_text += f"- Abdomen: Soft, {pe_tenderness}, {pe_bowel_sound}\n"
      
        soap_text += "\n"
    
    # --- Tab 2: 超音波報告組合邏輯 ---
    with tab_sono:
        st.write("您可以直接複製下方文字貼回 HIS 的 Echo 報告欄位：")
        
        if do_sono:
            sono_text = f"=== {sono_type} Report ===\n"
            sono_text += "[Findings]\n"
            
            if sono_findings:
                for finding in sono_findings:
                    sono_text += f"- {finding}\n"
            else:
                sono_text += "- No remarkable abnormality noted.\n"
        else:
            sono_text = "（左側未勾選「執行超音波檢查」，故不生成報告）"
            
        st.text_area("Sono Report Output", value=sono_text, height=450, key="sono_area")
    

    # 在網頁上呈現一個方便複製的文字框
    
    st.text_area("SOAP Output (可直接複製)", value=soap_text, height=400)
