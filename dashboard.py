# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import base64
from io import BytesIO
from PIL import Image
import requests

# Page configuration
st.set_page_config(
    page_title="Real Estate Lead Engine Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 30px;
    }
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stat-number {
        font-size: 32px;
        font-weight: bold;
        color: #667eea;
    }
    .stat-label {
        color: #666;
        font-size: 14px;
    }
    .lead-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .lead-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .price-tag {
        color: #e74c3c;
        font-weight: bold;
        font-size: 20px;
    }
    .phone-number {
        color: #27ae60;
        font-weight: bold;
        font-size: 16px;
    }
    .seller-name {
        color: #8e44ad;
        font-weight: bold;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton > button:hover {
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)


# Load data function
@st.cache_data(ttl=300)
def load_data():
    """Load leads data from CSV files."""
    leads_file = "data/final_leads.csv"
    raw_file = "data/raw_details.csv"

    leads_df = pd.DataFrame()
    raw_df = pd.DataFrame()

    if os.path.exists(leads_file):
        leads_df = pd.read_csv(leads_file)

    if os.path.exists(raw_file):
        raw_df = pd.read_csv(raw_file)

    return leads_df, raw_df


def load_image_from_url(url):
    """Load image from URL."""
    try:
        if url and pd.notna(url):
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return Image.open(BytesIO(response.content))
    except:
        pass
    return None


def get_download_link(df, filename):
    """Generate download link for dataframe."""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" class="download-link">📥 Download CSV</a>'
    return href


# Header
st.markdown(
    '<div class="main-header"><h1>🏠 Real Estate Lead Engine Dashboard</h1><p>Professional Lead Management System</p></div>',
    unsafe_allow_html=True)

# Load data
leads_df, raw_df = load_data()

# Sidebar filters
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/real-estate.png", width=80)
    st.markdown("## 🔍 Filters")

    # Price range filter
    if not leads_df.empty and 'Price' in leads_df.columns:
        st.markdown("### 💰 Price Range")
        price_options = ["All", "Under 1 Crore", "1-5 Crore", "5-10 Crore", "10+ Crore"]
        price_filter = st.selectbox("Select Price Range", price_options)

    # Location filter
    if not leads_df.empty and 'Location' in leads_df.columns:
        st.markdown("### 📍 Location")
        locations = ["All"] + sorted(leads_df['Location'].dropna().unique().tolist())
        location_filter = st.selectbox("Select Location", locations)

    # Furnished filter
    if not leads_df.empty and 'Furnished' in leads_df.columns:
        st.markdown("### 🛋️ Furnished Status")
        furnished_options = ["All", "Furnished", "Unfurnished"]
        furnished_filter = st.selectbox("Select Status", furnished_options)

    # Bedrooms filter
    if not leads_df.empty and 'Bedrooms' in leads_df.columns:
        st.markdown("### 🛏️ Bedrooms")
        bed_options = ["All"] + sorted(leads_df['Bedrooms'].dropna().unique().tolist())
        bed_filter = st.selectbox("Select Bedrooms", bed_options)

    st.markdown("---")
    st.markdown("### 📊 Export Data")
    if not leads_df.empty:
        st.markdown(get_download_link(leads_df, "leads_export.csv"), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🚀 Actions")
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📋 Leads List", "📈 Analytics", "⚙️ Settings"])

# Tab 1: Dashboard
with tab1:
    if not leads_df.empty:
        # Apply filters
        filtered_df = leads_df.copy()

        if 'Price' in filtered_df.columns:
            if price_filter == "Under 1 Crore":
                filtered_df = filtered_df[filtered_df['Price'].astype(str).str.contains('Lac', na=False)]
            elif price_filter == "1-5 Crore":
                filtered_df = filtered_df[filtered_df['Price'].astype(str).str.contains('Crore', na=False)]
                filtered_df = filtered_df[~filtered_df['Price'].astype(str).str.contains('Lac', na=False)]
            elif price_filter == "5-10 Crore":
                # Custom filter logic
                pass
            elif price_filter == "10+ Crore":
                pass

        if location_filter != "All" and 'Location' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Location'] == location_filter]

        if furnished_filter != "All" and 'Furnished' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Furnished'] == furnished_filter]

        if bed_filter != "All" and 'Bedrooms' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Bedrooms'] == bed_filter]

        # Statistics row
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(filtered_df)}</div>
                <div class="stat-label">Total Leads</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            avg_price = "N/A"
            if 'Price' in filtered_df.columns and not filtered_df.empty:
                price_text = filtered_df['Price'].astype(str)
                avg_price = f"{len(price_text[price_text.str.contains('Crore', na=False)])} Cr+"
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{avg_price}</div>
                <div class="stat-label">Properties > 1 Crore</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            unique_locations = filtered_df['Location'].nunique() if 'Location' in filtered_df.columns else 0
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{unique_locations}</div>
                <div class="stat-label">Unique Locations</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            furnished_count = len(
                filtered_df[filtered_df['Furnished'] == 'Furnished']) if 'Furnished' in filtered_df.columns else 0
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{furnished_count}</div>
                <div class="stat-label">Furnished Properties</div>
            </div>
            """, unsafe_allow_html=True)

        # Charts row
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📍 Leads by Location")
            if 'Location' in filtered_df.columns and not filtered_df.empty:
                location_counts = filtered_df['Location'].value_counts().head(10)
                fig = px.bar(
                    x=location_counts.values,
                    y=location_counts.index,
                    orientation='h',
                    title="Top 10 Locations",
                    labels={'x': 'Number of Leads', 'y': 'Location'},
                    color=location_counts.values,
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### 🏠 Property Types")
            if 'Title' in filtered_df.columns and not filtered_df.empty:
                # Extract property type from title
                property_types = []
                keywords = ['House', 'Apartment', 'Flat', 'Plot', 'Bungalow', 'Villa', 'Commercial', 'Office']
                for title in filtered_df['Title'].fillna(''):
                    for kw in keywords:
                        if kw.lower() in title.lower():
                            property_types.append(kw)
                            break
                    else:
                        property_types.append('Other')

                type_counts = pd.Series(property_types).value_counts()
                fig = px.pie(
                    values=type_counts.values,
                    names=type_counts.index,
                    title="Property Type Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

        # Recent leads
        st.markdown("### 🆕 Recent Leads")
        recent_leads = filtered_df.head(10)

        for idx, row in recent_leads.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([2, 3, 1])
                with col1:
                    st.markdown(f"**{row.get('Title', 'N/A')[:60]}**")
                    st.markdown(f"📍 {row.get('Location', 'N/A')}")
                with col2:
                    st.markdown(f"<span class='price-tag'>{row.get('Price', 'N/A')}</span>", unsafe_allow_html=True)
                    st.markdown(f"<span class='phone-number'>{row.get('Phone', 'N/A')}</span>", unsafe_allow_html=True)
                with col3:
                    st.markdown(f"👤 {row.get('Seller', 'N/A')[:20]}")
                    st.markdown(f"📅 {row.get('Posted', 'N/A')}")
                st.divider()
    else:
        st.info("No leads found. Run the pipeline first to generate leads.")

# Tab 2: Leads List
with tab2:
    if not leads_df.empty:
        st.markdown("## 📋 All Leads")

        # Search box
        search_term = st.text_input("🔍 Search leads by title, location, or seller", "")

        if search_term:
            filtered_df = leads_df[
                leads_df['Title'].str.contains(search_term, case=False, na=False) |
                leads_df['Location'].str.contains(search_term, case=False, na=False) |
                leads_df['Seller'].str.contains(search_term, case=False, na=False)
                ]
        else:
            filtered_df = leads_df

        st.markdown(f"**Showing {len(filtered_df)} leads**")

        # Display leads as cards
        cols = st.columns(3)
        for idx, (_, row) in enumerate(filtered_df.iterrows()):
            with cols[idx % 3]:
                with st.container():
                    # Image
                    if 'ImageURL' in row and pd.notna(row.get('ImageURL')):
                        try:
                            img = load_image_from_url(row['ImageURL'])
                            if img:
                                st.image(img, use_container_width=True)
                        except:
                            st.image("https://via.placeholder.com/300x200?text=No+Image", use_container_width=True)
                    else:
                        st.image("https://via.placeholder.com/300x200?text=No+Image", use_container_width=True)

                    st.markdown(f"**{row.get('Title', 'N/A')[:50]}**")
                    st.markdown(f"<span class='price-tag'>{row.get('Price', 'N/A')}</span>", unsafe_allow_html=True)
                    st.markdown(f"📞 {row.get('Phone', 'N/A')}")
                    st.markdown(f"📍 {row.get('Location', 'N/A')}")
                    st.markdown(f"👤 {row.get('Seller', 'N/A')}")
                    st.markdown(f"📅 {row.get('Posted', 'N/A')}")

                    if st.button(f"View Details", key=f"btn_{idx}"):
                        st.session_state.selected_lead = row.to_dict()

                    st.divider()

        # Selected lead details
        if 'selected_lead' in st.session_state:
            st.markdown("## 📄 Lead Details")
            selected = st.session_state.selected_lead
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Title:** {selected.get('Title', 'N/A')}")
                st.markdown(f"**Price:** {selected.get('Price', 'N/A')}")
                st.markdown(f"**Location:** {selected.get('Location', 'N/A')}")
                st.markdown(f"**Phone:** {selected.get('Phone', 'N/A')}")
                st.markdown(f"**Seller:** {selected.get('Seller', 'N/A')}")
            with col2:
                st.markdown(f"**Area:** {selected.get('Area', 'N/A')}")
                st.markdown(f"**Bedrooms:** {selected.get('Bedrooms', 'N/A')}")
                st.markdown(f"**Bathrooms:** {selected.get('Bathrooms', 'N/A')}")
                st.markdown(f"**Furnished:** {selected.get('Furnished', 'N/A')}")
                st.markdown(f"**Active Ads:** {selected.get('ActiveAds', 'N/A')}")

            st.markdown(f"[🔗 View on OLX]({selected.get('Link', '#')})")

            if st.button("Close Details"):
                del st.session_state.selected_lead
                st.rerun()
    else:
        st.info("No leads found. Run the pipeline first.")

# Tab 3: Analytics
with tab3:
    if not leads_df.empty:
        st.markdown("## 📈 Advanced Analytics")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 💰 Price Distribution")
            if 'Price' in leads_df.columns:
                price_values = leads_df['Price'].astype(str)
                price_categories = []
                for p in price_values:
                    if 'Crore' in p:
                        price_categories.append('> 1 Crore')
                    elif 'Lac' in p:
                        price_categories.append('< 1 Crore')
                    else:
                        price_categories.append('Other')

                price_counts = pd.Series(price_categories).value_counts()
                fig = px.pie(
                    values=price_counts.values,
                    names=price_counts.index,
                    title="Price Distribution",
                    color_discrete_sequence=['#e74c3c', '#27ae60', '#95a5a6']
                )
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### 📅 Posted Timeline")
            if 'Posted' in leads_df.columns:
                posted_counts = leads_df['Posted'].value_counts().head(10)
                fig = px.bar(
                    x=posted_counts.index,
                    y=posted_counts.values,
                    title="Leads by Posting Time",
                    labels={'x': 'Time Posted', 'y': 'Number of Leads'},
                    color=posted_counts.values,
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 🏢 Top Sellers by Active Ads")
        if 'Seller' in leads_df.columns and 'ActiveAds' in leads_df.columns:
            top_sellers = leads_df.groupby('Seller')['ActiveAds'].first().sort_values(ascending=False).head(10)
            fig = px.bar(
                x=top_sellers.values,
                y=top_sellers.index,
                orientation='h',
                title="Top 10 Sellers by Active Ads",
                labels={'x': 'Active Ads', 'y': 'Seller'},
                color=top_sellers.values,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 📊 Summary Statistics")
        stats_data = {
            "Metric": ["Total Leads", "Unique Locations", "Unique Sellers", "Furnished", "With Phone Numbers"],
            "Value": [
                len(leads_df),
                leads_df['Location'].nunique() if 'Location' in leads_df.columns else 0,
                leads_df['Seller'].nunique() if 'Seller' in leads_df.columns else 0,
                len(leads_df[leads_df['Furnished'] == 'Furnished']) if 'Furnished' in leads_df.columns else 0,
                len(leads_df[leads_df['Phone'].notna()]) if 'Phone' in leads_df.columns else 0
            ]
        }
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
    else:
        st.info("No data available for analytics. Run the pipeline first.")

# Tab 4: Settings
with tab4:
    st.markdown("## ⚙️ Settings")

    st.markdown("### 📁 Data Files")

    files = ["data/raw_links.csv", "data/raw_details.csv", "data/filtered_leads.csv", "data/final_leads.csv"]
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            st.success(f"✅ {file} - {size:,} bytes")
        else:
            st.error(f"❌ {file} - Not found")

    st.markdown("### 🚀 Pipeline Controls")

    if st.button("🗑️ Clear Cache"):
        st.cache_data.clear()
        st.success("Cache cleared!")

    st.markdown("### 📊 About")
    st.info("""
    **Real Estate Lead Engine Dashboard**

    - Version: 1.0
    - Last Updated: {}\n
    - Features:
      - Real-time lead tracking
      - Advanced filtering
      - Interactive charts
      - Export capabilities
      - Image preview
    """.format(datetime.now().strftime("%Y-%m-%d")))

# Footer
st.markdown("---")
st.markdown(
    f"<p style='text-align: center; color: #666;'>© 2024 Real Estate Lead Engine | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>",
    unsafe_allow_html=True)