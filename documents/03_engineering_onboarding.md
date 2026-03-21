# Volta Coffee Co. — Engineering & IT Onboarding Guide

**Document ID:** ENG-001  
**Last Updated:** 2026-02-01  
**Owner:** Engineering  
**Classification:** Internal Use Only

## First Day Checklist

Your manager should have completed the pre-boarding setup before your start date. Confirm you have access to the following on Day 1:

1. **Laptop:** MacBook Pro M3 (Engineering) or MacBook Air M3 (non-Engineering). IT ships devices 3 business days before start date.
2. **Accounts:** Google Workspace (email, Drive, Calendar), Slack, GitHub (volta-coffee org), Notion, 1Password team vault.
3. **Dev Environment:** Homebrew, Docker Desktop, Node.js 20 LTS, Python 3.12, and the Volta monorepo cloned from `github.com/volta-coffee/volta-platform`.
4. **VPN:** Tailscale with your @voltacoffee.com Google account. Required for accessing staging and production environments.

If anything is missing, file a ticket in the #it-support Slack channel. Typical response time is under 2 hours during business hours.

## System Architecture Overview

Volta's technology stack supports three primary domains:

### 1. Point of Sale & Retail Operations
- **POS System:** Toast POS across all retail locations
- **Scheduling & Time Tracking:** Homebase, integrated with Gusto payroll
- **Inventory:** BlueCart for ordering; custom inventory tracker (internal app, see below)

### 2. E-Commerce & DTC
- **Storefront:** Shopify Plus (voltacoffee.com)
- **Subscription Management:** Recharge, integrated with Shopify
- **Fulfillment:** ShipStation connected to the roastery warehouse in Red Hook, Brooklyn

### 3. Internal Platform (volta-platform)
The monorepo at `volta-platform` contains:
- **inventory-service:** Node.js/Express API for green coffee inventory tracking. Connects to a PostgreSQL database on AWS RDS.
- **roast-log-service:** Python/FastAPI service that records roast profiles from Cropster and calculates batch consistency scores.
- **employee-portal:** Next.js app for internal tools — shift schedules, PTO requests, training modules.
- **data-pipeline:** Airflow DAGs that sync data from Toast, Shopify, and Homebase into our analytics warehouse (BigQuery).

### Infrastructure
- **Cloud:** AWS (us-east-1). Staging and production accounts are separate.
- **Container Orchestration:** ECS Fargate for all services.
- **CI/CD:** GitHub Actions. All merges to `main` deploy to staging automatically. Production deploys require a manual approval in the #releases Slack channel.
- **Monitoring:** Datadog for metrics and logs. PagerDuty for on-call alerts (Engineering only).
- **Secrets Management:** AWS Secrets Manager. Never store credentials in code or environment files.

## Development Workflow

1. Create a feature branch from `main`: `feature/JIRA-123-description`
2. Open a PR when ready. Require at least 1 approval from a code owner.
3. All PRs must pass CI: lint, unit tests, and integration tests.
4. Merge via squash-and-merge to keep history clean.
5. Staging deploy is automatic. Verify in staging before requesting production deploy.

## On-Call Rotation

Engineering participates in a weekly on-call rotation for production incidents.

- **Schedule:** Managed in PagerDuty. Rotation changes every Monday at 9:00 AM ET.
- **Response SLA:** Acknowledge within 15 minutes. Begin investigation within 30 minutes.
- **Escalation:** If unresolved after 1 hour, escalate to the Engineering Manager on the secondary rotation.
- **Compensation:** On-call engineers receive a $300/week stipend plus $150 per incident outside business hours.

## Security Requirements

- Enable FileVault disk encryption on your Mac.
- Use 1Password for all credentials. No browser-saved passwords.
- Enable 2FA on all accounts (Google, GitHub, AWS, Slack).
- Never copy production data to local machines. Use staging databases for development.
- Report any suspected security incidents immediately to #security-incidents on Slack.
