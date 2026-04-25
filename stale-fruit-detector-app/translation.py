# translation.py
# Centralized translations for all pages in the Stale Fruit Detection application

TRANSLATIONS = {
    "main": {
        "English": {
            "title": "Stale Fruit Detector",
            "desc1": "Welcome to the Stale Fruit Detector App! This application uses advanced machine learning models to analyze images of fruits and determine their freshness level.",
            "desc2": "Our goal is to help you reduce food waste by accurately identifying stale fruits, allowing you to make informed decisions about consumption and storage.",
            "scan_line": "Navigate to the 'Upload' page in the sidebar to get started with scanning your fruit images.",
            "footer": "© 2023 Stale Fruit Detector App. All rights reserved.",
            "desc3": "The app currently supports detection and freshness classification for a variety of fruits including apples, bananas, grapes, mangoes, oranges, peaches, pears, pineapples, strawberries, and watermelons.",
            "desc4": "In addition to classifying freshness as 'Fresh' or 'Stale', the app also provides a detailed shelf life prediction based on the fruit's condition.",
            "desc5": "Our models, including a fine-tuned ResNet50 for fruit detection and Vision Transformer (ViT) or Swin Transformer for freshness, are continuously improved for accuracy."
        },
        "Telugu": {
            "title": "పండ్ల తాజా గుర్తింపు వ్యవస్థ",
            "desc1": "CNN మరియు Swin Transformers ఆధారంగా పనిచేసే AI సాధనం – పండ్ల తాజా తక్షణ గుర్తింపు కోసం.",
            "desc2": "🚀 పండ్ల నాణ్యత తనిఖీలను AIతో విప్లవాత్మకం చేయండి!<br>"
                     "మా బుద్ధిమంతమైన వ్యవస్థ CNN మరియు Swin Transformers ను కలిపి, పండ్ల చిత్రాలను స్కాన్ చేసి వెంటనే తాజాదనాన్ని గుర్తిస్తుంది.<br>"
                     "ఇక అభిప్రాయం కాదు—చిత్రాన్ని అప్‌లోడ్ చేయండి, విశ్లేషించండి, మరియు నమ్మకంగా నిర్ణయం తీసుకోండి.<br>"
                     "స్మార్ట్ కిచెన్లు, స్టోర్లు మరియు పర్యావరణాన్ని ప్రేమించే వినియోగదారుల కోసం రూపొందించబడింది.",
            "scan_line": "🍌🍓🍊 స్కాన్ చేసేందుకు సిద్ధంగా ఉంది... 🍍🍇🍎",
            "footer": "🧠 AI, ❤️ Streamlit, మరియు ☁️ MongoDB తో అభివృద్ధి చేయబడింది"
        },
        "Hindi": {
            "title": "फल की ताज़गी पहचान प्रणाली",
            "desc1": "CNN और Swin Transformers का उपयोग करने वाला AI-संचालित उपकरण – फल की ताज़गी को तुरंत पहचानें।",
            "desc2": "🚀 AI के साथ फल गुणवत्ता जांच में क्रांति लाएं!<br>"
                     "हमारी स्मार्ट प्रणाली CNN और Swin Transformers को मिलाकर फल की छवियों को स्कैन करती है और ताज़गी का तुरंत पता लगाती है.<br>"
                     "अब कोई अनुमान नहीं—बस अपलोड करें, विश्लेषण करें और आत्मविश्वास के साथ निर्णय लें।<br>"
                     "स्मार्ट रसोई, स्टोर्स और पर्यावरण-जागरूक उपयोगकर्ताओं के लिए बनाया गया।",
            "scan_line": "🍌🍓🍊 स्कैन के लिए तैयार... 🍍🍇🍎",
            "footer": "🧠 AI, ❤️ Streamlit, और ☁️ MongoDB के साथ विकसित किया गया"
        }
    },
    "about": {
        "English": {
            "title": "🍏 About the System",
            "desc": """
                Welcome to the Stale Fruit Detection System, an AI-powered web application that uses a hybrid model combining CNN and Swin Transformers to predict the freshness of fruits from images.
            """,
            "features": """
                - 📸 Upload fruit images for classification
                - 🧠 Deep learning model for high accuracy
                - 🗃️ Tracks predictions in MongoDB and CSV
                - 🔐 Secure login and registration system
            """,
            "footer": "Developed by your team using Streamlit, PyTorch, and MongoDB ☁️"
        },
        "Telugu": {
            "title": "🍏 వ్యవస్థ గురించి",
            "desc": """
                స్వాగతం Stale Fruit Detection System లో, ఇది AI ఆధారిత వెబ్ యాప్ గా పనిచేస్తుంది, ఇది CNN మరియు Swin Transformers ను కలిపి ఫలాల తాజాదనాన్ని అంచనా వేయడానికి.
            """,
            "features": """
                - 📸 ఫలాల చిత్రాలను అప్‌లోడ్ చేయండి వర్గీకరణ కోసం
                - 🧠 డీప్ లెర్నింగ్ మోడల్ కోసం ఉన్నత స్థాయి ఖచ్చితత్వం
                - 🗃️ MongoDB మరియు CSV లో అంచనాలను ట్రాక్ చేస్తుంది
                - 🔐 భద్రత గల లాగిన్ మరియు నమోదు వ్యవస్థ
            """,
            "footer": "మీ బృందం Streamlit, PyTorch, మరియు MongoDB ☁️ ఉపయోగించి అభివృద్ధి చేసింది"
        },
        "Hindi": {
            "title": "🍏 प्रणाली के बारे में",
            "desc": """
                Stale Fruit Detection System में आपका स्वागत है, यह एक AI-समर्थित वेब ऐप है जो CNN और Swin Transformers के संयोजन का उपयोग करके फलों की ताजगी का अनुमान लगाता है।
            """,
            "features": """
                - 📸 फलों की छवियाँ अपलोड करें वर्गीकरण के लिए
                - 🧠 गहरे अध्ययन मॉडल के लिए उच्च सटीकता
                - 🗃️ MongoDB और CSV में भविष्यवाणियों का ट्रैक करता है
                - 🔐 सुरक्षित लॉगिन और पंजीकरण प्रणाली
            """,
            "footer": "आपकी टीम द्वारा Streamlit, PyTorch, और MongoDB ☁️ के साथ विकसित किया गया"
        }
    },
    "login": {
        "English": {
            "title": "Login",
            "email_placeholder": "Enter your email",
            "password_placeholder": "Enter your password",
            "login_button": "Login",
            "sign_up_button": "Don't have an account? Sign up",
            "welcome": "Welcome",
            "incorrect_password": "Incorrect email or password",
            "google_login": "Or login with Google",
            "google_warning": "Google login is not available yet",
            "google_info": "This feature will be available soon"
        },
        "Telugu": {
            "title": "లాగిన్",
            "email_placeholder": "మీ ఇమెయిల్‌ని నమోదు చేయండి",
            "password_placeholder": "మీ పాస్‌వర్డ్‌ని నమోదు చేయండి",
            "login_button": "లాగిన్",
            "sign_up_button": "ఖాతా లేదా? సైన్ అప్ చేయండి",
            "welcome": "స్వాగతం",
            "incorrect_password": "తప్పు ఇమెయిల్ లేదా పాస్‌వర్డ్",
            "google_login": "లేదా Google తో లాగిన్ చేయండి",
            "google_warning": "Google లాగిన్ ఇంకా అందుబాటులో లేదు",
            "google_info": "ఈ ఫీచర్ త్వరలో అందుబాటులో ఉంటుంది"
        },
        "Hindi": {
            "title": "लॉगिन",
            "email_placeholder": "अपना ईमेल दर्ज करें",
            "password_placeholder": "अपना पासवर्ड दर्ज करें",
            "login_button": "लॉगिन",
            "sign_up_button": "खाता नहीं है? साइन अप करें",
            "welcome": "स्वागत है",
            "incorrect_password": "गलत ईमेल या पासवर्ड",
            "google_login": "या Google से लॉगिन करें",
            "google_warning": "Google लॉगिन अभी उपलब्ध नहीं है",
            "google_info": "यह सुविधा जल्द ही उपलब्ध होगी"
        }
    },
    "signup": {
        "Sign Up": {
            "en": "Sign Up",
            "te": "సైన్ అప్",
            "hi": "साइन अप करें"
        },
        "Full Name": {
            "en": "Full Name",
            "te": "పూర్తి పేరు",
            "hi": "पूरा नाम"
        },
        "Email": {
            "en": "Email",
            "te": "ఇమెయిల్",
            "hi": "ईमेल"
        },
        "Password": {
            "en": "Password",
            "te": "పాస్‌వర్డ్",
            "hi": "पासवर्ड"
        },
        "Confirm Password": {
            "en": "Confirm Password",
            "te": "పాస్‌వర్డ్‌ని నిర్ధారించండి",
            "hi": "पासवर्ड की पुष्टि करें"
        },
        "Create a new account below:": {
            "en": "Create a new account below:",
            "te": "క్రింద కొత్త ఖాతా సృష్టించండి:",
            "hi": "नीचे एक नया खाता बनाएं:"
        },
        "Please fill in all fields.": {
            "en": "Please fill in all fields.",
            "te": "దయచేసి అన్ని ఫీల్డ్‌లను పూరించండి.",
            "hi": "कृपया सभी फ़ील्ड भरें।"
        },
        "Passwords do not match.": {
            "en": "Passwords do not match.",
            "te": "పాస్వర్డ్లు సరిపోలడం లేదు.",
            "hi": "पासवर्ड मेल नहीं खाते।"
        },
        "An account with this email already exists.": {
            "en": "An account with this email already exists.",
            "te": "ఈ ఇమెయిల్‌తో ఖాతా ఇప్పటికే ఉంది.",
            "hi": "इस ईमेल के साथ एक खाता पहले से मौजूद है।"
        },
        "Account created successfully! You can now log in.": {
            "en": "Account created successfully! You can now log in.",
            "te": "ఖాతా విజయవంతంగా సృష్టించబడింది! ఇప్పుడు మీరు లాగిన్ చేయవచ్చు.",
            "hi": "खाता सफलतापूर्वक बनाया गया! अब आप लॉग इन कर सकते हैं।"
        },
        "Go to the Login page to access your account.": {
            "en": "Go to the Login page to access your account.",
            "te": "మీ ఖాతాను యాక్సెస్ చేయడానికి లాగిన్ పేజీకి వెళ్లండి.",
            "hi": "अपने खाते तक पहुंचने के लिए लॉगिन पृष्ठ पर जाएं।"
        },
        "Signup failed. Please try again.": {
            "en": "Signup failed. Please try again.",
            "te": "సైన్ అప్ విఫలమైంది. దయచేసి మళ్లీ ప్రయత్నించండి.",
            "hi": "साइनअप विफल रहा। कृपया पुनः प्रयास करें।"
        }
    },
    "app": {
        "English": {
            "title": "Fruit Freshness Detector",
            "upload_text": "Upload an image of your fruit",
            "analyzing": "Analyzing image...",
            "result_fresh": "FRESH",
            "result_stale": "STALE",
            "confidence": "Confidence",
            "fruit_type": "Fruit Type",
            "condition": "Condition",
            "shelf_life": "Estimated Shelf Life",
            "tips_title": "Tips for Best Results",
            "tip_1": "Ensure your fruit is well-lit",
            "tip_2": "Take a clear, focused image",
            "tip_3": "Get close enough to show details"
        },
        "Telugu": {
            "title": "పండ్ల తాజాదనం డిటెక్టర్",
            "upload_text": "మీ పండు చిత్రాన్ని అప్‌లోడ్ చేయండి",
            "analyzing": "చిత్రాన్ని విశ్లేషిస్తోంది...",
            "result_fresh": "తాజా",
            "result_stale": "పాత",
            "confidence": "నమ్మకం",
            "fruit_type": "పండు రకం",
            "condition": "స్థితి",
            "shelf_life": "అంచనా నిల్వ కాలం",
            "tips_title": "ఉత్తమ ఫలితాల కోసం చిట్కాలు",
            "tip_1": "మీ పండు బాగా వెలుగుతో ఉందని నిర్ధారించుకోండి",
            "tip_2": "స్పష్టమైన, ఫోకస్ చేసిన చిత్రాన్ని తీసుకోండి",
            "tip_3": "వివరాలు చూపించడానికి దగ్గరగా రండి"
        },
        "Hindi": {
            "title": "फल ताजगी डिटेक्टर",
            "upload_text": "अपने फल की छवि अपलोड करें",
            "analyzing": "छवि का विश्लेषण किया जा रहा है...",
            "result_fresh": "ताजा",
            "result_stale": "बासी",
            "confidence": "विश्वास",
            "fruit_type": "फल का प्रकार",
            "condition": "स्थिति",
            "shelf_life": "अनुमानित शेल्फ लाइफ",
            "tips_title": "सर्वोत्तम परिणामों के लिए सुझाव",
            "tip_1": "सुनिश्चित करें कि आपका फल अच्छी तरह से प्रकाशित है",
            "tip_2": "एक स्पष्ट, फोकस की गई छवि लें",
            "tip_3": "विवरण दिखाने के लिए पर्याप्त पास आएं"
        }
    },
    "history": {
        "English": {
            "title": "Prediction History",
            "login_required": "Please log in to view your prediction history.",
            "go_to_login": "Go to Login",
            "no_predictions": "No predictions found.",
            "timestamp": "Timestamp",
            "result": "Result",
            "confidence": "Confidence",
            "fruit_type": "Fruit Type",
            "shelf_life": "Shelf Life",
            "storage_conditions": "Storage Conditions"
        },
        "Telugu": {
            "title": "అంచనా చరిత్ర",
            "login_required": "మీ అంచనా చరిత్రను చూడటానికి దయచేసి లాగిన్ చేయండి.",
            "go_to_login": "లాగిన్‌కి వెళ్ళండి",
            "no_predictions": "అంచనాలు కనుగొనబడలేదు.",
            "timestamp": "సమయముద్ర",
            "result": "ఫలితం",
            "confidence": "నమ్మకం",
            "fruit_type": "పండు రకం",
            "shelf_life": "నిల్వ జీవితం",
            "storage_conditions": "నిల్వ పరిస్థితులు"
        },
        "Hindi": {
            "title": "पूर्वानुमान इतिहास",
            "login_required": "कृपया अपना पूर्वानुमान इतिहास देखने के लिए लॉगिन करें।",
            "go_to_login": "लॉगिन पर जाएं",
            "no_predictions": "कोई पूर्वानुमान नहीं मिला।",
            "timestamp": "समय मुद्रा",
            "result": "परिणाम",
            "confidence": "विश्वास",
            "fruit_type": "फल का प्रकार",
            "shelf_life": "शेल्फ लाइफ",
            "storage_conditions": "भंडारण की स्थिति"
        }
    }
}