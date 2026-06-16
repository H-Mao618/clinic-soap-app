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
    
    # 2. Subjective (主訴與症狀)
    st.subheader("Subjective (S)")
    cc_cough = st.checkbox("Cough (咳嗽)")
    cc_fever = st.checkbox("Fever (發燒)")
    cc_dyspnea = st.checkbox("Dyspnea (呼吸困難)")
    
    # 新增的 Abdominal pain 勾選框
    cc_abd_pain = st.checkbox("Abdominal pain (腹痛)")
    
    # 條件式連動：如果勾選「腹痛」，才顯示位置選擇
    abd_location = []
    if cc_abd_pain:
        abd_location = st.multiselect(
            "請選擇腹痛具體位置", 
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
    
    # 4. Assessment & Plan (診斷與計畫)
    st.subheader("Assessment & Plan (A/P)")
    # 根據勾選自動切換建議 Dx，如果是腹痛就換成 Abdominal pain
    default_dx = "Acute Gastroenteritis" if cc_abd_pain else "Acute Upper Respiratory Infection"
    diagnosis = st.text_input("初步診斷 (Dx)", value=default_dx)
    plan_med = st.checkbox("開立處方藥物 (Medication)")
    plan_education = st.checkbox("衛教 (Rest, hydration)")

    # 5. Sonography (超音波檢查)
    st.subheader("Sonography")
    do_sono = st.checkbox("Perform sonography")
    sono_date = st.date_input("檢查日期")
    sono_date_str = sono_date.strftime('%Y-%m-%d')

    sono_type = []
    sono_findings = []
    if do_sono:
        sono_type = st.selectbox("Select Sono type", ["Abdominal sono", "Thyroid sono", "Breast sono"])
        if sono_type == "Abdominal sono":
            findings_abd = st.multiselect("請勾選腹部超音波異常發現", ["Fatty liver change", "Liver mass", "GB stone", "GB wall thickening", "Kidney stone"])
            
            if "Fatty liver change" in findings_abd:
                fatty_liver_grade = st.selectbox("Select grade", ["Mild", "Moderate", "Severe"])
                if fatty_liver_grade == "Mild": 
                    sono_findings.append("Mild fatty liver change.")
                elif fatty_liver_grade == "Moderate": 
                    sono_findings.append("Moderate fatty liver change.")
                elif fatty_liver_grade == "Severe": 
                    sono_findings.append("Severe fatty liver change.")
            else:  
                sono_findings.append("No fatty liver change.")
# --- 2. Liver mass 邏輯 (選擇 Segment 與輸入大小) ---
            if "Liver mass" in findings_abd:
                st.caption("↳ Liver mass 詳細設定：")
                # 建立 Segment 的下拉選單
                mass_seg = st.selectbox(
                    "Select Segment", 
                    ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "indeterminate region"]
                )
                # 建立大小輸入框（預設 1.0 cm，每次加減 0.1）
                mass_size = st.number_input("Mass size (cm)", min_value=0.1, max_value=20.0, value=1.0, step=0.1, key="mass_size")
                
                # 自動組合成正式醫學英文病歷
                sono_findings.append(f"A liver mass measuring about {mass_size} cm at {mass_seg}.")

            # --- 3. GB stone 邏輯 (輸入大小) ---
            if "GB stone" in findings_abd:
                st.caption("↳ Gallbladder stone 詳細設定：")
                gb_stone_size = st.number_input("Stone size (cm)", min_value=0.1, max_value=10.0, value=1.0, step=0.1, key="gb_stone")
                
                sono_findings.append(f"A GB stone about {gb_stone_size} cm.")

            # --- 4. GB wall thickening 邏輯 (輸入厚度) ---
            if "GB wall thickening" in findings_abd:
                st.caption("↳ GB wall thickening 詳細設定：")
                # 膽囊壁通常用 mm 計算比較精準
                gb_wall_thickness = st.number_input("Wall thickness (mm)", min_value=1.0, max_value=20.0, value=4.0, step=0.5, key="gb_wall")
                
                sono_findings.append(f"GB wall thickening ({gb_wall_thickness} mm).")

            # --- 5. Kidney stone 邏輯 (選擇左右側與輸入大小) ---
            if "Kidney stone" in findings_abd:
                st.caption("↳ Kidney stone 詳細設定：")
                # 選擇左側、右側或雙側
                ks_side = st.selectbox("Select Side", ["Right", "Left", "Bilateral"])
                ks_size = st.number_input("Stone size (cm)", min_value=0.1, max_value=5.0, value=0.5, step=0.1, key="ks_size")
                
                # 根據單複數自動微調文法 (如果選 Bilateral 用 stones，其餘用 stone)
                if ks_side == "Bilateral":
                    sono_findings.append(f"Bilateral renal stones, largest {ks_size} cm.")
                else:
                    sono_findings.append(f"{ks_side} renal stone {ks_size} cm.")

    
    # 6. Assessment & Plan (診斷與計畫)
    st.subheader("Assessment & Plan (A/P)")


# 在右側即時組合並顯示病歷
with col2:
    st.header("📝 產出報告區")

    # 🌟 建立兩個分頁：一個放 SOAP，一個放 Sono 報告
    tab_soap, tab_sono = st.tabs(["📄 門診病歷 (SOAP)", "📊 超音波報告 (Sono Report)"])
    
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
            symptoms.extend(abd_location)  # .extend 會把複選的多個部位拆開，漂亮地排在籃子裡
        elif cc_abd_pain and not abd_location:
            symptoms.append("abdominal pain")
    
        if symptoms:
            soap_text += ", ".join(symptoms) + ".\n"
        else:
            soap_text += "no special discomfort today.\n"
        
        soap_text += "\n"
    
        # O 區塊
        soap_text += f"[Objective]\n"
        if pe_throat:
            soap_text += "- Throat: Throat injection (+)\n"
        else:
            soap_text += "- Throat: Not injected\n"
        soap_text += f"- Chest: Breathing sound: {pe_breathing}\n"
    
        # 如果有腹痛，在 Objective 也自動補上腹部觸診結果
        if cc_abd_pain:
            soap_text += f"- Abdomen: Soft, {pe_tenderness}\n"
    
        soap_text += "\n"
    
        # A 區塊
        soap_text += f"[Assessment]\n"
        soap_text += f"- {diagnosis}\n\n"
    
        # P 區塊
        soap_text += f"[Plan]\n"
        plans = []
        if plan_med: plans.append("Medication prescribed.")
        if plan_education: plans.append("Patient was educated about lifestyle modifications, adequate hydration, and rest.")
        if plans:
            soap_text += "\n".join([f"- {p}" for p in plans]) + "\n"
        else:
            soap_text += "- Routine follow up.\n"

        # 在網頁上呈現一個方便複製的文字框
        st.text_area("SOAP Output (可直接複製)", value=soap_text, height=400)

    with tab_sono:
        st.write("您可以直接複製下方文字貼回 HIS 的 SONO 欄位：")
        sono_text = ""
        sono_text += f"{sono_date_str}, {sono_type}.\n"
        
        if sono_findings:
            for finding in sono_findings:
                sono_text += f"- {finding}\n"
        else:
            sono_text += "- No remarkable abnormality noted.\n"
        
        # 在網頁上呈現一個方便複製的文字框
        st.text_area("SONO Output (可直接複製)", value=sono_text, height=400)
