# Module 4: Project Design and Outline
## Frosmear Legacy Modernization

**Company:** Schumann Hudson Acquisition & Technology (SHAT)  
**Project:** Frosmear Legacy Modernization  
**Target Platform:** www.darfcloud.com  
**Project Start Date:** October 1, 2026  
**Target Completion Date:** December 23, 2026  
**Estimated Duration:** 12 weeks  
**Estimated Budget:** $210,000

## 1. Project Scope and Goals

The Frosmear Legacy Modernization project will transform the existing PHP-based Frosmear website into Darfcloud, a modern, cloud-oriented application platform. The project will establish a maintainable foundation using Docker containers, the Django web framework, and a MySQL database.

The platform will support future artificial intelligence concepts, general-purpose applications, and investment-analysis tools. Advanced applications and additional business features are outside the initial release and will be considered for FY2027 unless approved through change control.

Two specialized teams will support the work. **LAME (Legacy Application Maintenance Engineering)** will address PHP compatibility, preservation of relevant functionality, and migration dependencies. **PITA (Protection, Integrity, Threat Assessments)** will focus on authentication, authorization, data integrity, security risks, and protection against unauthorized access or misuse of the authentication handoff.

Success will be measured by completion of the agreed functionality, validation of migrated account data, satisfaction of security requirements, user testing, and stakeholder acceptance of the deployed system.

## 2. Project Timeline and Major Deliverables

The project runs from October 1 through December 23, 2026. Its schedule uses overlapping activities to meet the 12-week delivery target. Parallel work requires coordination among the core development team, LAME, PITA, and operations. Marketing has emphasized delivery before 2027, making timely decisions and blocker resolution important.

| Project Phase | Duration | Start Date | Completion Date | Major Deliverables |
|---|---:|---|---|---|
| 1. Planning | 2 weeks | October 1, 2026 | October 16, 2026 | Project charter, scope, budget, schedule, stakeholder plan |
| 2. Current System Assessment | 2 weeks | October 12, 2026 | October 23, 2026 | Legacy inventory, requirements, migration assessment, compatibility review |
| 3. Architecture and Environments | 2 weeks | October 19, 2026 | October 30, 2026 | Docker/Django/MySQL architecture, environment standards, security requirements |
| 4. Application Development | 4 weeks | October 19, 2026 | November 20, 2026 | Authentication, permissions, application menu, legacy integration |
| 5. Data Migration and Security | 3 weeks | November 2, 2026 | December 4, 2026 | Migrated accounts, provisioning, compatibility validation, security controls, backup and recovery procedures |
| 6. Testing and Deployment | 2 weeks | November 23, 2026 | December 18, 2026 | Functional, security, and integration testing; deployment; operational handoff |
| 7. Project Closeout | 2 weeks | December 7, 2026 | December 30, 2026 | Acceptance, documentation, lessons learned, maintenance plan |

The schedule allows assessment to begin before planning is completely finished and migration and security work to overlap with development. LAME will identify legacy dependencies early, while PITA will review security requirements throughout implementation. Activities may proceed in parallel where dependencies permit, but testing and deployment require completion of critical prerequisites.

December 23 is the target delivery date. There is additional time allocated through December 30 to provide schedule slack for delays and closeout activities. The project manager will monitor dependencies, coordinate teams, and escalate issues that threaten the target.

## 3. Budget and Resource Allocation

The preliminary project budget is $210,000. This hypothetical corporate estimate assumes an experienced team, coordinated parallel work, and a defined initial release. It is a planning estimate rather than an approved budget or vendor quotation.

| Budget Category | Estimated Cost |
|---|---:|
| Project management and stakeholder coordination | $25,000 |
| Application development and legacy integration | $65,000 |
| Data migration and database validation | $25,000 |
| Security engineering and review | $20,000 |
| Testing, quality assurance, and deployment | $20,000 |
| Infrastructure, hosting, and software | $10,000 |
| Training, documentation, and operational transition | $5,000 |
| Team-building and stakeholder engagement | $10,000 |
| Contingency reserve | $30,000 |
| **Total Estimated Budget** | **$210,000** |

The team-building allocation covers a private suite at a Colorado Avalanche game to recognize contributions and strengthen collaboration across technical and operational groups. The project sponsor must approve this expense, and it cannot take priority over essential development, security, testing, or deployment costs.

The contingency reserve covers approved responses to unforeseen risks, including legacy dependencies, migration problems, or additional testing. It is not an automatic spending allowance.

Primary project resources and responsibilities include:

- **Glenda Schumann, CEO:** Executive sponsorship, strategic direction, and major decisions.
- **Zelda Hudson, CTO:** Technical leadership, architecture, and resolution of technical blockers.
- **Theresa Hudson, CFO:** Budget oversight, cost tracking, and financial analysis.
- **Gordie Roberts, Director of Operations:** Operational readiness, deployment coordination, and service continuity.
- **Jay Caufield, Legacy Systems Manager and LAME lead:** Legacy knowledge, PHP compatibility, and migration support.
- **Jim Paek, Lead Django/Darfcloud Developer:** Application implementation, integration, and technical quality.
- **Grant Jennings, Information Security Manager and PITA lead:** Security architecture, threat assessments, access controls, and security testing.
- **LAME and PITA team members:** Legacy assessment, compatibility validation, security reviews, data integrity, and release readiness.
- **User representatives:** Usability feedback, workflow validation, and acceptance testing.
- **Cloud-provider representatives:** Hosting and infrastructure guidance as needed.

The project manager and CFO will validate staffing assumptions, labor rates, hosting expenses, software costs, and vendor charges before finalizing the budget. Dedicated legacy and security teams are intended to reduce bottlenecks while the core development team builds the platform.

## 4. Stakeholder Analysis

Stakeholder engagement will follow the analysis established in Module 2. Communication will reflect each stakeholder's influence, interest, responsibilities, and required level of involvement.

| Stakeholder | Primary Interest | Engagement Approach |
|---|---|---|
| Glenda Schumann, CEO | Strategic value and project success | Executive updates, milestone reviews, major decisions |
| Zelda Hudson, CTO | Technical direction and delivery | Architecture reviews, technical decisions, blocker resolution |
| Theresa Hudson, CFO | Budget and cost control | Forecasts, variance reports, change-cost assessments |
| Gordie Roberts, Operations | Service continuity and readiness | Deployment planning, transition reviews, contingency preparation |
| Jay Caufield, LAME lead | Legacy compatibility and system knowledge | Assessment, migration reviews, knowledge transfer |
| Jim Paek, Lead Developer | Implementation and maintainability | Technical planning, development reviews, demonstrations |
| Grant Jennings, PITA lead | Security and risk reduction | Security reviews, threat assessments, release-readiness reviews |
| LAME team | Preservation of relevant legacy functionality | Compatibility reviews, migration planning, issue escalation |
| PITA team | Protection of users, systems, and data | Security design reviews, authorization tests, data-integrity validation |
| User representatives | Usability and functionality | Feedback sessions, demonstrations, acceptance testing |
| Shareholder representative | Financial performance and long-term value | Progress updates, risk reporting, financial summaries |

The project manager will monitor stakeholder engagement and address gaps between current and required involvement. LAME's early participation will help uncover legacy issues before they affect delivery. PITA's involvement in authentication and authorization design will help identify token misuse, unauthorized access, and data-integrity risks before deployment. The CFO will receive cost forecasts and explanations of financial impacts to support informed decisions.

Communication will include status reports, milestone reviews, issue escalation, and demonstrations. Stakeholder feedback will be documented and evaluated, but will not automatically become additional project scope.

## 5. Change Requests and Goal Alignment

Changes to requirements, schedule, budget, or deliverables must be documented and evaluated for their effects on scope, cost, schedule, technical dependencies, security, and business value. The project manager will coordinate the review, with the CTO assessing technical impacts, PITA reviewing security, LAME evaluating legacy compatibility and migration, and the CFO assessing costs. Significant baseline changes require approval from the project sponsor or designated steering committee.

This process limits scope creep and protects the delivery target. For example, adding an advanced AI application to the initial release would require evaluating its resource, schedule, and security impacts. If it threatens core modernization objectives, it should be deferred. Additional legacy work identified by LAME may affect migration schedules, while essential PITA security controls cannot simply be omitted to save time. Any required baseline adjustment must be evaluated and approved.

The project reduces dependence on legacy technology, improves maintainability and security, and establishes a foundation for future applications. Phased delivery identifies problems early, incorporates feedback, and informs decisions before deployment.

## 6. Maintenance and Project Closeout

The project begins with planning and system assessment in October 2026, followed by development, migration, testing, and deployment, with delivery targeted for December 23. The remaining time through December 30 provides flexibility for delays and closeout activities.

After deployment and acceptance, operational responsibility will transfer to the designated operations team. Initial stabilization and maintenance are expected to begin in January 2027 and continue through the first quarter. Ongoing responsibilities will include system monitoring, security updates, backup verification, recovery testing, account administration, and incident response. LAME will provide legacy-system documentation and compatibility support, while PITA will help establish security monitoring, incident escalation, access-control reviews, and periodic validation of security controls.

Closeout will include formal acceptance, technical and operational documentation, transfer of responsibilities, and a lessons-learned review. The project manager will document unresolved issues and recommendations for future development. Ongoing maintenance and FY2027 enhancements will be managed separately from the initial implementation budget and schedule.

## Conclusion

The Frosmear Legacy Modernization project uses a 12-week delivery plan, a $210,000 estimated budget, and a cross-functional team to establish Darfcloud as a maintainable application platform. Its scope, schedule, resources, stakeholder responsibilities, and change-control process provide a framework for coordinating the work and managing delivery risks.

LAME will protect legacy compatibility, while PITA will focus on security and data integrity. Their involvement throughout the project allows the team to address technical concerns while development proceeds in parallel. The project will be successful when the agreed initial release is tested, accepted, and deployed to the website at www.darfcloud.com providing a foundation for further development in 2027.
