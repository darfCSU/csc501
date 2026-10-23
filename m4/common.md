# Discovering Common Ground – Frosmear Legacy Modernization

Schumann Hudson Acquisition & Technology (SHAT) is modernizing the legacy Frosmear application by integrating authentication with the Darfcloud platform. A conflict has developed between the Legacy Application Maintenance Engineering (LAME) team and the Protection, Integrity, Threat Assessments (PITA) team over the requirements for transferring authentication tokens. The legacy team wants to preserve compatibility with the existing PHP application and avoid delaying deployment, while the security team wants strong protections against unauthorized access and token misuse. Both departments support the project, but their competing priorities could affect its budget, schedule, and quality.

## Conflict and Dialogue Scenario

During a project meeting, the project manager asks both teams to explain their concerns.

**LAME Lead:** “The existing application depends on established login procedures. Additional handoff requirements could require changes to legacy code and testing that were not included in our original estimate. We need a solution that works with the existing application without creating unnecessary delays.”

**PITA Lead:** “We cannot approve an authentication handoff without appropriate protections. Tokens must be difficult to misuse, and the process must prevent unauthorized access. Moving forward without verifying these controls could create a security risk that is more expensive to correct later.”

**Project Manager  (PM):** “Both concerns are valid. Instead of treating compatibility and security as competing goals, we need to identify the minimum requirements that satisfy both teams. Let us document the risks, estimate the work involved, and agree on acceptance criteria before deciding whether the schedule needs to change.”

The PM would then facilitate a requirements review covering token expiration, single-use enforcement, secure transmission, access authorization, failure handling, and testing. The teams would distinguish essential security controls from implementation preferences and identify any additional work that could affect the schedule or budget.

## Negotiation and Conflict Resolution

We would use collaborative, interest-based negotiation to find common ground. Rather than allowing either department to dictate the solution, the PM would identify shared interests: a reliable authentication handoff, protection of user accounts, and delivery within reasonable project constraints. Peters (2002) emphasizes planning strategies for delivering quality projects, supporting the need to evaluate requirements, risks, and resources before committing to a delivery plan.

The PM would also use objective criteria to evaluate proposed solutions. Both teams could agree that a token must be transmitted securely, accepted only once, expire after a defined period, and be rejected when the user does not meet the authorization requirements. The legacy team could recommend an implementation compatible with the existing application, while the security team verifies that it satisfies the agreed controls.

Rasmussen and Niles (2019) discuss project management considerations associated with data center projects, providing an infrastructure-focused perspective on coordinating technical requirements and project execution. The PM should assess dependencies and implementation risks before approving a change. If the required testing exceeds available resources, the PM should present the schedule and cost implications to the appropriate stakeholders rather than reducing security requirements.

## Recommendations and Conclusion

We would document the negotiated requirements, assign responsibility for implementation and security testing, and establish measurable acceptance criteria. A test environment would allow the teams to verify successful handoffs, expired and reused tokens, unauthorized users, and failure scenarios before deployment. If testing identifies a significant risk, the PM would coordinate corrective work and communicate any schedule impact to stakeholders.

This approach balances security, compatibility, cost, and schedule without assuming that one department must lose for the project to succeed. By using collaborative negotiation, objective acceptance criteria, and risk-based planning, SHAT can turn departmental disagreement into a shared decision-making process. The result would be a secure, maintainable authentication handoff that supports the project's overall modernization goals.

## References

Peters, L. A. (2002). *Eight planning strategies for delivering quality projects*. Project Management Institute. https://www.pmi.org/learning/library/planning-strategies-delivering-quality-projects-1052

Rasmussen, N., & Niles, S. (2019). *Data center projects: Project management*. Schneider Electric, Data Center Science Center. https://www.facilitiesnet.com/whitepapers/pdfs/APC_083011.pdf
