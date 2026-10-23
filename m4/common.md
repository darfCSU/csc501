# Discovering Common Ground – Frosmear Legacy Modernization

Schumann Hudson Acquisition & Technology (SHAT) is modernizing the legacy Frosmear application by integrating authentication with Darfcloud. A conflict has developed between the Legacy Application Maintenance Engineering (LAME) team and the Protection, Integrity, Threat Assessments (PITA) team over authentication token handoff requirements. LAME wants to preserve compatibility with the existing PHP application and avoid delays, while PITA prioritizes protection against unauthorized access and token misuse. Both teams support the project, but their competing priorities could affect cost, schedule, and quality.

## Conflict and Dialogue Scenario

The project manager (PM) asks both teams to explain their concerns:

**LAME Lead:** “Additional handoff requirements could require legacy code changes and testing beyond our original estimate. We need a solution that works with the existing application without unnecessary delays.”

**PITA Lead:** “We cannot approve the handoff without appropriate protections. Tokens must be difficult to misuse, and the process must prevent unauthorized access. Skipping these controls could create more expensive problems later.”

**PM:** “Both concerns are valid. Instead of treating compatibility and security as competing goals, we need requirements that satisfy both teams. Let us document the risks, estimate the work, and agree on acceptance criteria before deciding whether the schedule needs to change.”

The PM would facilitate a review of token expiration, single-use enforcement, secure transmission, access authorization, failure handling, and testing. The teams would distinguish essential security controls from implementation preferences and identify impacts on cost and schedule.

## Negotiation and Conflict Resolution

We would use collaborative, interest-based negotiation to find common ground. Rather than allowing either department to dictate the solution, the PM would identify shared interests: reliable authentication, protection of user accounts, and delivery within reasonable project constraints. Peters (2002) discusses planning strategies for delivering quality projects, supporting the need to evaluate requirements, risks, and resources before committing to a delivery plan.

The PM would use objective criteria to evaluate proposed solutions. Both teams could agree that tokens must be transmitted securely, accepted only once, expire after a defined period, and be rejected when users lack authorization. LAME could recommend an approach compatible with the existing application, while PITA verifies that it meets the agreed controls.

Rasmussen and Niles (2019) provide an infrastructure-focused perspective on coordinating technical requirements and project execution. Applying this approach, the PM should assess dependencies and implementation risks before approving changes. If testing exceeds available resources, the PM should present the schedule and cost implications to stakeholders rather than reduce security requirements.

## Recommendations and Conclusion

We would document the negotiated requirements, assign responsibility for implementation and security testing, and establish measurable acceptance criteria. A test environment would verify successful handoffs, expired and reused tokens, unauthorized users, and failure scenarios before deployment. If testing identifies significant risks, the PM would coordinate corrective work and communicate schedule impacts to stakeholders.

This approach is "win-win" as it balances security, compatibility, cost, and schedule requirements. Collaborative negotiation, objective acceptance criteria, and risk-based planning can turn disagreement into shared decision-making. The result would be a secure, maintainable authentication handoff that supports the modernization vision.

## References

Peters, L. A. (2002). *Eight planning strategies for delivering quality projects*. Project Management Institute. https://www.pmi.org/learning/library/planning-strategies-delivering-quality-projects-1052

Rasmussen, N., & Niles, S. (2019). *Data center projects: Project management*. Schneider Electric, Data Center Science Center. https://www.facilitiesnet.com/whitepapers/pdfs/APC_083011.pdf
