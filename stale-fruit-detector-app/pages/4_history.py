import streamlit as st
import pandas as pd
from datetime import datetime
import base64
from translation import TRANSLATIONS
from db_utils import get_predictions_by_user
from utils.style import apply_style
from utils.auth_utils import check_auth, logout
import sqlite3
from PIL import Image
import os

# Set page config - MUST be first Streamlit command
st.set_page_config(page_title="History - Stale Fruit Detector", layout="wide")

# Apply custom background color
st.markdown("""
    <style>
    .stApp {
        background-color: #6FE6FC !important;
    }
    </style>
""", unsafe_allow_html=True)

# Check authentication
check_auth()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'email' not in st.session_state:
    st.session_state.email = None

# Apply shared styles
apply_style()

# Add authentication JavaScript for session persistence
st.components.v1.html("""
<script>
// Check for stored token and add to URL if found
window.addEventListener('load', function() {
    const token = localStorage.getItem('login_token');
    if (token && !window.location.search.includes('token=')) {
        const separator = window.location.search ? '&' : '?';
        window.location.search += separator + 'token=' + encodeURIComponent(token);
    }
});
</script>
""", height=0)

# Add custom CSS for styling
st.markdown("""
<style>
    /* Header container styling */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        margin-bottom: 2rem;
        background: rgba(0, 0, 0, 0.1);
        border-radius: 10px;
    }

    .page-title {
        color: #000000;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
        flex: 2;
    }

    /* Custom delete button styling */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #EF4444, #DC2626) !important;
        color: white !important;
        padding: 0.5rem 1rem !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 500 !important;
        width: 200px !important;
        height: auto !important;
        float: right !important;
        margin-left: auto !important;
    }

    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #DC2626, #B91C1C) !important;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2) !important;
    }

    .delete-container {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 1rem;
        padding-right: 1rem;
    }
    
    /* Table styling */
    .dataframe {
        width: 100%;
        margin: 1rem 0;
        background: white;
        border-radius: 10px;
        overflow: hidden;
    }
    
    .dataframe th {
        background-color: #1a1a1a !important;
        color: white !important;
        padding: 12px 8px !important;
        border: 1px solid #333 !important;
        font-size: 14px !important;
        text-align: left !important;
    }
    
    .dataframe td {
        padding: 8px !important;
        border: 1px solid #ddd !important;
        color: #333 !important;
        font-size: 14px !important;
        line-height: 1.4 !important;
        text-align: left !important;
    }
    
    .fresh-row td {
        background-color: rgba(16, 185, 129, 0.2) !important;
        border-color: rgba(16, 185, 129, 0.3) !important;
    }

    .stale-row td {
        background-color: rgba(239, 68, 68, 0.2) !important;
        border-color: rgba(239, 68, 68, 0.3) !important;
    }
    
    .fresh-row:hover td {
        background-color: rgba(16, 185, 129, 0.3) !important;
    }

    .stale-row:hover td {
        background-color: rgba(239, 68, 68, 0.3) !important;
    }
    
    .model-type {
        font-family: monospace;
        padding: 2px 6px;
        border-radius: 4px;
        background-color: #333;
        display: inline-block;
        color: white;
    }

    /* Image hover styling */
    .image-hover-text {
        color: #4CAF50;
        text-decoration: underline;
        cursor: pointer;
        position: relative;
        display: inline-block;
    }

    .image-preview {
        display: none;
        position: fixed;
        z-index: 1000;
        background: rgba(0, 0, 0, 0.9);
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 0 20px rgba(255,255,255,0.2);
        pointer-events: none;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .image-hover-text:hover .image-preview {
        display: block;
        position: absolute;
        top: 100%;
        left: 50%;
        transform: translateX(-50%);
        margin-top: 10px;
    }

    .image-preview img {
        max-width: 300px;
        max-height: 300px;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# --- Language Selection ---
lang = st.sidebar.selectbox("🌐 Select Language", ["English", "Telugu", "Hindi"])
tr = TRANSLATIONS["history"][lang]

# Add logout option in sidebar if logged in
if st.session_state.logged_in:
    with st.sidebar:
        if st.button("Logout"):
            logout()

# Check if user is logged in
if not st.session_state.logged_in:
    st.error(tr["login_required"])
    if st.button(tr["go_to_login"]):
        st.switch_page("pages/2_login.py")
    st.stop()

# Main Content
st.markdown(f"""
    <div class="header-container">
        <div style="flex: 1;"></div>
        <h1 class="page-title">{tr['title']}</h1>
        <div style="flex: 1;"></div>
    </div>
""", unsafe_allow_html=True)

def format_timestamp(timestamp):
    """Format timestamp in a consistent way"""
    try:
        if isinstance(timestamp, str):
            dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        else:
            dt = timestamp
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except Exception as e:
        return str(timestamp)

def format_image_cell(image_path):
    if image_path and os.path.exists(image_path):
        try:
            with Image.open(image_path) as img:
                # Create a smaller thumbnail
                img.thumbnail((300, 300))
                # Convert image to base64
                import io
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format=img.format)
                img_byte_arr = img_byte_arr.getvalue()
                encoded = base64.b64encode(img_byte_arr).decode()
                
                return f"""
                    <span class="image-hover-text">
                        View Image
                        <div class="image-preview">
                            <img src="data:image/{img.format.lower()};base64,{encoded}" alt="Preview">
                        </div>
                    </span>
                """
        except Exception as e:
            return "Error loading image"
    return "No image available"

def format_model_type(model_type):
    """Format model type with consistent styling"""
    return f'<span class="model-type">{model_type}</span>'

def main():
    # Apply shared styles
    apply_style()

    try:
        # Get predictions
        predictions = get_predictions_by_user(st.session_state["email"])
        
        if not predictions:
            st.info(tr["no_predictions"])
            st.stop()
        
        # Convert predictions to DataFrame
        df = pd.DataFrame(predictions, columns=[
            tr["result"],
            tr["timestamp"],
            "Model",
            "Storage Condition",
            "Storage Recommendation", 
            "Image"
        ])
        
        # Format timestamp
        df[tr["timestamp"]] = df[tr["timestamp"]].apply(format_timestamp)
        
        # Format model type
        df["Model"] = df["Model"].apply(format_model_type)
        
        # Format storage condition - only show if available
        df["Storage Condition"] = df["Storage Condition"].apply(lambda x: x if x and x != "None" else "")
        
        # Format storage recommendation - only show if available  
        df["Storage Recommendation"] = df["Storage Recommendation"].apply(lambda x: x if x and x != "None" else "")
        
        # Format image column
        df["Image"] = df["Image"].apply(format_image_cell)
        
        # Create download version (clean version without HTML tags)
        df_download = df.copy()
        df_download["Model"] = df_download["Model"].apply(lambda x: x.replace('<span class="model-type">', '').replace('</span>', ''))
        df_download["Image"] = df_download["Image"].apply(lambda x: "Image Available" if "View Image" in x else "No Image")
        
        # Add delete history button
        with st.container():
            if st.button("🗑️ Clear History", type="secondary", help="Delete all your prediction history"):
                if st.session_state.get("confirm_delete", False):
                    # Delete all predictions for this user
                    from db_utils import client, db
                    predictions_collection = db["predictions"]
                    result = predictions_collection.delete_many({"user_email": st.session_state["email"]})
                    
                    if result.deleted_count > 0:
                        st.success(f"Successfully deleted {result.deleted_count} predictions from your history!")
                        st.rerun()
                    else:
                        st.info("No history to delete.")
                    st.session_state.confirm_delete = False
                else:
                    st.session_state.confirm_delete = True
                    st.warning("⚠️ Are you sure you want to delete all your history? Click the button again to confirm.")
        
        # Add some space after the delete button
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Convert DataFrame to HTML and apply row colors
        html = df.to_html(escape=False, index=False)
        
        # Apply row colors based on result
        for i, row in df.iterrows():
            result = row[tr["result"]]
            if "FRESH" in result.upper():
                html = html.replace(f'<tr><td>{result}', f'<tr class="fresh-row"><td>{result}')
            elif "STALE" in result.upper():
                html = html.replace(f'<tr><td>{result}', f'<tr class="stale-row"><td>{result}')
        
        st.write(html, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error loading prediction history: {str(e)}")
        st.error("Please try refreshing the page. If the problem persists, contact support.")

if __name__ == "__main__":
    main() 