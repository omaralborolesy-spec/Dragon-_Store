import streamlit as st
import json
import os
import base64
import urllib.parse

st.set_page_config(
    page_title="Dragon Store - متجر الأناقة الأسطورية",
    page_icon="🐉",
    layout="wide"
)

def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

lamp_base64 = get_image_base64("lamp_isolated.png")
robot_base64 = get_image_base64("robot.png")
logo_base64 = get_image_base64("logo.png")

if "login_state" not in st.session_state:
    st.session_state.login_state = "normal"

animation_class = "robot-footer"
if st.session_state.login_state == "success":
    animation_class = "robot-footer robot-happy"
elif st.session_state.login_state == "error":
    animation_class = "robot-footer robot-shake"

st.markdown(
    f"""
    <style>
    /* خلفية داكنة فخمة */
    .stApp {{
        background: linear-gradient(135deg, #0b0f0e 0%, #131c18 50%, #1a2923 100%);
        color: #ffffff;
        font-family: 'Cairo', sans-serif;
    }}
    
    /* رأس الصفحة والشعار والمصباح في اليسار */
    .top-left-container {{
        position: fixed;
        top: 20px;
        left: 30px;
        z-index: 999;
        display: flex;
        align-items: center;
        gap: 15px;
    }}

    .store-logo img {{
        width: 65px;
        height: 65px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #00ff88;
        box-shadow: 0 0 15px rgba(0, 255, 128, 0.6);
        animation: fadeInLogo 1s ease-out forwards;
    }}

    @keyframes fadeInLogo {{
        0% {{ opacity: 0; transform: scale(0.5); }}
        100% {{ opacity: 1; transform: scale(1); }}
    }}

    .top-left-lamp {{
        animation: lampEntranceShake 1.2s ease-out forwards, lampGlowEffect 2.5s ease-in-out 1.2s infinite alternate;
    }}
    .top-left-lamp img {{
        width: 100px;
        height: auto;
        background: transparent !important;
        filter: drop-shadow(0 0 20px rgba(0, 255, 128, 0.7));
    }}

    @keyframes lampEntranceShake {{
        0% {{ opacity: 0; transform: translateY(-30px) scale(0.8); filter: drop-shadow(0 0 0px #00ff88); }}
        30% {{ opacity: 1; transform: translateY(5px) rotate(-8deg) scale(1.1); filter: drop-shadow(0 0 40px #00ff88); }}
        50% {{ transform: translateY(-5px) rotate(6deg) scale(0.95); filter: drop-shadow(0 0 10px #00ff88); }}
        70% {{ transform: translateY(3px) rotate(-4deg) scale(1.05); filter: drop-shadow(0 0 35px #00ff88); }}
        100% {{ opacity: 1; transform: translateY(0) rotate(0deg) scale(1); filter: drop-shadow(0 0 25px rgba(0, 255, 128, 0.8)); }}
    }}

    @keyframes lampGlowEffect {{
        0% {{ filter: drop-shadow(0 0 15px rgba(0, 255, 128, 0.5)); transform: scale(1); }}
        100% {{ filter: drop-shadow(0 0 35px rgba(0, 255, 128, 0.95)); transform: scale(1.02); }}
    }}

    /* حاوية تسجيل الدخول في الجانب اليمين */
    .login-right-container {{
        display: flex;
        justify-content: flex-end;
        align-items: center;
        min-height: 80vh;
        padding-right: 50px;
    }}

    .login-box {{
        background: rgba(14, 22, 19, 0.95);
        border: 1px solid rgba(0, 255, 128, 0.4);
        border-radius: 20px;
        padding: 30px 40px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.9), 0 0 25px rgba(0, 255, 128, 0.15);
        width: 420px;
        text-align: right;
        backdrop-filter: blur(10px);
        animation: fadeInBox 1.2s ease-in-out 0.8s forwards;
        opacity: 0;
    }}

    @keyframes fadeInBox {{
        0% {{ opacity: 0; transform: translateY(20px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}

    /* الروبوت في أسفل الصفحة بعيون وحركة متفاعلة */
    .robot-footer {{
        position: fixed;
        bottom: 15px;
        left: 50%;
        transform: translateX(-50%);
        text-align: center;
        z-index: 999;
        animation: showRobotFooter 1s ease-out 1s forwards;
        opacity: 0;
    }}

    .robot-footer img {{
        width: 85px;
        height: auto;
        background: transparent !important;
        animation: robotEyeAndHeadMove 3s infinite ease-in-out;
        filter: drop-shadow(0 0 15px rgba(0, 255, 128, 0.7));
    }}

    @keyframes showRobotFooter {{
        0% {{ opacity: 0; transform: translateX(-50%) translateY(20px); }}
        100% {{ opacity: 1; transform: translateX(-50%) translateY(0); }}
    }}

    @keyframes robotEyeAndHeadMove {{
        0%, 100% {{ transform: translateY(0) rotate(0deg) scale(1); }}
        25% {{ transform: translateY(-5px) rotate(-2deg) scale(1.02); filter: drop-shadow(0 0 20px #00ff88); }}
        50% {{ transform: translateY(0) rotate(0deg) scale(1); }}
        75% {{ transform: translateY(-5px) rotate(2deg) scale(1.02); filter: drop-shadow(0 0 20px #00ff88); }}
    }}

    .robot-happy img {{
        animation: robotJump 0.5s ease-in-out 3 !important;
        filter: drop-shadow(0 0 25px #00ff66) !important;
    }}

    .robot-shake img {{
        animation: shakeError 0.3s ease-in-out 3 !important;
        filter: drop-shadow(0 0 25px #ff0033) !important;
    }}

    @keyframes robotJump {{
        0%, 100% {{ transform: translateY(0) scale(1); }}
        50% {{ transform: translateY(-15px) scale(1.08); }}
    }}

    @keyframes shakeError {{
        0%, 100% {{ transform: translateX(0); }}
        25% {{ transform: translateX(-10px); }}
        75% {{ transform: translateX(10px); }}
    }}

    .stButton button {{
        background: linear-gradient(90deg, #00b074, #00ff88);
        color: #0b0f0e;
        border: none;
        border-radius: 10px;
        font-weight: bold;
        font-size: 16px;
        width: 100%;
        padding: 12px;
        box-shadow: 0 4px 20px rgba(0, 255, 136, 0.4);
        transition: all 0.3s ease;
    }}
    
    .stButton button:hover {{
        background: linear-gradient(90deg, #00ff88, #00b074);
        box-shadow: 0 0 25px rgba(0, 255, 136, 0.8);
        transform: translateY(-2px);
    }}

    .sidebar-robot img {{
        width: 45px;
        height: auto;
        border-radius: 50%;
        background: transparent !important;
        box-shadow: 0 0 10px rgba(0, 255, 128, 0.5);
        vertical-align: middle;
        margin-left: 8px;
    }}

    .sidebar-logo img {{
        width: 50px;
        height: 50px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #00ff88;
        vertical-align: middle;
        margin-left: 10px;
    }}

    .product-card {{
        background: rgba(19, 28, 24, 0.85);
        border: 1px solid rgba(0, 255, 128, 0.3);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.4s ease-in-out;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }}

    .product-card:hover {{
        transform: translateY(-8px);
        border-color: #00ff88;
        box-shadow: 0 0 25px rgba(0, 255, 128, 0.6);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "cart" not in st.session_state:
    st.session_state.cart = []

ORDERS_FILE = "orders_db.json"
PRODUCTS_FILE = "products_db.json"

def load_json(file_path, default_val):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return default_val
    return default_val

def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

orders_db = load_json(ORDERS_FILE, {})
products_db = load_json(PRODUCTS_FILE, {})

if not st.session_state.logged_in:
    # عرض الشعار والمصباح معاً في الزاوية اليسرى العليا
    top_left_html = '<div class="top-left-container">'
    if logo_base64:
        top_left_html += f'<div class="store-logo"><img src="data:image/png;base64,{logo_base64}" alt="Logo"></div>'
    if lamp_base64:
        top_left_html += f'<div class="top-left-lamp"><img src="data:image/png;base64,{lamp_base64}" alt="Lamp"></div>'
    top_left_html += '</div>'
    
    st.markdown(top_left_html, unsafe_allow_html=True)
    
    # الروبوت في أسفل الصفحة
    if robot_base64:
        st.markdown(
            f"""
            <div class="{animation_class}">
                <img src="data:image/png;base64,{robot_base64}" alt="Robot">
            </div>
            """,
            unsafe_allow_html=True
        )

    # نموذج تسجيل الدخول في الجانب اليمين
    st.markdown('<div class="login-right-container"><div class="login-box">', unsafe_allow_html=True)
    
    st.markdown("<h2 style='color: #ffffff; margin-bottom: 2px; text-align: right;'>Welcome Back.</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00ff88; font-size: 13px; margin-bottom: 20px; text-align: right;'>Illuminate your path with Dragon Store</p>", unsafe_allow_html=True)
    
    with st.form("video_login_form"):
        user_input = st.text_input("اسم المستخدم", placeholder="Username")
        pass_input = st.text_input("كلمة المرور", type="password", placeholder="Password (12345)")
        
        submit_btn = st.form_submit_button("SIGN IN ➔")
        
        if submit_btn:
            if user_input.strip() == "":
                st.session_state.login_state = "error"
                st.warning("الرجاء إدخال اسم المستخدم.")
                st.rerun()
            elif pass_input == "12345":
                st.session_state.login_state = "success"
                st.session_state.logged_in = True
                st.session_state.username = user_input
                st.session_state.is_admin = (user_input.lower() == "admin")
                st.success("تم تسجيل الدخول بنجاح! 🚀")
                st.rerun()
            else:
                st.session_state.login_state = "error"
                st.error("كلمة المرور غير صحيحة! (12345)")
                st.rerun()
                
    st.markdown('</div></div>', unsafe_allow_html=True)

else:
    # عرض الشعار في القائمة الجانبية بعد تسجيل الدخول
    if logo_base64:
        st.sidebar.markdown(
            f"""
            <div style="display: flex; align-items: center; margin-bottom: 20px; border-bottom: 1px solid rgba(0,255,128,0.2); padding-bottom: 15px;">
                <div class="sidebar-logo"><img src="data:image/png;base64,{logo_base64}" alt="Logo"></div>
                <div>
                    <h3 style="color: #00ff88; margin: 0; font-size: 18px;">Dragon Store</h3>
                    <p style="color: #bbb; margin: 0; font-size: 12px;">أهلاً، {st.session_state.username}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.sidebar.title(f"👤 أهلاً بك، {st.session_state.username}")
    
    if st.sidebar.button("تسجيل الخروج 🚪"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.is_admin = False
        st.session_state.cart = []
        st.session_state.login_state = "normal"
        st.rerun()
        
    menu_options = ["الرئيسية والمتجر 🛒", "سلة الشراء والفاتورة 🛍️", "تتبع الطلب 📦"]
    if st.session_state.is_admin:
        menu_options.append("لوحة الأدمن 🛠️")
        
    page = st.sidebar.radio("الانتقال إلى:", menu_options)

    if page == "الرئيسية والمتجر 🛒":
        st.title("🐉 متجر الأناقة الأسطورية - Dragon Store")
        st.write(f"مرحباً بك يا **{st.session_state.username}**! تصفح المنتجات وأضفها لسلة الشراء:")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if not products_db:
            st.info("📦 الكتالوج فارغ حالياً. يمكن للأدمن إضافة منتجات من لوحة التحكم.")
        else:
            cols = st.columns(2)
            for i, (p_id, p_info) in enumerate(products_db.items()):
                with cols[i % 2]:
                    st.markdown(
                        f"""
                        <div class="product-card">
                            <h3 style="color: #00ff88; margin-top: 0;">{p_info.get('name')}</h3>
                            <p><b>السعر:</b> {p_info.get('price')} ج.م</p>
                            <p><b>القسم:</b> {p_info.get('category')}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    if st.button(f"إضافة للسلة 🛒", key=f"add_{p_id}"):
                        st.session_state.cart.append(p_info)
                        st.success(f"تم إضافة {p_info.get('name')} للسلة!")

    elif page == "سلة الشراء والفاتورة 🛍️":
        st.title("🧾 الفاتورة والدفع")
        
        if not st.session_state.cart:
            st.warning("سلة الشراء فارغة حالياً! تصفح المتجر وأضف منتجات.")
        else:
            st.subheader("🛒 المنتجات المختارة:")
            total_price = 0
            items_summary = ""
            
            for idx, item in enumerate(st.session_state.cart):
                st.write(f"{idx+1}. **{item['name']}** - {item['price']} ج.م")
                total_price += item['price']
                items_summary += f"- {item['name']} ({item['price']} ج.م)\n"
                
            st.markdown("---")
            st.markdown(f"### 💰 الإجمالي: **{total_price} ج.م**")
            
            st.subheader("📝 بيانات الدفع والتوصيل:")
            cust_name = st.text_input("اسم العميل بالكامل", value=st.session_state.username)
            cust_phone = st.text_input("رقم الهاتف للتواصل")
            cust_address = st.text_area("عنوان التوصيل بالتفصيل")
            
            if st.button("إتمام الطلب وإرسال الفاتورة عبر الواتساب 📲"):
                if not cust_phone or not cust_address:
                    st.error("الرجاء إدخال رقم الهاتف والعنوان لتأكيد الطلب.")
                else:
                    order_id = f"ORD-{len(orders_db) + 1001}"
                    
                    orders_db[order_id] = {
                        "name": cust_name,
                        "phone": cust_phone,
                        "address": cust_address,
                        "total": total_price,
                        "items": items_summary,
                        "status": "قيد المعالجة ⏳"
                    }
                    save_json(ORDERS_FILE, orders_db)
                    
                    invoice_text = (
                        f"🐉 *فاتورة طلب جديدة - Dragon Store*\n\n"
                        f"📌 *رقم الطلب:* {order_id}\n"
                        f"👤 *اسم العميل:* {cust_name}\n"
                        f"📞 *رقم العميل:* {cust_phone}\n"
                        f"📍 *العنوان:* {cust_address}\n\n"
                        f"🛍️ *المنتجات:*\n{items_summary}\n"
                        f"💰 *الإجمالي النهائي:* {total_price} ج.م\n\n"
                        f"شكرًا لتسوقك من متجر الأناقة الأسطورية! 👑"
                    )
                    
                    target_whatsapp = "201558478544"
                    encoded_msg = urllib.parse.quote(invoice_text)
                    whatsapp_url = f"https://wa.me/{target_whatsapp}?text={encoded_msg}"
                    
                    st.success(f"✅ تم تسجيل طلبك بنجاح! رقم الطلب: {order_id}")
                    st.markdown(f"[👉 اضغط هنا لإرسال الفاتورة عبر الواتساب لتأكيد الدفع 📲]({whatsapp_url})")
                    
                    st.session_state.cart = []

    elif page == "تتبع الطلب 📦":
        st.markdown("## 📦 تتبع حالة طلبك (Order Tracking)")
        st.write("أدخل رقم الطلب أو رقم الهاتف المسجل لمتابعة شحنتك لحظة بلحظة:")
        
        search_query = st.text_input("🔍 أدخل رقم الطلب أو الهاتف:", placeholder="مثال: ORD-1001 أو 01558478544")
        
        if st.button("بحث عن الطلب 🚀"):
            if search_query.strip():
                found = False
                for order_id, details in orders_db.items():
                    if search_query.strip() == order_id or search_query.strip() == details.get("phone"):
                        found = True
                        st.success(f"📌 **رقم الطلب:** {order_id}")
                        status = details.get("status", "قيد المعالجة ⏳")
                        
                        if "قيد المعالجة" in status:
                            st.warning(f"**حالة الشحن:** {status}")
                        elif "جاري الشحن" in status:
                            st.info(f"**حالة الشحن:** {status}")
                        else:
                            st.success(f"**حالة الشحن:** {status}")
                            
                        st.write(f"👤 **العميل:** {details.get('name')}")
                        st.write(f"📍 **العنوان:** {details.get('address')}")
                        st.write(f"💰 **الإجمالي:** {details.get('total')} ج.م")
                        st.markdown("---")
                if not found:
                    st.error("❌ لم يتم العثور على أي طلب بهذه البيانات.")
            else:
                st.warning("الرجاء كتابة رقم الطلب أو الهاتف أولاً.")

    elif page == "لوحة الأدمن 🛠️" and st.session_state.is_admin:
        st.title("🛠️ لوحة تحكم الأدمن (Admin Dashboard)")
        st.success("أهلاً بك يا بطل في لوحة القيادة الإدارية 👑")
        
        tab1, tab2 = st.tabs(["إدارة المنتجات 👕", "إدارة الطلبات والشحن 📦"])
        
        with tab1:
            st.subheader("➕ إضافة منتج جديد للكتالوج")
            p_name = st.text_input("اسم المنتج الجديد")
            p_price = st.number_input("السعر بالجنيه", min_value=0.0)
            p_cat = st.selectbox("القسم", ["هوديس وملابس أسطورية", "أكسسوارات التنين", "عطور ملكية"])
            
            if st.button("حفظ وإضافة المنتج للمتجر"):
                if p_name:
                    p_id = str(len(products_db) + 1001)
                    products_db[p_id] = {"name": p_name, "price": p_price, "category": p_cat}
                    save_json(PRODUCTS_FILE, products_db)
                    st.success("تم إضافة المنتج بنجاح وسيظهر للعملاء فوراً!")
                else:
                    st.warning("أدخل اسم المنتج من فضلك.")
                    
        with tab2:
            st.subheader("📋 تحديث حالات الطلبات والشحن")
            if not orders_db:
                st.info("لا توجد طلبات مسجلة حتى الآن.")
            else:
                for o_id, o_det in orders_db.items():
                    with st.expander(f"طلب: {o_id} - {o_det.get('name')}"):
                        current_status = o_det.get("status", "قيد المعالجة ⏳")
                        new_stat = st.selectbox(
                            "تحديث الحالة:",
                            ["قيد المعالجة ⏳", "جاري الشحن 🚚", "تم التوصيل ✅"],
                            index=["قيد المعالجة ⏳", "جاري الشحن 🚚", "تم التوصيل ✅"].index(current_status),
                            key=f"st_{o_id}"
                        )
                        if st.button("تحديث الحالة", key=f"btn_{o_id}"):
                            orders_db[o_id]["status"] = new_stat
                            save_json(ORDERS_FILE, orders_db)
                            st.success("تم تحديث الحالة بنجاح!")