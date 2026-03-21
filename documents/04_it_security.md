# Volta Coffee Co. — IT Security Policy

**Document ID:** SEC-001  
**Last Updated:** 2026-01-20  
**Owner:** IT Security  
**Classification:** Internal — Confidential

## Purpose

This document defines the mandatory security controls for all Volta Coffee Co. employees, contractors, and third-party vendors with access to Volta systems. Violations may result in disciplinary action up to and including termination.

## Access Control

### Authentication Requirements

- All corporate accounts must use Single Sign-On (SSO) through Google Workspace.
- Multi-factor authentication (MFA) is mandatory on all systems. Approved second factors: hardware security keys (preferred), Google Authenticator, or Authy. SMS-based MFA is not permitted.
- Passwords must be minimum 16 characters, generated and stored in 1Password. Password reuse across services is prohibited.
- Service accounts must use API keys or OAuth tokens rotated every 90 days. Service account credentials are stored in AWS Secrets Manager and must never appear in source code, environment files, or Slack messages.

### Principle of Least Privilege

- Access to systems is granted on a need-to-know basis.
- Production environment access is restricted to the Engineering and DevOps teams. All production access is logged and audited monthly.
- AWS IAM roles are scoped per-service. No engineer has broad admin access except the CTO and VP of Engineering, who use break-glass accounts monitored by CloudTrail.
- Quarterly access reviews are conducted by IT Security. Dormant accounts (no login in 60 days) are automatically suspended.

## Device Security

### Corporate Devices

- All laptops must run macOS with the latest security patches applied within 7 days of release.
- FileVault full-disk encryption must be enabled. IT verifies compliance via Kandji MDM.
- Laptops must lock after 5 minutes of inactivity.
- Only approved software may be installed. The approved software list is maintained in Notion under IT Policies > Approved Software.
- Personal devices may not be used to access corporate systems except for Slack and email via mobile apps with MDM enrollment.

### Network Security

- Retail location WiFi is segmented: POS devices on a dedicated VLAN, customer WiFi on a separate isolated network, and back-office devices on the corporate VLAN.
- VPN (Tailscale) is required for all remote access to staging and production environments.
- Public WiFi usage is permitted only with VPN active.

## Data Classification

| Classification | Description | Examples | Handling |
|---------------|-------------|----------|----------|
| Public | Non-sensitive, externally shareable | Marketing materials, menu | No restrictions |
| Internal | Business info, not sensitive | Meeting notes, project plans | Google Drive with link sharing off |
| Confidential | Sensitive business data | Financial reports, employee records, supplier contracts | Encrypted storage, access-controlled |
| Restricted | Highest sensitivity | Customer PII, payment data, credentials | Encrypted at rest and in transit, audit-logged access |

## Incident Response

### Severity Levels

- **SEV-1 (Critical):** Active data breach, ransomware, or unauthorized access to Restricted data. Response within 15 minutes. All-hands incident response.
- **SEV-2 (High):** Suspected breach, compromised credentials, or malware detection. Response within 1 hour.
- **SEV-3 (Medium):** Policy violation, phishing attempt (not successful), or suspicious activity. Response within 4 business hours.
- **SEV-4 (Low):** Minor policy deviation, access request issues. Response within 1 business day.

### Reporting

Report all security incidents immediately through:
1. **Slack:** #security-incidents channel
2. **Email:** security@voltacoffee.com
3. **Emergency (SEV-1 only):** Call the IT Security Manager at the number listed in 1Password under "Emergency Contacts"

Never attempt to investigate or remediate a suspected breach on your own. Preserve evidence by not modifying affected systems.

## Vendor Security

- All third-party vendors with access to Volta data must complete a security questionnaire before onboarding.
- Vendors handling Confidential or Restricted data must provide SOC 2 Type II certification or equivalent.
- Vendor access is reviewed quarterly and revoked upon contract termination.
- No vendor may store Volta data outside the United States without written approval from the CTO.

## Compliance

Volta Coffee Co. maintains PCI DSS compliance for payment processing through our partnership with Toast (POS) and Shopify Payments (e-commerce). Engineering and IT staff must complete annual PCI awareness training.

All employees must complete Security Awareness Training within 30 days of hire and annually thereafter. Training is delivered through the employee portal and tracked in Notion.
