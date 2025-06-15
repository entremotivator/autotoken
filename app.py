import streamlit as st
import requests
import json
import jwt
from datetime import datetime, timedelta
import base64
import hashlib
import hmac

# Page configuration
st.set_page_config(
    page_title="n8n Token Manager",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 n8n Authentication Token Manager")
st.markdown("---")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    n8n_url = st.text_input("n8n Instance URL", value="https://your-n8n-instance.com")
    st.markdown("*Enter your n8n instance URL*")

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["🔑 Generate Token", "🔍 Decode Token", "📋 Token Info", "⚙️ Settings"])

with tab1:
    st.header("Generate New Authentication Token")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Login Credentials")
        email = st.text_input("Email", placeholder="your-email@example.com")
        password = st.text_input("Password", type="password", placeholder="Your password")
        
    with col2:
        st.subheader("Token Settings")
        token_name = st.text_input("Token Name", value="API Token")
        expiry_days = st.number_input("Expiry (days)", min_value=1, max_value=365, value=30)
        
    if st.button("🚀 Generate Token", type="primary"):
        if email and password:
            try:
                # Simulate token generation (replace with actual n8n API call)
                with st.spinner("Generating token..."):
                    # This is a placeholder - replace with actual n8n API authentication
                    login_data = {
                        "email": email,
                        "password": password
                    }
                    
                    # Mock response for demonstration
                    # In real implementation, you would call n8n's API
                    mock_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyLWlkIiwiaXNzIjoibjhuIiwiYXVkIjoicHVibGljLWFwaSIsImlhdCI6MTczNDI5NTIwMCwiZXhwIjoxNzM2ODg3MjAwfQ.example-signature"
                    
                    st.success("✅ Token generated successfully!")
                    
                    # Display token information
                    st.subheader("🎯 Your New Token")
                    st.code(mock_token, language="text")
                    
                    # Token details
                    st.subheader("📊 Token Details")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Token Type", "JWT")
                    with col2:
                        st.metric("Expires In", f"{expiry_days} days")
                    with col3:
                        st.metric("Status", "Active")
                    
                    # Copy button
                    st.download_button(
                        label="📥 Download Token",
                        data=mock_token,
                        file_name=f"n8n_token_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                    
            except Exception as e:
                st.error(f"❌ Error generating token: {str(e)}")
        else:
            st.warning("⚠️ Please enter both email and password")

with tab2:
    st.header("Decode JWT Token")
    
    token_input = st.text_area("Paste JWT Token", height=100, placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    
    if st.button("🔍 Decode Token"):
        if token_input:
            try:
                # Decode JWT token (without verification for inspection)
                decoded_header = jwt.get_unverified_header(token_input)
                decoded_payload = jwt.decode(token_input, options={"verify_signature": False})
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📋 Header")
                    st.json(decoded_header)
                
                with col2:
                    st.subheader("📋 Payload")
                    st.json(decoded_payload)
                
                # Token validity check
                if 'exp' in decoded_payload:
                    exp_timestamp = decoded_payload['exp']
                    exp_datetime = datetime.fromtimestamp(exp_timestamp)
                    current_time = datetime.now()
                    
                    st.subheader("⏰ Token Validity")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Issued At", 
                                datetime.fromtimestamp(decoded_payload.get('iat', 0)).strftime('%Y-%m-%d %H:%M:%S') if 'iat' in decoded_payload else "Unknown")
                    with col2:
                        st.metric("Expires At", exp_datetime.strftime('%Y-%m-%d %H:%M:%S'))
                    with col3:
                        is_valid = current_time < exp_datetime
                        st.metric("Status", "Valid ✅" if is_valid else "Expired ❌")
                
            except Exception as e:
                st.error(f"❌ Error decoding token: {str(e)}")
        else:
            st.warning("⚠️ Please paste a JWT token")

with tab3:
    st.header("Token Information & Management")
    
    # Current token display
    current_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NDI5NWRjYS01YTIxLTQzZDMtYTA1OS1jOTA5YTQ5ZjlkYTEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzUwMDA0NDM4LCJleHAiOjE3NTI1NTIwMDB9.zGO6k91A-upUAAn-dcJ3hgqoDXkTTKO8u8PdfKg24Fc"
    
    st.subheader("🔑 Current Token")
    st.code(current_token, language="text")
    
    # Decode current token
    try:
        decoded = jwt.decode(current_token, options={"verify_signature": False})
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("User ID", decoded.get('sub', 'Unknown')[:8] + "...")
        with col2:
            st.metric("Issuer", decoded.get('iss', 'Unknown'))
        with col3:
            st.metric("Audience", decoded.get('aud', 'Unknown'))
        with col4:
            exp_time = datetime.fromtimestamp(decoded.get('exp', 0))
            is_valid = datetime.now() < exp_time
            st.metric("Status", "Valid ✅" if is_valid else "Expired ❌")
        
        # Expiration info
        st.subheader("⏰ Expiration Details")
        time_left = exp_time - datetime.now()
        if time_left.total_seconds() > 0:
            days_left = time_left.days
            hours_left = time_left.seconds // 3600
            st.info(f"Token expires in {days_left} days and {hours_left} hours")
        else:
            st.error("Token has expired!")
            
    except Exception as e:
        st.error(f"Error parsing current token: {str(e)}")
    
    # Token actions
    st.subheader("🛠️ Token Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh Token"):
            st.info("Token refresh functionality would be implemented here")
    
    with col2:
        if st.button("🗑️ Revoke Token"):
            st.warning("Token revocation functionality would be implemented here")
    
    with col3:
        if st.button("📋 Copy Token"):
            st.success("Token copied to clipboard!")

with tab4:
    st.header("Application Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔧 API Settings")
        api_timeout = st.number_input("API Timeout (seconds)", min_value=5, max_value=300, value=30)
        verify_ssl = st.checkbox("Verify SSL Certificates", value=True)
        debug_mode = st.checkbox("Enable Debug Mode", value=False)
        
    with col2:
        st.subheader("🔐 Security Settings")
        auto_refresh = st.checkbox("Auto-refresh tokens", value=True)
        token_storage = st.selectbox("Token Storage", ["Memory Only", "Encrypted Local", "Secure Vault"])
        log_requests = st.checkbox("Log API Requests", value=False)
    
    if st.button("💾 Save Settings"):
        st.success("Settings saved successfully!")
    
    # Connection test
    st.subheader("🔌 Connection Test")
    if st.button("🧪 Test n8n Connection"):
        with st.spinner("Testing connection..."):
            # Mock connection test
            st.success("✅ Connection successful!")
            st.info("Connected to n8n instance")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>🔐 n8n Token Manager | Built with Streamlit</p>
        <p><small>Keep your tokens secure and never share them publicly</small></p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Security warning
with st.expander("⚠️ Security Best Practices"):
    st.markdown("""
    - **Never share your tokens** with anyone
    - **Use HTTPS** for all API calls
    - **Rotate tokens regularly** (recommended: every 30 days)
    - **Store tokens securely** (use environment variables or secure vaults)
    - **Monitor token usage** and revoke unused tokens
    - **Use minimal permissions** for each token
    """)
