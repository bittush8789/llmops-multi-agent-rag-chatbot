import os

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs')

def create_docs():
    os.makedirs(DOCS_DIR, exist_ok=True)
    
    docs = {
        "company_overview.txt": """TechNova Solutions is a leading AI, Cloud, and Software Services company founded in 2020.
We specialize in providing cutting-edge technological solutions for enterprise businesses. Our mission is to automate and streamline operations through artificial intelligence and cloud-native architecture.
Headquarters: San Francisco, CA.
Global Offices: London, Tokyo, Bangalore.
We are committed to delivering secure, scalable, and innovative solutions.""",

        "services.txt": """TechNova Solutions offers the following core services:
1. Custom AI Development: Building bespoke LLM applications and machine learning models.
2. Cloud Migration & Management: End-to-end cloud infrastructure services on AWS, Azure, and Google Cloud.
3. Enterprise Software Development: Full-stack web and mobile application development.
4. Data Analytics & BI: Big data processing and business intelligence dashboards.
5. Cyber Security Consulting: Penetration testing, compliance auditing, and security architecture.""",

        "support_faq.txt": """Frequently Asked Questions:
Q: What are your working hours?
A: Our global support team is available 24/7. Core business hours are 9 AM to 6 PM PST.

Q: How do I contact technical support?
A: You can reach technical support via email at support@technovasolutions.com or call 1-800-555-NOVA.

Q: Do you offer service level agreements (SLAs)?
A: Yes, we offer 99.9% uptime SLAs for all enterprise contracts.

Q: How do I reset my password for the customer portal?
A: Click on the "Forgot Password" link on the portal login page. A reset link will be sent to your registered email.

Q: Can I upgrade my plan mid-cycle?
A: Yes, you can upgrade your plan at any time through the billing dashboard. Prorated charges will apply.

Q: Do you provide dedicated account managers?
A: Yes, all Enterprise tier clients are assigned a dedicated account manager.

Q: How long does a typical cloud migration take?
A: A typical migration takes between 3 to 6 months depending on the complexity of your infrastructure.

Q: Is there a free trial for your products?
A: We offer a 14-day free trial for NovaChat AI and NovaAnalytics.

Q: How do I cancel my subscription?
A: Subscriptions can be cancelled via the billing portal. Notice must be given 30 days prior to the next billing cycle.

Q: What payment methods do you accept?
A: We accept all major credit cards, wire transfers, and ACH payments.""",

        "pricing.txt": """Pricing Plans:
Starter: $99/month. Includes basic access to NovaCloud and standard email support.
Pro: $499/month. Includes NovaChat AI, NovaAnalytics, and priority 24/7 support.
Enterprise: Custom pricing. Includes full suite, dedicated account manager, custom integrations, and SLA guarantee.
Consulting rate: $250/hour for custom software development.""",

        "refund_policy.txt": """TechNova Solutions Refund Policy:
We offer a 30-day money-back guarantee for all new software subscriptions. If you are not satisfied within the first 30 days, contact billing@technovasolutions.com for a full refund.
Consulting services and custom development work are non-refundable once the statement of work is signed and work has commenced.
Prorated refunds are not provided for mid-cycle cancellations after the initial 30 days.""",

        "hr_policy.txt": """TechNova Human Resources Policy:
TechNova Solutions is an equal opportunity employer. We embrace diversity and inclusion.
Leave Policy: Employees receive 20 days of paid time off (PTO) per year, 10 paid public holidays, and unlimited sick leave with manager approval.
Remote Work: We operate a hybrid work model. Employees can work remotely up to 3 days a week.
Benefits: Comprehensive health, dental, and vision insurance. 401(k) matching up to 5%.""",

        "security_policy.txt": """TechNova Security & Compliance Policy:
Data Protection: All customer data is encrypted at rest using AES-256 and in transit using TLS 1.3.
Compliance: TechNova is SOC 2 Type II certified, GDPR compliant, and HIPAA compliant for healthcare clients.
Access Control: We enforce strict Role-Based Access Control (RBAC) and mandatory Multi-Factor Authentication (MFA) for all internal systems.
Incident Response: We have a dedicated 24/7 Security Operations Center (SOC). In the event of a breach, customers are notified within 24 hours.""",

        "case_studies.txt": """Case Studies:
Acme Corp: TechNova successfully migrated Acme Corp's legacy on-premise infrastructure to NovaCloud, resulting in a 40% reduction in IT costs and 99.99% uptime.
Global Finance Inc: We implemented NovaAnalytics to process over 10TB of financial data daily, reducing report generation time from 48 hours to 15 minutes.
HealthPlus: Our team deployed a custom HIPAA-compliant version of NovaChat AI, which now handles 60% of their initial patient inquiries automatically.""",

        "contact.txt": """Contact Information:
General Inquiries: info@technovasolutions.com
Sales: sales@technovasolutions.com
Support: support@technovasolutions.com
Phone: 1-800-555-NOVA (6682)
Address: 123 Innovation Drive, Suite 500, San Francisco, CA 94105, USA""",

        "product_docs.txt": """Product Documentation:
1. NovaChat AI: Our flagship enterprise conversational AI. It integrates with your internal knowledge base to provide instant answers to employee and customer queries. Features include multi-language support and sentiment analysis.
2. NovaCloud: A secure, scalable cloud hosting platform optimized for AI workloads. Features auto-scaling, built-in DDoS protection, and one-click database deployments.
3. NovaAnalytics: A big data platform that connects to various data sources (SQL, NoSQL, APIs) to provide real-time dashboards and predictive analytics using machine learning.
4. NovaAutomation: A Robotic Process Automation (RPA) tool that automates repetitive tasks such as data entry, invoice processing, and report generation."""
    }

    for filename, content in docs.items():
        filepath = os.path.join(DOCS_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created: {filename}")

if __name__ == "__main__":
    print("Generating fictional company data...")
    create_docs()
    print("Done!")
