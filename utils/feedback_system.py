import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
from datetime import datetime
import json

def send_feedback_email(rating, feedback_text, user_email=""):
    """Send feedback email to the specified address"""

    try:
        # Email configuration - you'll need to set these up in Streamlit secrets
        smtp_server = st.secrets.get("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = st.secrets.get("SMTP_PORT", 587)
        sender_email = st.secrets.get("SENDER_EMAIL", "")
        sender_password = st.secrets.get("SENDER_PASSWORD", "")
        recipient_email = "darshan.t.mn@gmail.com"

        if not sender_email or not sender_password:
            return False, "Email configuration not found in secrets"

        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Resume Optimizer Feedback - {rating} Stars"

        # Email body
        body = f"""
New feedback received for Resume Optimizer:

Rating: {rating}/5 stars
User Email: {user_email if user_email else "Not provided"}
Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Feedback:
{feedback_text}

---
This is an automated message from the Resume Optimizer application.
        """

        msg.attach(MIMEText(body, 'plain'))

        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()

        return True, "Feedback sent successfully!"

    except Exception as e:
        return False, f"Error sending feedback: {str(e)}"

def show_feedback_popup():
    """Display feedback popup using Streamlit components"""

    if 'show_feedback' not in st.session_state:
        st.session_state.show_feedback = False

    if st.session_state.show_feedback:
        with st.container():
            st.markdown("---")
            st.markdown("### 📝 We'd love your feedback!")

            col1, col2 = st.columns([3, 1])

            with col1:
                # Star rating
                rating = st.select_slider(
                    "How would you rate your experience?",
                    options=[1, 2, 3, 4, 5],
                    value=5,
                    format_func=lambda x: "⭐" * x
                )

                # Feedback text
                feedback_text = st.text_area(
                    "Tell us more about your experience (optional):",
                    placeholder="What did you like? What could be improved?",
                    height=100
                )

                # User email (optional)
                user_email = st.text_input(
                    "Your email (optional - for follow-up):",
                    placeholder="your.email@example.com"
                )

                # Buttons
                col_submit, col_skip = st.columns(2)

                with col_submit:
                    if st.button("Submit Feedback", type="primary"):
                        success, message = send_feedback_email(rating, feedback_text, user_email)
                        if success:
                            st.success("Thank you for your feedback! 🙏")
                            st.session_state.show_feedback = False
                            st.rerun()
                        else:
                            st.error(f"Failed to send feedback: {message}")

                with col_skip:
                    if st.button("Skip"):
                        st.session_state.show_feedback = False
                        st.rerun()

            with col2:
                st.markdown("### 🎯")
                st.markdown("Your feedback helps us improve!")

def trigger_feedback_popup():
    """Trigger the feedback popup to show"""
    st.session_state.show_feedback = True

def save_feedback_locally(rating, feedback_text, user_email=""):
    """Save feedback locally as backup"""

    try:
        feedback_data = {
            "timestamp": datetime.now().isoformat(),
            "rating": rating,
            "feedback": feedback_text,
            "user_email": user_email
        }

        # Try to load existing feedback
        try:
            with open("feedback_log.json", "r") as f:
                feedback_log = json.load(f)
        except FileNotFoundError:
            feedback_log = []

        # Add new feedback
        feedback_log.append(feedback_data)

        # Save updated feedback
        with open("feedback_log.json", "w") as f:
            json.dump(feedback_log, f, indent=2)

        return True

    except Exception as e:
        st.error(f"Error saving feedback locally: {str(e)}")
        return False
