import streamlit as st
import pandas as pd
import numpy as np
import joblib


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚘",
    layout="wide"
)


# =========================================================
# SESSION STATE PAGE
# =========================================================
if "page" not in st.session_state:
    st.session_state.page = "Home"


# =========================================================
# CUSTOM CSS UI: MICROSOFT LUMIA / METRO STYLE + ANIMATION
# =========================================================
st.markdown("""
<style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(0, 120, 215, 0.22), transparent 30%),
            radial-gradient(circle at bottom right, rgba(227, 0, 140, 0.18), transparent 32%),
            #111111;
        color: white;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1280px;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    @keyframes fadeSlideUp {
        from {opacity: 0; transform: translateY(28px);}
        to {opacity: 1; transform: translateY(0);}
    }

    @keyframes fadeSlideLeft {
        from {opacity: 0; transform: translateX(-28px);}
        to {opacity: 1; transform: translateX(0);}
    }

    @keyframes pulseGlow {
        0% {box-shadow: 0 0 0 rgba(0, 183, 195, 0.0);}
        50% {box-shadow: 0 0 28px rgba(0, 183, 195, 0.28);}
        100% {box-shadow: 0 0 0 rgba(0, 183, 195, 0.0);}
    }

    .animated-page {
        animation: fadeSlideUp 0.65s ease-out;
    }

    .animated-left {
        animation: fadeSlideLeft 0.65s ease-out;
    }

    .metro-header {
        background: linear-gradient(135deg, #0078D7 0%, #5C2D91 100%);
        padding: 2rem 2.2rem;
        border-radius: 0px;
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.35);
        margin-bottom: 1.2rem;
        color: white;
        border-left: 8px solid #00B7C3;
        animation: fadeSlideUp 0.65s ease-out;
    }

    .metro-title {
        font-size: 2.35rem;
        font-weight: 900;
        line-height: 1.15;
        letter-spacing: -0.04em;
        margin-bottom: 1rem;
    }

    .metro-subtitle {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.88);
        margin-top: 1rem;
        margin-bottom: 0;
        font-weight: 500;
    }

    .team-list {
        margin-top: 0.8rem;
        margin-bottom: 0.8rem;
        color: rgba(255, 255, 255, 0.95);
        font-size: 0.98rem;
        line-height: 1.65;
        font-weight: 500;
        padding-left: 1.2rem;
    }

    .team-list li {
        margin: 0.1rem 0;
        padding-left: 0.25rem;
    }

    .metro-tile {
        padding: 1.35rem;
        min-height: 130px;
        color: white;
        border-radius: 0px;
        box-shadow: 0 14px 32px rgba(0, 0, 0, 0.32);
        margin-bottom: 1rem;
        transition: transform 0.18s ease-in-out, box-shadow 0.18s ease-in-out;
        animation: fadeSlideUp 0.75s ease-out;
    }

    .metro-tile:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 48px rgba(0, 0, 0, 0.48);
    }

    .tile-blue {background: #0078D7;}
    .tile-cyan {background: #00B7C3;}
    .tile-green {background: #107C10;}
    .tile-purple {background: #5C2D91;}
    .tile-magenta {background: #E3008C;}
    .tile-orange {background: #F7630C;}
    .tile-red {background: #D13438;}
    .tile-dark {
        background: #1B1B1B;
        border: 1px solid rgba(255, 255, 255, 0.12);
    }

    .tile-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 850;
        opacity: 0.9;
        margin-bottom: 0.55rem;
    }

    .tile-value {
        font-size: 1.45rem;
        font-weight: 900;
        line-height: 1.18;
        letter-spacing: -0.03em;
    }

    .tile-small {
        font-size: 0.88rem;
        font-weight: 600;
        opacity: 0.9;
        margin-top: 0.4rem;
    }

    .tile-number {
        font-size: 2.1rem;
        font-weight: 950;
        line-height: 1;
        letter-spacing: -0.05em;
    }

    .metro-card {
        background: rgba(255, 255, 255, 0.96);
        color: #111111;
        padding: 1.5rem;
        border-radius: 0px;
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.38);
        margin-bottom: 1.2rem;
        border-top: 8px solid #0078D7;
        animation: fadeSlideUp 0.75s ease-out;
    }

    .metro-card-purple {border-top: 8px solid #5C2D91;}
    .metro-card-green {border-top: 8px solid #107C10;}
    .metro-card-magenta {border-top: 8px solid #E3008C;}
    .metro-card-orange {border-top: 8px solid #F7630C;}
    .metro-card-cyan {border-top: 8px solid #00B7C3;}

    .metro-card-title {
        font-size: 1.35rem;
        font-weight: 900;
        color: #111111;
        margin-bottom: 0.35rem;
        letter-spacing: -0.03em;
    }

    .metro-card-desc {
        font-size: 0.92rem;
        color: #555555;
        margin-bottom: 1.1rem;
        font-weight: 500;
    }

    div[data-baseweb="select"] > div {
        border-radius: 0px;
        border: 2px solid #d0d0d0;
        min-height: 44px;
        box-shadow: none;
    }

    div[data-baseweb="select"] > div:focus-within {
        border-color: #0078D7;
    }

    div[data-baseweb="input"] > div {
        border-radius: 0px;
        border: 2px solid #d0d0d0;
        min-height: 44px;
        box-shadow: none;
    }

    .stNumberInput input {
        border-radius: 0px;
    }

    label {
        font-weight: 850 !important;
        color: #222222 !important;
        font-size: 0.92rem !important;
    }

    div[data-testid="stAlert"] {
        border-radius: 0px;
        border-left: 7px solid #0078D7;
        box-shadow: none;
    }

    .stButton > button {
        width: 100%;
        height: 3.5rem;
        border-radius: 0px;
        border: none;
        background: linear-gradient(135deg, #E3008C 0%, #D13438 100%);
        color: white;
        font-weight: 950;
        font-size: 1rem;
        box-shadow: 0 12px 26px rgba(227, 0, 140, 0.28);
        transition: all 0.18s ease-in-out;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 16px 36px rgba(227, 0, 140, 0.42);
        color: white;
    }

    .result-tile {
        background: linear-gradient(135deg, #107C10 0%, #00B7C3 100%);
        color: white;
        padding: 2rem;
        border-radius: 0px;
        box-shadow: 0 18px 42px rgba(0, 0, 0, 0.38);
        margin-bottom: 1.2rem;
        animation: pulseGlow 2.4s infinite ease-in-out;
    }

    .result-label {
        font-size: 0.9rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        opacity: 0.9;
        margin-bottom: 0.6rem;
    }

    .result-price {
        font-size: 2.85rem;
        font-weight: 950;
        letter-spacing: -0.06em;
        line-height: 1.05;
        margin-bottom: 0.65rem;
    }

    .result-caption {
        font-size: 0.95rem;
        font-weight: 650;
        opacity: 0.9;
    }

    .empty-result-tile {
        background: #1B1B1B;
        color: white;
        padding: 2rem;
        border-radius: 0px;
        border-left: 8px solid #F7630C;
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.36);
        margin-bottom: 1.2rem;
        animation: fadeSlideUp 0.75s ease-out;
    }

    .empty-result-title {
        font-size: 1.2rem;
        font-weight: 950;
        margin-bottom: 0.4rem;
    }

    .empty-result-desc {
        font-size: 0.92rem;
        color: rgba(255, 255, 255, 0.78);
        font-weight: 500;
    }

    .nav-card {
        background: rgba(255, 255, 255, 0.96);
        color: #111111;
        padding: 1rem;
        margin-bottom: 1.2rem;
        border-left: 8px solid #00B7C3;
        animation: fadeSlideLeft 0.65s ease-out;
    }

    .nav-title {
        font-size: 1rem;
        font-weight: 900;
        margin-bottom: 0.35rem;
    }

    .nav-desc {
        font-size: 0.88rem;
        color: #555555;
        font-weight: 500;
    }

    .footer {
        text-align: center;
        color: rgba(255, 255, 255, 0.56);
        font-size: 0.9rem;
        margin-top: 2rem;
        font-weight: 600;
    }

    @media (max-width: 768px) {
        .metro-title {font-size: 1.55rem;}
        .result-price {font-size: 2.2rem;}
        .metro-header {padding: 1.5rem;}
        .metro-tile {min-height: auto;}
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA & MODEL
# =========================================================
@st.cache_data
def load_data():
    # Ganti ke CSV jika file final kamu .csv
    try:
        return pd.read_excel("cars_final_processed.xlsx")
    except Exception:
        return pd.read_csv("test.csv")


@st.cache_resource
def load_model():
    return joblib.load("car_price_prediction_best_model.pkl")


try:
    df_raw = load_data()
    model = load_model()
    data_ready = True
except Exception as e:
    st.error(f"Failed to load data or model: {e}")
    data_ready = False


# =========================================================
# HELPER FUNCTIONS
# =========================================================
def get_expected_columns(model):
    try:
        return list(model.feature_names_in_)
    except Exception:
        pass

    try:
        return list(model.named_steps["preprocessor"].feature_names_in_)
    except Exception:
        pass

    return None


def get_brand_origin(brand):
    brand = str(brand).strip().lower()

    asia_brands = [
        "toyota", "lexus", "scion",
        "honda", "acura",
        "nissan", "infiniti",
        "mazda", "subaru", "mitsubishi", "suzuki",
        "hyundai", "kia", "genesis"
    ]

    america_brands = [
        "ford", "lincoln",
        "chevrolet", "gmc", "cadillac", "buick",
        "dodge", "chrysler", "jeep", "ram",
        "tesla", "pontiac", "saturn", "mercury",
        "hummer", "plymouth"
    ]

    europe_brands = [
        "bmw", "mini", "rolls-royce",
        "mercedes-benz", "maybach", "smart",
        "audi", "volkswagen", "porsche", "bentley", "bugatti",
        "volvo", "jaguar", "land rover",
        "aston martin", "maserati", "ferrari", "lamborghini",
        "alfa romeo", "fiat", "lotus", "mclaren", "saab"
    ]

    if brand in asia_brands:
        return "Asia"
    elif brand in america_brands:
        return "America"
    elif brand in europe_brands:
        return "Europe"
    else:
        return "Others"


def get_color_group(color):
    color = str(color).lower()
    neutral_colors = ["black", "white", "silver", "gray", "grey"]

    if any(neutral in color for neutral in neutral_colors):
        return "Neutral"
    return "Exotic"


def align_input_columns(input_df, model):
    expected_cols = get_expected_columns(model)

    if expected_cols is None:
        return input_df

    for col in expected_cols:
        if col not in input_df.columns:
            input_df[col] = 0

    return input_df[expected_cols]


def go_home():
    st.session_state.page = "Home"


def go_prediction():
    st.session_state.page = "Prediction"


# =========================================================
# UI START
# =========================================================
if data_ready:

    # =====================================================
    # PAGE 1: HOME
    # =====================================================
    if st.session_state.page == "Home":
        st.markdown('<div class="animated-page">', unsafe_allow_html=True)

        st.markdown("""
        <div class="metro-header">
            <div class="metro-title">🚘 Final Project Data Science Group 7 : Team Outliers</div>
            <ol class="team-list">
                <li>Artorius Weelyn Jawra (Ketua)</li>
                <li>Fabian Rashed Majduddin</li>
                <li>Kurniati</li>
                <li>Gunaryono Ary</li>
                <li>Hashfi Hawali</li>
            </ol>
            <p class="metro-subtitle">Used car price prediction based on vehicle specifications.</p>
        </div>
        """, unsafe_allow_html=True)

        home_col1, home_col2, home_col3 = st.columns(3)

        with home_col1:
            st.markdown("""
            <div class="metro-tile tile-blue">
                <div class="tile-label">Project Type</div>
                <div class="tile-value">Regression</div>
                <div class="tile-small">Used car price prediction</div>
            </div>
            """, unsafe_allow_html=True)

        with home_col2:
            st.markdown("""
            <div class="metro-tile tile-purple">
                <div class="tile-label">Model Output</div>
                <div class="tile-value">Estimated Price</div>
                <div class="tile-small">Market value prediction</div>
            </div>
            """, unsafe_allow_html=True)

        with home_col3:
            st.markdown("""
            <div class="metro-tile tile-magenta">
                <div class="tile-label">Interface Style</div>
                <div class="tile-value">Metro UI</div>
                <div class="tile-small">Microsoft Lumia inspired</div>
            </div>
            """, unsafe_allow_html=True)

        insight_col1, insight_col2, insight_col3, insight_col4 = st.columns(4)

        with insight_col1:
            st.markdown(f"""
            <div class="metro-tile tile-green">
                <div class="tile-label">Total Records</div>
                <div class="tile-number">{len(df_raw):,}</div>
                <div class="tile-small">rows in dataset</div>
            </div>
            """, unsafe_allow_html=True)

        with insight_col2:
            st.markdown(f"""
            <div class="metro-tile tile-orange">
                <div class="tile-label">Total Brands</div>
                <div class="tile-number">{df_raw['brand'].nunique()}</div>
                <div class="tile-small">unique car brands</div>
            </div>
            """, unsafe_allow_html=True)

        with insight_col3:
            st.markdown(f"""
            <div class="metro-tile tile-red">
                <div class="tile-label">Total Models</div>
                <div class="tile-number">{df_raw['model'].nunique()}</div>
                <div class="tile-small">unique car models</div>
            </div>
            """, unsafe_allow_html=True)

        with insight_col4:
            st.markdown(f"""
            <div class="metro-tile tile-dark">
                <div class="tile-label">Median Mileage</div>
                <div class="tile-number">{int(df_raw['milage'].median()):,}</div>
                <div class="tile-small">miles</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="metro-card metro-card-cyan">
            <div class="metro-card-title">Project Overview</div>
            <div class="metro-card-desc">
                This application predicts used car market prices using selected vehicle specifications.
                The interface is designed with a Microsoft Lumia / Metro-inspired tile layout.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.button("Go to Prediction Page", on_click=go_prediction, type="primary")

        st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # PAGE 2: PREDICTION
    # =====================================================
    elif st.session_state.page == "Prediction":
        st.markdown('<div class="animated-page">', unsafe_allow_html=True)

        st.markdown("""
        <div class="nav-card">
            <div class="nav-title">Prediction Page</div>
            <div class="nav-desc">Select vehicle specifications and generate estimated used car market price.</div>
        </div>
        """, unsafe_allow_html=True)

        nav_col1, nav_col2 = st.columns([0.2, 0.8])
        with nav_col1:
            st.button("Back to Home", on_click=go_home)

        st.markdown("""
        <div class="metro-header">
            <div class="metro-title">🚘 Car Price Prediction App</div>
            <p class="metro-subtitle">Input vehicle specifications and predict estimated market price.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="metro-card metro-card-purple">
            <div class="metro-card-title">Vehicle Selection</div>
            <div class="metro-card-desc">Select the vehicle identity before entering technical specifications.</div>
        </div>
        """, unsafe_allow_html=True)

        select_col1, select_col2, select_col3 = st.columns(3)

        with select_col1:
            brand_list = sorted(df_raw["brand"].dropna().unique())
            selected_brand = st.selectbox("Brand", brand_list)

        with select_col2:
            filtered_models = df_raw[df_raw["brand"] == selected_brand]
            model_list = sorted(filtered_models["model"].dropna().unique())
            selected_model = st.selectbox("Model", model_list)

        with select_col3:
            filtered_years = filtered_models[filtered_models["model"] == selected_model]
            year_list = sorted(filtered_years["model_year"].dropna().unique(), reverse=True)
            selected_year = st.selectbox("Model Year", year_list)

        exact_car = filtered_years[filtered_years["model_year"] == selected_year]

        brand_origin = get_brand_origin(selected_brand)
        similar_records = len(exact_car)

        median_milage = int(exact_car["milage"].median()) if "milage" in exact_car else 0
        median_hp = round(exact_car["horsepower"].median(), 1) if "horsepower" in exact_car else 0
        median_engine = round(exact_car["engine_liter"].median(), 1) if "engine_liter" in exact_car else 0

        st.markdown("<br>", unsafe_allow_html=True)

        tile_col1, tile_col2, tile_col3, tile_col4 = st.columns(4)

        with tile_col1:
            st.markdown(f"""
            <div class="metro-tile tile-blue">
                <div class="tile-label">Brand</div>
                <div class="tile-value">{selected_brand}</div>
                <div class="tile-small">Selected manufacturer</div>
            </div>
            """, unsafe_allow_html=True)

        with tile_col2:
            st.markdown(f"""
            <div class="metro-tile tile-purple">
                <div class="tile-label">Model</div>
                <div class="tile-value">{selected_model}</div>
                <div class="tile-small">Selected vehicle model</div>
            </div>
            """, unsafe_allow_html=True)

        with tile_col3:
            st.markdown(f"""
            <div class="metro-tile tile-cyan">
                <div class="tile-label">Model Year</div>
                <div class="tile-value">{selected_year}</div>
                <div class="tile-small">Production year</div>
            </div>
            """, unsafe_allow_html=True)

        with tile_col4:
            st.markdown(f"""
            <div class="metro-tile tile-magenta">
                <div class="tile-label">Brand Origin</div>
                <div class="tile-value">{brand_origin}</div>
                <div class="tile-small">Detected automatically</div>
            </div>
            """, unsafe_allow_html=True)

        insight_col1, insight_col2, insight_col3, insight_col4 = st.columns(4)

        with insight_col1:
            st.markdown(f"""
            <div class="metro-tile tile-green">
                <div class="tile-label">Similar Records</div>
                <div class="tile-number">{similar_records}</div>
                <div class="tile-small">cars found in dataset</div>
            </div>
            """, unsafe_allow_html=True)

        with insight_col2:
            st.markdown(f"""
            <div class="metro-tile tile-orange">
                <div class="tile-label">Median Mileage</div>
                <div class="tile-number">{median_milage:,}</div>
                <div class="tile-small">miles</div>
            </div>
            """, unsafe_allow_html=True)

        with insight_col3:
            st.markdown(f"""
            <div class="metro-tile tile-red">
                <div class="tile-label">Median Horsepower</div>
                <div class="tile-number">{median_hp}</div>
                <div class="tile-small">HP</div>
            </div>
            """, unsafe_allow_html=True)

        with insight_col4:
            st.markdown(f"""
            <div class="metro-tile tile-dark">
                <div class="tile-label">Median Engine</div>
                <div class="tile-number">{median_engine}L</div>
                <div class="tile-small">engine capacity</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        left_col, right_col = st.columns([1.25, 0.75], gap="large")

        with left_col:
            st.markdown("""
            <div class="metro-card">
                <div class="metro-card-title">Technical Specifications</div>
                <div class="metro-card-desc">Complete the specification details to generate the estimated market price.</div>
            """, unsafe_allow_html=True)

            with st.form("spec_form"):
                st.info(f"Detected Brand Origin: **{brand_origin}**")

                input_col1, input_col2 = st.columns(2)

                with input_col1:
                    milage = st.number_input(
                        "Mileage",
                        min_value=0,
                        value=median_milage
                    )

                    hp_options = sorted(exact_car["horsepower"].dropna().unique().tolist())
                    el_options = sorted(exact_car["engine_liter"].dropna().unique().tolist())
                    cyl_options = sorted(exact_car["cylinders"].dropna().unique().tolist())

                    horsepower = st.selectbox("Horsepower", hp_options) if hp_options else st.number_input("Horsepower", value=median_hp)
                    engine_liter = st.selectbox("Engine Liter", el_options) if el_options else st.number_input("Engine Liter", value=median_engine)
                    cylinders = st.selectbox("Cylinders", cyl_options) if cyl_options else st.number_input("Cylinders", value=4.0)

                with input_col2:
                    fuel_options = exact_car["fuel_type"].dropna().unique().tolist()
                    trans_options = exact_car["transmission"].dropna().unique().tolist()

                    fuel_type = st.selectbox("Fuel Type", fuel_options) if fuel_options else st.selectbox("Fuel Type", ["Gasoline", "Hybrid", "Diesel", "Electric"])
                    transmission = st.selectbox("Transmission", trans_options) if trans_options else st.selectbox("Transmission", ["Automatic", "Manual", "CVT", "Dual Shift", "Other"])

                    accident = st.selectbox("Accident", ["None Reported", "Accident Reported"])
                    ext_col = st.selectbox("Exterior Color Group", ["Neutral", "Exotic"])
                    int_col = st.selectbox("Interior Color Group", ["Neutral", "Exotic"])

                st.markdown("<br>", unsafe_allow_html=True)
                predict_btn = st.form_submit_button("Predict Market Price", type="primary")

            st.markdown("</div>", unsafe_allow_html=True)

        if predict_btn:
            acc_val = 0 if accident == "None Reported" else 1

            input_df = pd.DataFrame({
                "brand": [selected_brand],
                "model": [selected_model],
                "model_year": [selected_year],
                "milage": [milage],
                "fuel_type": [fuel_type],
                "transmission": [transmission],
                "accident": [acc_val],
                "horsepower": [horsepower],
                "engine_liter": [engine_liter],
                "cylinders": [cylinders],
                "brand_origin": [brand_origin],
                "ext_col_group": [ext_col],
                "int_col_group": [int_col]
            })

            input_df = align_input_columns(input_df, model)

            try:
                pred_log = model.predict(input_df)
                final_price = np.expm1(pred_log)[0]

                st.session_state.final_price = final_price
                st.session_state.prediction_caption = f"Prediction for {selected_brand} {selected_model} ({selected_year})"

            except Exception as e:
                st.error(f"Prediction error occurred: {e}")
                st.write("Input columns:")
                st.write(input_df.columns.tolist())

        with right_col:
            if "final_price" in st.session_state:
                st.markdown(f"""
                <div class="result-tile">
                    <div class="result-label">Estimated Market Price</div>
                    <div class="result-price">${st.session_state.final_price:,.2f}</div>
                    <div class="result-caption">{st.session_state.prediction_caption}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="empty-result-tile">
                    <div class="empty-result-title">No Prediction Yet</div>
                    <div class="empty-result-desc">
                        Complete the technical specifications and click Predict Market Price.
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="metro-header">
        <div class="metro-title">🚘 Final Project Data Science Group 7 : Team Outliers</div>
        <p class="metro-subtitle">Used car price prediction based on vehicle specifications.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='footer'>Developed by Fabian RM</div>", unsafe_allow_html=True)