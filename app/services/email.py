"""
이메일 서비스
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from loguru import logger

from app.config import settings


def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    text_content: Optional[str] = None
) -> bool:
    """
    이메일 발송
    
    Args:
        to_email: 수신자 이메일
        subject: 제목
        html_content: HTML 내용
        text_content: 텍스트 내용 (선택)
    
    Returns:
        성공 여부
    """
    if not settings.EMAIL_ENABLED:
        logger.warning("이메일 알림이 비활성화되어 있습니다")
        return False
    
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.error("SMTP 설정이 누락되었습니다")
        return False
    
    try:
        # 메시지 생성
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = settings.FROM_EMAIL or settings.SMTP_USER
        message["To"] = to_email
        
        # 텍스트 파트
        if text_content:
            part_text = MIMEText(text_content, "plain")
            message.attach(part_text)
        
        # HTML 파트
        part_html = MIMEText(html_content, "html")
        message.attach(part_html)
        
        # SMTP 연결 및 발송
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(message)
        
        logger.info(f"이메일 발송 성공: {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"이메일 발송 실패: {e}")
        return False


def send_new_support_notification(
    to_email: str,
    support_title: str,
    support_organization: str,
    support_url: str,
    application_end_date: str
) -> bool:
    """
    신규 공고 알림 이메일
    """
    subject = f"[신규 공고] {support_title}"
    
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #2c3e50;">🎉 새로운 정부지원사업 공고</h2>
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
                <h3 style="margin-top: 0;">{support_title}</h3>
                <p><strong>담당 기관:</strong> {support_organization}</p>
                <p><strong>신청 마감:</strong> {application_end_date}</p>
                <p style="margin-top: 20px;">
                    <a href="{support_url}" 
                       style="background-color: #007bff; color: white; padding: 10px 20px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">
                        자세히 보기
                    </a>
                </p>
            </div>
            <p style="color: #6c757d; font-size: 12px;">
                이 메일은 정부지원사업 크롤러에서 자동으로 발송되었습니다.
            </p>
        </body>
    </html>
    """
    
    return send_email(to_email, subject, html_content)


def send_deadline_reminder(
    to_email: str,
    support_title: str,
    support_url: str,
    days_remaining: int
) -> bool:
    """
    마감 임박 알림 이메일
    """
    subject = f"[마감 D-{days_remaining}] {support_title}"
    
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #dc3545;">⏰ 마감 임박 알림</h2>
            <div style="background-color: #fff3cd; padding: 20px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #ffc107;">
                <h3 style="margin-top: 0;">{support_title}</h3>
                <p style="font-size: 18px; color: #dc3545;"><strong>D-{days_remaining}</strong> 남았습니다!</p>
                <p style="margin-top: 20px;">
                    <a href="{support_url}" 
                       style="background-color: #dc3545; color: white; padding: 10px 20px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">
                        지금 신청하기
                    </a>
                </p>
            </div>
            <p style="color: #6c757d; font-size: 12px;">
                이 메일은 정부지원사업 크롤러에서 자동으로 발송되었습니다.
            </p>
        </body>
    </html>
    """
    
    return send_email(to_email, subject, html_content)
