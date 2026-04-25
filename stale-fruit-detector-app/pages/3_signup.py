import streamlit as st
from utils.db_utils import db
from utils.auth_utils import check_auth
from translation import TRANSLATIONS
from utils.style import apply_style
import re

# Set page config - MUST be first Streamlit command
st.set_page_config(page_title="Sign Up - Stale Fruit Detector", layout="wide")

# Apply shared styles
apply_style()

# Apply custom background color and import fonts
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&family=Inter:wght@400;500&display=swap');
    
    .stApp {
        background-color: #FFF0F5;
    }

    /* Modern Container Styling */
    .signup-container {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        padding: 2rem;
        margin: 1.5rem auto;
        max-width: 400px;
    }

    /* Heading Styles */
    .signup-header {
        text-align: center;
        margin-bottom: 1.5rem;
    }

    .signup-header h1 {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: #333;
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }

    .signup-header p {
        font-family: 'Inter', sans-serif;
        color: #666;
        font-size: 0.9rem;
    }

    /* Form Field Styling */
    .stTextInput > label {
        color: #2C3E50 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }

    /* Input Styling */
    .stTextInput > div > div > input {
        font-family: 'Inter', sans-serif !important;
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        border-radius: 10px !important;
        padding: 0.8rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        color: #2C3E50 !important;
        font-weight: 500 !important;
        caret-color: #2C3E50 !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #F34949 !important;
        box-shadow: 0 0 15px rgba(243, 73, 73, 0.15) !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #95A5A6 !important;
        opacity: 0.8 !important;
    }

    /* Hide Streamlit's default form messages */
    .stMarkdown div[data-testid="stMarkdownContainer"] > p,
    div[data-baseweb="base-input"] + div small {
        display: none !important;
    }

    /* Button Styling */
    .stButton > button {
        font-family: 'Poppins', sans-serif !important;
        background: #F34949 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.8rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        transform: scale(1) !important;
        width: 100% !important;
        margin-bottom: 0.5rem !important;
    }

    .stButton > button:hover {
        background: #E43D3D !important;
        transform: scale(1.02) !important;
        box-shadow: 0 5px 15px rgba(243, 73, 73, 0.2) !important;
    }

    /* Alternative Action Text */
    .alt-action {
        text-align: center;
        margin: 0.5rem 0;
        font-family: 'Inter', sans-serif;
        color: #666;
        font-size: 0.9rem;
    }

    /* Login Button */
    .login-button > button {
        background: #6C63FF !important;
    }

    .login-button > button:hover {
        background: #5B52E0 !important;
        box-shadow: 0 5px 15px rgba(108, 99, 255, 0.2) !important;
    }

    /* Alert Styling */
    .stAlert {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
    }

    /* Error Message Styling */
    .element-container div[data-testid="stMarkdownContainer"] div.stAlert {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        color: #E74C3C !important;
    }

    .stAlert > div[role="alert"] {
        color: #E74C3C !important;
        font-weight: 500 !important;
    }

    /* Password Guidelines */
    .password-guidelines {
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        color: #2C3E50;
        margin: 0.5rem 0 1rem 0;
        line-height: 1.4;
        padding: 0.75rem;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 8px;
        border: 1px solid rgba(107, 114, 128, 0.1);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .password-guidelines .check-icon {
        color: #10B981;
        font-size: 1rem;
        flex-shrink: 0;
    }

    /* Error Box Styling */
    .error-box {
        background-color: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.2);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        font-family: 'Inter', sans-serif;
    }

    .error-box ul {
        margin: 0;
        padding-left: 1.5rem;
        list-style-type: none;
    }

    .error-box li {
        color: #EF4444;
        font-size: 0.875rem;
        line-height: 1.5;
        margin: 0.25rem 0;
        position: relative;
    }

    .error-box li::before {
        content: "•";
        position: absolute;
        left: -1rem;
        color: #EF4444;
    }

    /* Password Validation Items */
    .validation-container {
        margin-top: 0.5rem;
        padding: 0.75rem;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
    }

    .validation-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.875rem;
        color: #6B7280;
        margin: 0.25rem 0;
        transition: color 0.3s ease;
    }

    .validation-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 18px;
        height: 18px;
        transition: all 0.3s ease;
    }

    .validation-icon.valid {
        color: #10B981;
    }

    .validation-icon.invalid {
        color: #EF4444;
    }

    /* Password Strength Meter */
    .strength-meter {
        margin-top: 1rem;
        padding: 0.75rem;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 8px;
    }

    .strength-text {
        font-size: 0.875rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .strength-bar {
        height: 4px;
        background: #E5E7EB;
        border-radius: 2px;
        overflow: hidden;
    }

    .strength-fill {
        height: 100%;
        width: 0;
        transition: all 0.3s ease;
    }

    /* Strength levels */
    .strength-weak .strength-text {
        color: #EF4444;
    }
    .strength-weak .strength-fill {
        width: 33.33%;
        background: #EF4444;
    }

    .strength-moderate .strength-text {
        color: #F59E0B;
    }
    .strength-moderate .strength-fill {
        width: 66.66%;
        background: #F59E0B;
    }

    .strength-strong .strength-text {
        color: #10B981;
    }
    .strength-strong .strength-fill {
        width: 100%;
        background: #10B981;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Hide Streamlit's default form submit text */
    .stMarkdown div[data-testid="stMarkdownContainer"] > p {
        display: none;
    }

    /* Form Container */
    </style>

    <script>
    function updatePasswordValidation(password) {
        const rules = {
            length: password.length >= 8,
            uppercase: /[A-Z]/.test(password),
            number: /[0-9]/.test(password),
            special: /[@#$!%?*]/.test(password),
            noSpace: !/\\s/.test(password)
        };

        // Update validation icons
        Object.entries(rules).forEach(([rule, isValid]) => {
            const item = document.querySelector(`#validation-${rule}`);
            if (item) {
                const icon = item.querySelector('.validation-icon');
                icon.className = `validation-icon ${isValid ? 'valid' : 'invalid'}`;
                icon.textContent = isValid ? '✅' : '❌';
            }
        });

        // Calculate strength
        const strength = Object.values(rules).filter(Boolean).length;
        const strengthMeter = document.querySelector('.strength-meter');
        let strengthClass = '';
        let strengthText = '';

        if (strength <= 2) {
            strengthClass = 'strength-weak';
            strengthText = 'Weak';
        } else if (strength <= 3) {
            strengthClass = 'strength-moderate';
            strengthText = 'Moderate';
        } else {
            strengthClass = 'strength-strong';
            strengthText = 'Strong';
        }

        strengthMeter.className = `strength-meter ${strengthClass}`;
        document.querySelector('.strength-text').textContent = `Password Strength: ${strengthText}`;
    }

    // Add event listener to password input
    document.addEventListener('DOMContentLoaded', function() {
        const passwordInput = document.querySelector('input[type="password"]');
        if (passwordInput) {
            passwordInput.addEventListener('input', function() {
                updatePasswordValidation(this.value);
            });
        }
    });
    </script>
""", unsafe_allow_html=True)

def is_valid_email(email):
    """Check if email is valid Gmail address with proper username format."""
    # Pattern for Gmail addresses with proper username format
    pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    
    if not re.match(pattern, email):
        return False
    
    # Additional checks for username part
    username = email.split('@')[0]
    
    # Username must:
    # - Start with a letter
    # - Contain only letters, numbers, dots, or underscores
    # - Not have consecutive dots
    # - Be between 6 and 30 characters
    username_pattern = r'^[a-zA-Z][a-zA-Z0-9._]{4,28}[a-zA-Z0-9]$'
    if not re.match(username_pattern, username):
        return False
    
    # Check for consecutive dots
    if '..' in username:
        return False
    
    return True

def is_valid_password(password):
    """Validate password against all rules."""
    rules = {
        'length': len(password) >= 8,
        'uppercase': bool(re.search(r'[A-Z]', password)),
        'number': bool(re.search(r'[0-9]', password)),
        'special': bool(re.search(r'[@#$!%?*]', password)),
        'no_space': not bool(re.search(r'\s', password))
    }
    return rules

def get_password_errors(password_rules):
    """Get list of password validation errors."""
    errors = []
    if not password_rules['length']:
        errors.append("Password must be at least 8 characters long")
    if not password_rules['uppercase']:
        errors.append("Password must include at least one uppercase letter")
    if not password_rules['number']:
        errors.append("Password must include at least one number")
    if not password_rules['special']:
        errors.append("Password must include at least one special character (@#$!%?*)")
    if not password_rules['no_space']:
        errors.append("Password must not contain spaces")
    return errors

def main():
    # Create the signup container
    st.markdown("""
        <div class="signup-container">
            <div class="signup-header">
                <h1>Create Account</h1>
                <p>Join us to start detecting fruit freshness</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Center container
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("signup_form"):
            email = st.text_input(
                "Email:",
                placeholder="username@gmail.com",
                key="email_input"
            )
            
            password = st.text_input(
                "Password:",
                type="password",
                placeholder="Enter your password",
                key="password_input"
            )
            
            confirm_password = st.text_input(
                "Confirm Password:",
                type="password",
                placeholder="Re-enter your password",
                key="confirm_password_input"
            )

            # Password guidelines
            st.markdown("""
                <div class="password-guidelines">
                    <span class="check-icon">✅</span>
                    Password must be at least 8 characters long and include one uppercase letter, one number, and one special character (e.g., @, #, $). No spaces allowed.
                </div>
            """, unsafe_allow_html=True)
            
            submit = st.form_submit_button("Create Account", use_container_width=True)
            
            st.markdown(
                '''
                <div class="alt-action">
                    Already have an account?
                </div>
                ''',
                unsafe_allow_html=True
            )
            
            login = st.form_submit_button("Login", use_container_width=True)

            if submit:
                errors = []
                
                # Check for empty fields
                if not email or not password or not confirm_password:
                    errors.append("Please fill in all fields")
                else:
                    # Validate email
                    if not is_valid_email(email):
                        errors.append("Enter a Valid Email Address (e.g., username@gmail.com)")
                        if '@' not in email:
                            errors.append("Email must contain '@' symbol")
                        elif not email.endswith('@gmail.com'):
                            errors.append("Only Gmail addresses are allowed")
                        else:
                            username = email.split('@')[0]
                            if len(username) < 6:
                                errors.append("Username must be at least 6 characters long")
                            if not username[0].isalpha():
                                errors.append("Username must start with a letter")
                            if '..' in username:
                                errors.append("Username cannot contain consecutive dots")
                            if not re.match(r'^[a-zA-Z0-9._]+$', username):
                                errors.append("Username can only contain letters, numbers, dots, or underscores")
                    
                    # Validate password
                    password_rules = is_valid_password(password)
                    password_errors = get_password_errors(password_rules)
                    errors.extend(password_errors)
                    
                    # Check password match
                    if password != confirm_password:
                        errors.append("Passwords do not match")

                # Display all errors in a single box if there are any
                if errors:
                    st.markdown(
                        f"""
                        <div class="error-box">
                            <ul>
                                {"".join(f"<li>{error}</li>" for error in errors)}
                            </ul>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    # All validations passed, try to create account
                    try:
                        if db.add_user(email, password):
                            st.success("Account created successfully! Redirecting to login page...")
                            st.session_state.logged_in = False  # Ensure logged out state
                            st.session_state.email = None
                            st.switch_page("pages/2_login.py")
                        else:
                            st.markdown(
                                """
                                <div class="error-box">
                                    <ul>
                                        <li>An account with this email already exists</li>
                                    </ul>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                    except Exception as e:
                        st.markdown(
                            """
                            <div class="error-box">
                                <ul>
                                    <li>Signup failed. Please try again.</li>
                                    <li>If the problem persists, please contact support.</li>
                                </ul>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            if login:
                st.switch_page("pages/2_login.py")

if __name__ == "__main__":
    main()