import streamlit as st
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import torch.nn.functional as F
import urllib.request
import os
import base64
import time
import uuid
import matplotlib.pyplot as plt
from db_utils import save_prediction, get_predictions_by_user
from translation import TRANSLATIONS
import logging
import torch.nn as nn
import gdown
from utils.style import apply_style
import sqlite3
from datetime import datetime
import io
import numpy as np
from config import (
    BASE_DIR, MODEL_DIR, VIT_MODEL_PATH, SWIN_MODEL_PATH, 
    SHELF_LIFE_MODEL_PATH, UPLOAD_DIR, BACKGROUND_DIR,
    VIT_MODEL_ID, SWIN_MODEL_ID, SHELF_LIFE_MODEL_ID
)
from model_utils import (
    ViT, SwinTransformer, shelf_life_data,
    shelf_life_class_names, fruit_keywords,
    condition_indicators
)
from utils.auth_utils import check_auth, logout

# Set page config - MUST be first Streamlit command
st.set_page_config(page_title="Stale Fruit Detector", layout="wide")

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'email' not in st.session_state:
    st.session_state.email = None
if 'model_choice' not in st.session_state:
    st.session_state.model_choice = "ViT"  # Default to ViT model

# Check authentication
check_auth()

# Check if user is logged in
if not st.session_state.logged_in:
    st.warning("Please log in to access the Fruit Freshness Detection App")
    if st.button("Go to Login"):
        st.switch_page("pages/2_login.py")
    st.stop()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load ImageNet class names
try:
    from torchvision.models import ResNet50_Weights
    imagenet_classes = ResNet50_Weights.DEFAULT.meta["categories"]
except:
    # Fallback for older torchvision versions
    import json
    import urllib.request
    LABELS_URL = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
    try:
        with urllib.request.urlopen(LABELS_URL) as response:
            imagenet_classes = [line.decode('utf-8').strip() for line in response.readlines()]
        logger.info("ImageNet classes loaded from URL")
    except:
        logger.error("Failed to load ImageNet classes")
        imagenet_classes = []

# Apply custom styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&family=Inter:wght@400;500&display=swap');
    
    .stApp {
        background-color: #FFFBEA;
    }

    /* Glass Container Styling */
    .glass-container {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        padding: 2rem;
        margin: 1.5rem auto;
        max-width: 800px;
        text-align: center;
    }

    /* Header Styles */
    .app-header {
        text-align: center;
        margin-bottom: 1.5rem;
    }

    .app-header h1 {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: #2C3E50;
        font-size: 2rem;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }

    .app-header p {
        font-family: 'Inter', sans-serif;
        color: #4A5568;
        font-size: 1.1rem;
        line-height: 1.5;
    }

    /* Upload Section Styling */
    .upload-section {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        transition: all 0.3s ease;
    }

    .upload-zone {
        border: 2px dashed rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .upload-zone:hover {
        border-color: #F34949;
        background: rgba(255, 255, 255, 0.05);
        transform: translateY(-2px);
    }

    .upload-icon {
        font-size: 2rem;
        color: #4A5568;
        margin-bottom: 0.75rem;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
        100% { transform: translateY(0px); }
    }

    .upload-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: #4A5568;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }

    .upload-text {
        font-family: 'Inter', sans-serif;
        color: #718096;
        font-size: 0.9rem;
        margin: 0.25rem 0;
        line-height: 1.5;
    }

    /* Image Preview Styling */
    .image-preview-container {
        margin: 1rem auto;
        max-width: 200px;
        width: 100%;
        overflow: hidden;
    }

    .image-preview {
        width: 100%;
        height: auto;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }

    .image-preview:hover {
        transform: scale(1.02);
    }

    /* Hide default Streamlit uploader - REMOVED to fix drag and drop */
    /* .stFileUploader > div {
        padding: 0 !important;
    }

    .stFileUploader > div > div {
        padding: 0 !important;
    }

    .stFileUploader [data-testid="stFileUploadDropzone"] {
        min-height: 0 !important;
        padding: 0 !important;
        background: transparent !important;
        border: none !important;
    } */

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .upload-section {
            padding: 1rem;
            margin: 0.75rem 0;
        }

        .upload-zone {
            padding: 1rem;
        }

        .upload-icon {
            font-size: 1.75rem;
        }

        .upload-title {
            font-size: 1rem;
        }

        .upload-text {
            font-size: 0.85rem;
        }

        .image-preview-container {
            max-width: 150px;
        }
    }

    /* Result Section Styling */
    .result-container {
        background: rgba(255, 255, 255, 0.25);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        font-family: 'Inter', sans-serif;
    }

    .result-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: #2C3E50;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }

    .result-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0.5rem 0;
        color: #2C3E50;
        font-size: 0.95rem;
    }

    .success-icon {
        color: #10B981;
        font-size: 1.1rem;
    }

    .error-icon {
        color: #EF4444;
        font-size: 1.1rem;
    }

    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeIn 0.5s ease-out forwards;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Add Tips Notifier Styling */
    .tips-notifier {
        position: fixed;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1rem 1.5rem;
        z-index: 1000;
        max-width: 90%;
        width: auto;
        text-align: center;
        animation: fadeIn 0.5s ease-out;
    }

    .tips-notifier h4 {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: #4A5568;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }

    .tips-notifier ul {
        list-style: none;
        padding: 0;
        margin: 0;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: #718096;
    }

    .tips-notifier li {
        margin: 0.25rem 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }

    .tips-notifier li::before {
        content: "•";
        color: #F34949;
        font-weight: bold;
    }

    @media (max-width: 768px) {
        .tips-notifier {
            bottom: 1rem;
            padding: 0.75rem 1rem;
        }
        
        .tips-notifier h4 {
            font-size: 0.9rem;
        }
        
        .tips-notifier ul {
            font-size: 0.8rem;
        }
    }

    /* Collapsible Tips Section */
    .tips-section {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1.5rem 0;
        overflow: hidden;
    }

    .tips-header {
        padding: 1rem 1.5rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.3s ease;
    }

    .tips-header:hover {
        background: rgba(255, 255, 255, 0.05);
    }

    .tips-header h4 {
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
        color: #4A5568;
        font-size: 1rem;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .tips-header .icon {
        transition: transform 0.3s ease;
        font-size: 1.2rem;
        color: #4A5568;
    }

    .tips-content {
        max-height: 0;
        opacity: 0;
        transition: all 0.3s ease-in-out;
        padding: 0 1.5rem;
        overflow: hidden;
    }

    .tips-content.show {
        max-height: 500px;
        opacity: 1;
        padding: 1rem 1.5rem;
    }

    .tips-list {
        list-style: none;
        padding: 0;
        margin: 0;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #718096;
    }

    .tips-list li {
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .tips-list li::before {
        content: "•";
        color: #F34949;
        font-weight: bold;
    }

    @media (max-width: 768px) {
        .tips-section {
            margin: 1rem 0;
        }
        
        .tips-header {
            padding: 0.75rem 1rem;
        }
        
        .tips-content.show {
            padding: 0.75rem 1rem;
        }
    }

    /* Hide the default streamlit uploader label - REMOVED to fix drag and drop */
    /* .stFileUploader > label {
        display: none !important;
    } */

    /* Style the upload box - REMOVED to fix drag and drop */
    /* .upload-section {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }

    .upload-zone {
        border: 2px dashed rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .upload-icon {
        font-size: 2rem;
        color: #4A5568;
        margin-bottom: 0.75rem;
    }

    .upload-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: #4A5568;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }

    .upload-text {
        font-family: 'Inter', sans-serif;
        color: #718096;
        font-size: 0.9rem;
        margin: 0.25rem 0;
    } */

    /* Position the streamlit uploader inside our custom box */
    .stFileUploader {
        position: relative;
        z-index: 1;
    }

    .upload-container {
        position: relative;
    }

    /* Make the default uploader transparent and overlay it - REMOVED to fix drag and drop */
    /* .stFileUploader > div {
        background: transparent !important;
        border: none !important;
    } */
    </style>
""", unsafe_allow_html=True)

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

# --- Language Selection ---
lang = st.sidebar.selectbox("🌐 Select Language", ["English", "Telugu", "Hindi"])
tr = TRANSLATIONS["app"][lang]

# Add model selection in sidebar
with st.sidebar:
    st.session_state.model_choice = st.selectbox(
        "🤖 Select Model",
        ["ViT", "Swin"],
        index=0 if st.session_state.model_choice == "ViT" else 1,
        help="Choose between Vision Transformer (ViT) or Swin Transformer model"
    )
    
    # Add logout button if logged in
    if st.session_state.logged_in:
        if st.button("Logout"):
            logout()

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

@st.cache_resource
def download_models():
    """Download models if they don't exist"""
    def download_if_not_exists(file_path, file_id):
        try:
            # Ensure absolute path
            file_path = os.path.abspath(file_path)
            logger.info(f"Checking model at path: {file_path}")
            
            if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                logger.info(f"Downloading model to {file_path}")
                
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                # Use gdown with direct file ID
                url = f"https://drive.google.com/uc?id={file_id}"
                output = gdown.download(url, file_path, quiet=False)
                
                if output is None:
                    raise Exception(f"Failed to download model from {url}")
                
                # Verify file was downloaded and is not empty
                if not os.path.exists(file_path):
                    raise Exception(f"Model file not found at {file_path} after download")
                if os.path.getsize(file_path) == 0:
                    raise Exception(f"Downloaded model file is empty: {file_path}")
                    
                logger.info(f"Model downloaded successfully to {file_path} (size: {os.path.getsize(file_path)} bytes)")
            else:
                file_size = os.path.getsize(file_path)
                logger.info(f"Model already exists at {file_path} (size: {file_size} bytes)")
                
                # Verify file is not empty
                if file_size == 0:
                    logger.warning(f"Existing model file is empty, re-downloading: {file_path}")
                    os.remove(file_path)
                    return download_if_not_exists(file_path, file_id)
            
            return file_path
            
        except Exception as e:
            error_msg = f"Error downloading model to {file_path}: {str(e)}"
            logger.error(error_msg)
            st.error(error_msg)
            raise Exception(error_msg)

    try:
        # Get absolute paths
        vit_path = os.path.abspath(VIT_MODEL_PATH)
        swin_path = os.path.abspath(SWIN_MODEL_PATH)
        shelf_life_path = os.path.abspath(SHELF_LIFE_MODEL_PATH)
        
        logger.info("Starting model downloads...")
        logger.info(f"ViT path: {vit_path}")
        logger.info(f"Swin path: {swin_path}")
        logger.info(f"Shelf life path: {shelf_life_path}")
        
        # Download models
        vit_path = download_if_not_exists(vit_path, VIT_MODEL_ID)
        swin_path = download_if_not_exists(swin_path, SWIN_MODEL_ID)
        shelf_life_path = download_if_not_exists(shelf_life_path, SHELF_LIFE_MODEL_ID)
        
        # Final verification
        for path in [vit_path, swin_path, shelf_life_path]:
            if not os.path.exists(path):
                raise Exception(f"Model file not found: {path}")
            if os.path.getsize(path) == 0:
                raise Exception(f"Model file is empty: {path}")
        
        logger.info("All models downloaded and verified successfully")
        return vit_path, swin_path, shelf_life_path
        
    except Exception as e:
        error_msg = f"Failed to download or verify models: {str(e)}"
        logger.error(error_msg)
        st.error(error_msg)
        raise Exception(error_msg)

# Download models at startup
try:
    vit_path, swin_path, shelf_life_path = download_models()
    logger.info("Models loaded successfully at startup")
except Exception as e:
    logger.error(f"Error loading models at startup: {str(e)}")
    st.error(f"Failed to load models at startup: {str(e)}")

def set_background(image_file):
    try:
        with open(image_file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: linear-gradient(135deg, rgba(15,23,42,0.95), rgba(12,74,110,0.95));
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        logger.warning(f"Background image not found: {image_file}")
        st.markdown(
            """
            <style>
            .stApp {
                background: linear-gradient(135deg, #1e3c72, #2a5298);
            }
            </style>
            """,
            unsafe_allow_html=True
        )

@st.cache_resource
def load_classifier():
    try:
        class ImageClassifier:
            def __init__(self):
                try:
                    # Initialize transform first
                    self.transform = transforms.Compose([
                        transforms.Resize((224, 224)),
                        transforms.ToTensor(),
                        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
                    ])

                    # ResNet for fruit detection
                    self.resnet_model = models.resnet50(weights="DEFAULT")
                    self.resnet_model.eval().to(device)
                    logger.info("ResNet50 loaded successfully")

                    # ViT for freshness classification
                    self.vit_model = ViT(
                        img_size=224,
                        in_channels=3,
                        patch_size=16,
                        embedding_dims=768,
                        num_transformer_layers=12,
                        mlp_dropout=0.1,
                        attn_dropout=0.0,
                        mlp_size=3072,
                        num_heads=12,
                        num_classes=2
                    )
                    try:
                        state_dict = torch.load(VIT_MODEL_PATH, map_location=device)
                        self.vit_model.load_state_dict(state_dict)
                        logger.info(f"ViT loaded successfully from {VIT_MODEL_PATH}")
                    except Exception as e:
                        st.error(f"❌ Error loading ViT model: {str(e)}")
                        logger.error(f"Error loading ViT model: {str(e)}")
                        return None
                    self.vit_model.eval().to(device)

                    # Swin for freshness classification
                    self.swin_model = SwinTransformer(
                        img_size=224,
                        patch_size=4,
                        in_chans=3,
                        embed_dim=96,
                        depths=[2, 2],
                        num_heads=[3, 6],
                        window_size=7,
                        num_classes=2
                    )
                    try:
                        state_dict = torch.load(SWIN_MODEL_PATH, map_location=device)
                        self.swin_model.load_state_dict(state_dict)
                        logger.info(f"Swin Transformer loaded successfully from {SWIN_MODEL_PATH}")
                    except Exception as e:
                        st.error(f"❌ Error loading Swin model: {str(e)}")
                        logger.error(f"Error loading Swin model: {str(e)}")
                        return None
                    self.swin_model.eval().to(device)

                    logger.info("ImageClassifier initialized successfully")
                except Exception as e:
                    st.error(f"Error initializing classifier: {str(e)}")
                    logger.error(f"Classifier init error: {str(e)}")
                    return None

            def detect_fruit_type(self, img):
                try:
                    if not imagenet_classes:
                        raise ValueError("ImageNet classes not loaded. Cannot perform fruit detection.")
                    
                    input_tensor = self.transform(img).unsqueeze(0).to(device)
                    outputs = self.resnet_model(input_tensor)
                    probs = F.softmax(outputs, dim=1)
                    
                    # Get top 5 predictions for better debugging
                    top_probs, top_indices = torch.topk(probs, k=5)
                    top_classes = [imagenet_classes[idx.item()].lower() for idx in top_indices[0]]
                    top_probabilities = [prob.item() * 100 for prob in top_probs[0]]
                    
                    # Check if any of the top 5 predictions contain fruit keywords
                    is_fruit = False
                    matched_keyword = None
                    for class_name in top_classes:
                        for keyword in fruit_keywords:
                            if keyword in class_name:
                                is_fruit = True
                                matched_keyword = keyword
                                break
                        if is_fruit:
                            break
                    
                    # Get the highest confidence prediction
                    confidence = top_probabilities[0]
                    predicted_class = top_classes[0]
                    
                    # Only log for debugging, don't display to user
                    logger.info(f"Fruit detection result: is_fruit={is_fruit}, matched_keyword={matched_keyword}, confidence={confidence:.2f}%")
                    
                    return is_fruit, predicted_class, confidence
                except ValueError as e:
                    st.error(f"Validation error in fruit detection")
                    logger.error(f"Validation error in detect_fruit_type: {str(e)}")
                    return False, "unknown", 0.0
                except Exception as e:
                    st.error(f"Error detecting fruit type")
                    logger.error(f"Error in detect_fruit_type: {str(e)}")
                    return False, "unknown", 0.0

            def classify_freshness(self, img):
                try:
                    input_tensor = self.transform(img).unsqueeze(0).to(device)
                    
                    # Use the selected model
                    if st.session_state.model_choice == "ViT":
                        if not hasattr(self, 'vit_model'):
                            raise ValueError("ViT model not properly initialized")
                        outputs = self.vit_model(input_tensor)
                        model_name = "ViT"
                    else:  # Swin
                        if not hasattr(self, 'swin_model'):
                            raise ValueError("Swin model not properly initialized")
                        outputs = self.swin_model(input_tensor)
                        model_name = "Swin"
                    
                    probs = F.softmax(outputs, dim=1)
                    confidence, pred_class = torch.max(probs, dim=1)
                    pred_class = pred_class.item()
                    confidence = confidence.item() * 100
                    
                    # Log the prediction
                    logger.info(f"Freshness classification ({model_name}): class={'FRESH' if pred_class == 0 else 'STALE'}, confidence={confidence:.2f}%")
                    
                    return pred_class, confidence
                except ValueError as e:
                    st.error(f"Model initialization error: {str(e)}")
                    logger.error(f"Model initialization error in classify_freshness: {str(e)}")
                    return 1, 0.0
                except Exception as e:
                    st.error(f"Error classifying freshness: {str(e)}")
                    logger.error(f"Error in classify_freshness: {str(e)}")
                    return 1, 0.0

            def predict_shelf_life(self, img):
                try:
                    # Load shelf life model on demand
                    if not hasattr(self, 'shelf_life_model'):
                        self.shelf_life_model = models.efficientnet_b0(weights="DEFAULT")
                        # Match the saved model's number of classes (40)
                        self.shelf_life_model.classifier[1] = nn.Linear(
                            self.shelf_life_model.classifier[1].in_features, 
                            40  # Changed from len(shelf_life_class_names) to match saved model
                        )
                        try:
                            state_dict = torch.load(SHELF_LIFE_MODEL_PATH, map_location=device)
                            self.shelf_life_model.load_state_dict(state_dict)
                            logger.info(f"EfficientNet-B0 loaded successfully from {SHELF_LIFE_MODEL_PATH}")
                        except Exception as e:
                            st.error(f"❌ Error loading shelf life model: {str(e)}")
                            logger.error(f"Error loading shelf life model: {str(e)}")
                            return "unknown", "unknown", "Shelf life data not available", 0.0
                        self.shelf_life_model.eval().to(device)
                    
                    image_tensor = self.transform(img).unsqueeze(0).to(device)
                    with torch.no_grad():
                        output = self.shelf_life_model(image_tensor)
                        probs = F.softmax(output, dim=1)
                        confidence, predicted_idx = torch.max(probs, 1)
                    
                    # Map the 40-class output to our 6 classes
                    # The saved model uses a more detailed classification scheme
                    # We'll map it to our simplified classes based on the highest probability group
                    predicted_idx = predicted_idx.item() % len(shelf_life_class_names)  # Map to our 6 classes
                    predicted_class = shelf_life_class_names[predicted_idx]
                    fruit, condition = predicted_class.split('_')
                    
                    if fruit not in shelf_life_data or condition not in shelf_life_data[fruit]:
                        raise ValueError(f"No shelf life data available for this condition")
                    
                    shelf_life = shelf_life_data[fruit][condition]
                    logger.info(f"Shelf life prediction: condition={condition}, shelf_life={shelf_life}, confidence={confidence.item():.4f}")
                    return fruit, condition, shelf_life, confidence.item() * 100
                except ValueError as e:
                    st.error(f"Validation error in shelf life prediction: {str(e)}")
                    logger.error(f"Validation error in predict_shelf_life: {str(e)}")
                    return "unknown", "unknown", "Shelf life data not available", 0.0
                except Exception as e:
                    st.error(f"Error predicting shelf life: {str(e)}")
                    logger.error(f"Error in predict_shelf_life: {str(e)}")
                    return "unknown", "unknown", "Shelf life data not available", 0.0

        return ImageClassifier()
    except Exception as e:
        st.error(f"Failed to initialize classifier: {str(e)}")
        logger.error(f"Error in load_classifier: {str(e)}")
        return None

def save_uploaded_image(image_file):
    try:
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            logger.info(f"Created upload directory: {UPLOAD_DIR}")
        unique_id = f"{int(time.time())}_{uuid.uuid4().hex[:8]}"
        file_ext = os.path.splitext(image_file.name)[1]
        unique_filename = f"{unique_id}{file_ext}"
        image_path = os.path.join(UPLOAD_DIR, unique_filename)
        with open(image_path, "wb") as f:
            f.write(image_file.getbuffer())
        absolute_path = os.path.abspath(image_path)
        logger.info(f"Image saved successfully: {absolute_path}")
        return absolute_path
    except Exception as e:
        st.error(f"Error saving image: {str(e)}")
        logger.error(f"Error saving image: {str(e)}")
        return None

def image_to_base64(image):
    """Convert PIL image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def main():
    # Main Content
    st.markdown("""
        <div class="glass-container">
            <div class="app-header">
                <h1>Fruit Freshness Detector</h1>
                <p>Upload an image of your fruit</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Create a container for the upload section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # File uploader with proper drag and drop support
        uploaded_file = st.file_uploader(
            "📸 Upload Image", 
            type=["jpg", "jpeg", "png"],
            help="Choose a clear, well-lit image of fruit for best results (Max 200MB)",
            label_visibility="visible"
        )

        if uploaded_file is not None:
            try:
                # Load and display the image
                image = Image.open(uploaded_file)
                
                # Display image and details in a glass container
                st.markdown("""
                    <div class="glass-container fade-in">
                        <div class="result-title">Upload Details</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Display file details
                st.markdown(f"""
                    <div class="result-container">
                        <div class="result-item">
                            <span>File Name: {uploaded_file.name}</span>
                        </div>
                        <div class="result-item">
                            <span>Format: {image.format}</span>
                        </div>
                        <div class="result-item">
                            <span>Size: {image.size}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # Display image in preview container with enhanced styling
                st.markdown(f"""
                    <div class="image-preview-container">
                        <img 
                            src="data:image/png;base64,{image_to_base64(image)}" 
                            class="image-preview w-[300px] md:w-[400px] rounded-xl shadow-md" 
                            alt="Uploaded Image"
                            style="width: 300px; max-width: 100%; height: auto; margin: 0 auto; display: block;"
                        >
                    </div>
                """, unsafe_allow_html=True)

                # Process the image
                with st.spinner('Processing image...'):
                    try:
                        # Get classifier instance
                        classifier = load_classifier()
                        if classifier is None:
                            st.error("Failed to initialize classifier. Please try again later.")
                            return

                        # Detect if image contains fruit
                        is_fruit, detected_fruit, _ = classifier.detect_fruit_type(image)
                        
                        if not is_fruit:
                            st.error("No fruit detected in the image. Please upload an image containing fruit.")
                            return

                        # Get freshness prediction
                        freshness_class, freshness_confidence = classifier.classify_freshness(image)
                        
                        # Get shelf life prediction immediately
                        fruit, condition, shelf_life, shelf_life_confidence = classifier.predict_shelf_life(image)
                        
                        # Save the image first
                        image_path = save_uploaded_image(uploaded_file)
                        if not image_path:
                            st.error("Failed to save uploaded image")
                            return
                        
                        # Display results
                        result = "FRESH" if freshness_class == 0 else "STALE"
                        
                        st.markdown(
                            f'''
                            <div class="result-container fade-in">
                                <div class="result-title">Analysis Results</div>
                                <div class="result-item">
                                    <span>Freshness Score: {freshness_confidence:.2f}%</span>
                                </div>
                                <div class="result-item">
                                    <span>Fruit Type: {fruit.title()}</span>
                                </div>
                                <div class="result-item">
                                    <span>Condition: {condition.title()}</span>
                                </div>
                                <div class="result-item">
                                    <span>Storage Recommendation: {shelf_life}</span>
                                </div>
                                <div class="result-item">
                                    <span>Estimated Shelf Life: {result}</span>
                                </div>
                            </div>
                            ''',
                            unsafe_allow_html=True
                        )

                        # Save complete prediction to database immediately
                        save_prediction(
                            user_email=st.session_state["email"],
                            result=result,
                            confidence=freshness_confidence,
                            fruit_type=fruit,
                            image_path=image_path,
                            shelf_life_condition=condition,
                            shelf_life_estimate=shelf_life,
                            shelf_life_confidence=shelf_life_confidence,
                            model_type=st.session_state.model_choice
                        )

                    except Exception as e:
                        st.error(f"An error occurred during analysis: {str(e)}")
                        logger.error(f"Error during image analysis: {str(e)}")
            except Exception as e:
                st.markdown(f"""
                    <div class="result-container fade-in">
                        <div class="result-item">
                            <span>Error processing image: {str(e)}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()