#!/usr/bin/env python3
"""
Email notification script for CI/CD pipeline
Sends deployment status notifications via SMTP
Based on the original working script with enhancements
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sys


def send_mail(status, workflow_name=None, repo_name=None, workflow_run_id=None, deployment_url=None):
    """
    Send email notification about workflow/deployment status
    
    Args:
        status: 'success' or 'failed'
        workflow_name: Name of the GitHub workflow
        repo_name: Repository name
        workflow_run_id: GitHub Actions run ID
        deployment_url: URL of deployed application (optional)
    """
    
    # Email configuration from environment variables
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    
    # Get workflow details from environment if not provided
    workflow_name = workflow_name or os.getenv('WORKFLOW_NAME', 'CI/CD Pipeline')
    repo_name = repo_name or os.getenv('REPO_NAME', 'React-ci-cd-setup')
    workflow_run_id = workflow_run_id or os.getenv('WORKFLOW_RUN_ID', 'N/A')
    deployment_url = deployment_url or os.getenv('DEPLOYMENT_URL')
    
    # Validate required credentials
    if not sender_email or not sender_password:
        print('❌ ERROR: SENDER_EMAIL or SENDER_PASSWORD not found in environment variables')
        sys.exit(1)
    
    if not receiver_email:
        receiver_email = sender_email  # Default to sender if receiver not specified
    
    # Create email message based on status
    if status == 'success':
        subject = f"✅ Deployment Successful - {repo_name}"
        
        # HTML body for success
        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f9fafb;">
            <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
              <h2 style="color: #22c55e; margin-top: 0;">
                ✅ Deployment Successful!
              </h2>
              
              <div style="background: #f0fdf4; padding: 15px; border-radius: 5px; border-left: 4px solid #22c55e;">
                <p style="margin: 5px 0;"><strong>Repository:</strong> {repo_name}</p>
                <p style="margin: 5px 0;"><strong>Workflow:</strong> {workflow_name}</p>
                <p style="margin: 5px 0;"><strong>Run ID:</strong> {workflow_run_id}</p>
                {f'<p style="margin: 5px 0;"><strong>Deployment URL:</strong> <a href="{deployment_url}" style="color: #2563eb;">{deployment_url}</a></p>' if deployment_url else ''}
              </div>
              
              <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
                <p style="color: #6b7280; font-size: 14px; margin: 0;">
                  🤖 This is an automated notification from your CI/CD pipeline.
                </p>
              </div>
            </div>
          </body>
        </html>
        """
        
        # Plain text fallback
        text_body = f"""
        ✅ Deployment Successful!
        
        Repository: {repo_name}
        Workflow: {workflow_name}
        Run ID: {workflow_run_id}
        {f'Deployment URL: {deployment_url}' if deployment_url else ''}
        
        ---
        This is an automated notification from your CI/CD pipeline.
        """
        
    else:  # failed
        subject = f"❌ Workflow Failed - {repo_name}"
        
        # Get GitHub Actions URL if available
        github_url = f"https://github.com/{repo_name}/actions/runs/{workflow_run_id}" if workflow_run_id != 'N/A' else None
        
        # HTML body for failure
        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f9fafb;">
            <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
              <h2 style="color: #ef4444; margin-top: 0;">
                ❌ Workflow Failed
              </h2>
              
              <div style="background: #fef2f2; padding: 15px; border-radius: 5px; border-left: 4px solid #ef4444;">
                <p style="margin: 5px 0;"><strong>Repository:</strong> {repo_name}</p>
                <p style="margin: 5px 0;"><strong>Workflow:</strong> {workflow_name}</p>
                <p style="margin: 5px 0;"><strong>Run ID:</strong> {workflow_run_id}</p>
              </div>
              
              <p style="margin-top: 20px;">
                The workflow <strong>{workflow_name}</strong> failed for repository <strong>{repo_name}</strong>.
              </p>
              
              {f'<p><a href="{github_url}" style="display: inline-block; padding: 10px 20px; background: #2563eb; color: white; text-decoration: none; border-radius: 5px; margin-top: 10px;">View Logs on GitHub</a></p>' if github_url else '<p style="color: #6b7280;">Please check the logs for more details.</p>'}
              
              <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
                <p style="color: #6b7280; font-size: 14px; margin: 0;">
                  🤖 This is an automated notification from your CI/CD pipeline.
                </p>
              </div>
            </div>
          </body>
        </html>
        """
        
        # Plain text fallback
        text_body = f"""
        ❌ Workflow Failed
        
        Repository: {repo_name}
        Workflow: {workflow_name}
        Run ID: {workflow_run_id}
        
        The workflow {workflow_name} failed for repository {repo_name}.
        {f'View logs: {github_url}' if github_url else 'Please check the logs for more details.'}
        
        ---
        This is an automated notification from your CI/CD pipeline.
        """
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    
    # Attach both plain text and HTML versions
    msg.attach(MIMEText(text_body, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))
    
    # Send email
    try:
        # Use Gmail SMTP with STARTTLS (port 587) - most compatible
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        
        print(f'✅ Email sent successfully to {receiver_email}')
        return True
        
    except Exception as e:
        print(f'❌ Error sending email: {e}')
        return False


if __name__ == "__main__":
    # Check if status argument is provided
    if len(sys.argv) > 1:
        status = sys.argv[1]  # Get status from command line argument
    else:
        status = os.getenv('STATUS', 'failed')  # Default to 'failed' for backward compatibility
    
    # Get deployment URL if provided as second argument
    deployment_url = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Send the email
    send_mail(
        status=status,
        deployment_url=deployment_url
    )
