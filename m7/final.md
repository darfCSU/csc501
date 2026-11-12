# Frosmear Legacy Modernization Integrated Project Plan

| **Company** | Schumann Hudson Acquisitions & Technologies (SHAT) |
|---|---|
| **Project** | Frosmear Legacy Modernization |
| **Target Platform** | Darfcloud — [www.darfcloud.com](https://www.darfcloud.com) |
| **Project Start** | October 1, 2026 |
| **Target Delivery** | December 23, 2026 |
| **Estimated Duration** | 12 weeks |
| **Estimated Budget** | $210,000 |

---

## Executive Summary

Schumann Hudson Acquisitions & Technologies (SHAT) will modernize Frosmear.com, a legacy PHP-based website, by replacing its existing foundation with Darfcloud, a modern application platform built with Docker containers, Django, and MySQL. The initial release will establish a maintainable platform for future artificial intelligence concepts, general-purpose applications, and investment-analysis tools.

The project must preserve relevant legacy functionality while improving maintainability, security, account management, and deployment practices. The work includes requirements and legacy-system assessment, architecture and environment preparation, application development, authentication integration, data migration, security validation, testing, deployment, and operational transition.

The project will use a hybrid management approach. Predictive planning will establish the scope, budget, schedule, major deliverables, and governance. Iterative development and demonstrations will allow the technical team to validate functionality and respond to findings without losing control of the approved project baseline.

Two specialized teams will address major technical concerns. The Legacy Application Maintenance Engineering (LAME) team will assess legacy PHP functionality, compatibility, and migration dependencies. The Protection, Integrity, Threat Assessments (PITA) team will review authentication, authorization, data integrity, and security controls. The project manager will coordinate these teams with development, operations, executives, and user representatives.

The project has a preliminary budget of $210,000 and a target delivery date of December 23, 2026. The schedule includes closeout activities through December 30. Success will be measured by delivery of the agreed initial-release functionality, validated account data, satisfactory security and integration testing, operational readiness, and stakeholder acceptance.

## Background and Project Justification

[Frosmear.com](https://www.frosmear.com/) is a legacy PHP-based website that has become a foundation for a broader set of planned applications. Continuing to expand the existing system would preserve technical dependencies and make future development exponentially more time-consuming. Modernization provides an opportunity to establish a clean architecture, improve security and deployment practices, and create a platform that can support rapid new application development.

[Darfcloud](https://www.darfcloud.com/) will use Docker to package and deploy application services, Django as its web framework, and MySQL for relational data. These established technologies were selected for maintainability, long-term support, security, deployment flexibility, and compatibility with the existing environment. They also provide a foundation for future applications while keeping the new platform separate from the legacy PHP implementation.

Docker provides consistent packaging across development and deployment environments. Django offers an established application framework with built-in authentication capabilities, while MySQL stores account and application data. Together, these technologies replace the legacy foundation without carrying its implementation dependencies into the new platform.

The project is not intended to deliver every future Darfcloud application. Its purpose is to establish the platform and complete the core functionality required for an initial release. Advanced AI capabilities, additional applications, and other enhancements will be considered for CY2027 and managed through a separate planning and approval process.

## Project Objectives and Success Criteria

The project objectives are to:

- Establish the Darfcloud application platform using Docker, Django, and MySQL.
- Implement the initial authentication, authorization, and application-navigation capabilities.
- Integrate required functionality with the existing Frosmear environment while limiting legacy dependencies.
- Migrate and validate the account data required for the initial release.
- Implement and verify security controls for authentication, authorization, token handling, and data integrity.
- Test application functionality, database operations, legacy integration, deployment, backup, and recovery procedures.
- Deploy the initial release and transfer operational responsibility.

The project will be considered successful when:

- The initial-release functionality is available on the Darfcloud platform.
- Required account data is migrated and validated.
- Authentication and authorization behave as specified.
- Functional, integration, and security testing is completed.
- Deployment, backup, and recovery procedures are tested and documented.
- The project sponsor and designated stakeholders accept the completed deliverables.

## Project Scope

### In Scope

The initial project scope includes:

- Assessment of the existing Frosmear PHP application and its dependencies.
- Requirements analysis and identification of functionality to preserve.
- Docker, Django, and MySQL architecture and environment preparation.
- Core application authentication and account permissions.
- Application navigation and menu functionality.
- Required integration between the legacy Frosmear application and Darfcloud.
- Account-data migration, mapping, and validation.
- Authentication handoff security, token handling, and authorization testing.
- Functional, integration, security, and deployment testing.
- Backup and recovery validation.
- User feedback, stakeholder acceptance, documentation, and operational handoff.

## Out of Scope

The following items are not part of the initial release unless approved through formal change control:

- Advanced artificial intelligence applications.
- New investment-analysis products beyond the platform foundation and agreed initial functionality.
- Additional applications or major feature expansions planned for 2027.
- Unrelated redesign or replacement of legacy functionality that is not required for the agreed release.
- Ongoing maintenance and enhancements after the initial operational transition.

## Scope Management and Change Control

The project manager will maintain the approved scope, schedule, and budget baselines. Requirements and deliverables will have measurable acceptance criteria. Stakeholder suggestions and discoveries made during development will be documented and evaluated rather than automatically added to the project.

Each change request must describe the requested change and its expected effect on scope, schedule, budget, resources, security, technical dependencies, and business value.

The project manager will coordinate the assessment with the appropriate leads:

- The CTO will assess architecture and technical impacts.
- LAME will assess legacy compatibility and migration impacts.
- PITA will assess security and data-protection impacts.
- The CFO will assess cost and budget impacts.
- Operations will assess deployment and support impacts.

The project sponsor must approve significant changes to the project baselines. Essential security controls will not be removed simply to protect the schedule. If a required change threatens the delivery target, the project manager will present the impact and recommend an appropriate adjustment or deferral of nonessential functionality.

## Project Management and Development Approach

A hybrid project management approach is appropriate because the project requires defined commitments while involving technical uncertainty. Predictive planning will establish the project charter, scope, budget, schedule, major deliverables, responsibilities, and change-control process. Iterative development will allow the team to implement and validate functionality in increments. This combination reflects the hybrid life-cycle approach described by the Project Management Institute (PMI, 2017), in which predictive and agile practices can be selected to fit a project's characteristics rather than forcing every activity into a single method.

The project will begin with requirements analysis and assessment of the existing Frosmear application. The team will identify functionality to preserve, data to migrate, and dependencies between the legacy PHP application and Darfcloud.

The technical team will define the Docker, Django, and MySQL architecture, including application structure, database organization, environment configuration, authentication interfaces, and deployment requirements. Security requirements will be incorporated during design rather than postponed until release. The team will use relevant NIST security and privacy controls for access control, identification and authentication, auditability, configuration management, and contingency planning. (Ross & Pillitteri, 2020).

Development will proceed in increments. Core functionality will be demonstrated and tested as it becomes available. Feedback and defects will be evaluated against the approved requirements. Data migration and security work may proceed alongside development where dependencies permit. Integration and acceptance testing will verify that the components work together.

This approach provides a balance between planning and adaptation. The team can respond to information discovered during implementation while maintaining accountability for the agreed deliverables, schedule, and budget.

## Work Breakdown and Major Deliverables

The following high-level work breakdown organizes the project into manageable phases and deliverables.

| Work package | Major activities | Principal deliverables |
|---|---|---|
| 1. Project planning | Confirm objectives, requirements, stakeholders, resources, budget, schedule, and governance | Project charter and management baselines |
| 2. Current-system assessment | Inventory legacy PHP functionality, dependencies, data, and integration requirements | Legacy inventory, requirements, migration assessment |
| 3. Architecture and environments | Define Docker/Django/MySQL architecture, environment standards, and security requirements | Architecture and environment specifications |
| 4. Application development | Implement authentication, permissions, application navigation, and required legacy integration | Tested initial-release application components |
| 5. Data migration and security | Map and migrate required account data; implement and review security controls | Validated migrated data and security controls |
| 6. Testing and deployment | Perform functional, integration, security, and deployment testing; prepare operational handoff | Test results, deployment, backup and recovery procedures |
| 7. Project closeout | Obtain acceptance, complete documentation, transfer responsibilities, and record lessons learned | Acceptance record, operational documentation, closeout report |

## Schedule and Milestones

The project is planned to run from October 1 through December 30. Several activities overlap to support the delivery target.

![Project Gantt Chart](frosmear_gantt.png)

| Project phase | Duration | Start | Completion | Major milestone or deliverable |
|---|---|---|---|---|
| 1. Planning | 2 weeks | October 1, 2026 | October 16, 2026 | Project charter, scope, budget, schedule, stakeholder plan |
| 2. Current-system assessment | 2 weeks | October 12, 2026 | October 23, 2026 | Legacy inventory, requirements, migration assessment, compatibility review |
| 3. Architecture and environments | 2 weeks | October 19, 2026 | October 30, 2026 | Docker/Django/MySQL architecture, environment standards, security requirements |
| 4. Application development | 4 weeks | October 19, 2026 | November 20, 2026 | Authentication, permissions, application menu, legacy integration |
| 5. Data migration and security | 3 weeks | November 2, 2026 | December 4, 2026 | Migrated accounts, provisioning, compatibility validation, security controls, backup and recovery procedures |
| 6. Testing and deployment | 2 weeks | November 23, 2026 | December 18, 2026 | Functional, security, and integration testing; deployment; operational handoff |
| 7. Project closeout | 2 weeks | December 7, 2026 | December 30, 2026 | Acceptance, documentation, lessons learned, maintenance plan |

## Budget and Resource Allocation

The preliminary project budget is $210,000. This hypothetical corporate estimate assumes an experienced team, coordinated parallel work, and a defined initial release. It is a planning estimate rather than an approved budget or vendor quotation.

| Budget category | Estimated cost |
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
| **Total estimated budget** | **$210,000** |

The contingency reserve is intended for approved responses to unforeseen risks, including legacy dependencies, migration problems, or additional testing. It is not an automatic spending allowance. The project manager and CFO will validate staffing assumptions, labor rates, hosting expenses, software costs, and vendor charges before finalizing the budget. Infrastructure planning will include capacity, availability, power and cooling considerations, operational support, and the costs of maintaining the hosting environment, consistent with the project-management concerns associated with data-center projects (Rasmussen & Niles, 2019).

### Project Resources and Responsibilities

| Stakeholder | Role and responsibilities |
|---|---|
| Glenda Schumann, CEO | Executive sponsorship, strategic direction, and major decisions. |
| Zelda Hudson, CTO | Technical leadership, architecture, and resolution of technical blockers. |
| Theresa Hudson, CFO | Budget oversight, cost tracking, and financial analysis. |
| Gordie Roberts, Director of Operations | Operational readiness, deployment coordination, and service continuity. |
| Jay Caufield, Legacy Systems Manager and LAME lead | Legacy knowledge, PHP compatibility, and migration support. |
| Jim Paek, Lead Django/Darfcloud Developer | Application implementation, integration, and technical quality. |
| Grant Jennings, Information Security Manager and PITA lead | Security architecture, threat assessments, access controls, and security testing. |
| LAME and PITA team members | Legacy assessment, compatibility validation, security reviews, data integrity, and release readiness. |
| User representatives | Usability feedback, workflow validation, and acceptance testing. |
| Cloud-provider representatives | Hosting and infrastructure guidance as needed. |

## Stakeholder Management and Communications

Stakeholder engagement will reflect each participant's influence, interest, responsibilities, and required level of involvement. The project manager will compare current engagement with desired engagement and use targeted communication to address gaps.

![Stakeholder Listing](diagram.jpg)

### Stakeholder Engagement Levels

- **Unaware:** The stakeholder does not know the project exists.
- **Resistant:** The stakeholder does not want the project to succeed and may actively work against it.
- **Neutral:** The stakeholder is indifferent to the project's success or failure.
- **Supportive:** The stakeholder believes the project will provide benefits and wants it to succeed.
- **Leading:** The stakeholder actively participates in ensuring project success.

### Stakeholder Engagement Assessment Matrix

| Stakeholder | Unaware | Resistant | Neutral | Supportive | Leading |
| ----------- | ------- | --------- | ------- | ---------- | ------- |
| A           |         |           |         | C          | D       |
| B           |         |           |         |            | C,D     |
| C           |         |           | C       | D          |         |
| D           |         |           |         | C          | D       |
| E           |         | C         |         | D          |         |
| F           |         |           |         |            | C,D     |
| G           |         |           |         | C          | D       |
| H           |         |           |         | C,D        |         |
| I           |         |           | C,D     |            |         |
| J           |         |           | C       | D          |         |
| K           | C       |           |         | D          |         |
| L           | C       |           |         | D          |         |
| M           |         |           | C       | D          |         |

### Stakeholder Key

| Letter | Stakeholder       | Role                                    |
| ------ | ----------------- | --------------------------------------- |
| A      | Glenda Schumann   | CEO                                     |
| B      | Zelda Hudson      | CTO                                     |
| C      | Theresa Hudson    | CFO                                     |
| D      | Gordie Roberts    | Director of Operations                  |
| E      | Jay Caufield      | Legacy Systems Manager                  |
| F      | Jim Paek          | Lead Django/Darfcloud Developer         |
| G      | Grant Jennings    | Information Security Manager            |
| H      | Phil Bourque      | AWS Account Manager                     |
| I      | Jamie Leach       | Azure Account Manager                   |
| J      | Peter Taglianetti | Power-User Representative               |
| K      | Brad Aitken       | Casual-User Representative              |
| L      | Jeff Daniels      | Investment-Tool Customer Representative |
| M      | Troy Loney        | Shareholder Representative              |

Legend: C = Current engagement; D = Desired engagement.

The stakeholder names and assigned business roles are fictional characters created for this academic project. They do not represent actual involvement by the named individuals.

### Communication Plan

The project manager will use a combination of status reports, milestone reviews, demonstrations, issue escalation, and targeted stakeholder discussions.

| Audience | Information / communication | Purpose |
|---|---|---|
| CEO and steering stakeholders | Milestone status, major risks, decisions, and changes | Maintain sponsorship and timely executive decisions |
| CFO | Budget status, forecasts, variance, and change-cost assessments | Maintain financial oversight |
| CTO and technical leads | Architecture, dependencies, defects, and technical decisions | Coordinate technical work and resolve blockers |
| LAME and PITA | Compatibility findings, security requirements, test results, and unresolved issues | Coordinate legacy and security responsibilities |
| Operations | Deployment readiness, backups, recovery, monitoring, and support documentation | Prepare for operational ownership |
| User representatives | Demonstrations, workflow reviews, and acceptance testing | Validate usability and required functionality |
| Shareholder representative | Periodic progress, risk, financial performance, and expected value | Maintain visibility into project performance |

## Risk Management

Risk management will identify potential problems, evaluate their likelihood and impact, assign ownership, and establish appropriate responses. The project manager will coordinate regular risk reviews and update the risk register as conditions change.

### SWOT Analysis

![Project SWOT Analysis](frosmear_swot.png)

The SWOT analysis should be reviewed with stakeholders through document reviews, brainstorming, interviews, and assumptions analysis. Its findings should be compared against the work breakdown to identify missing activities, validate assumptions, and determine whether additional planning is necessary.

### Probability and Severity Matrix

The project uses a 3×3 matrix. Probability is classified as likely, possible, or unlikely. Severity is classified as negligible, moderate, or critical.

| Probability / Severity | Negligible | Moderate | Critical |
|---|---|---|---|
| Likely | Medium | High | High |
| Possible | Low | Medium | High |
| Unlikely | Low | Low | Medium |

![Project Risk Matrix](frosmear_risk_matrix.png)

### Project Risk Register

![Project Risk Register](frosmear_risk_register.png)

## Risk Responses and Monitoring

| ID | Response |
|---|---|
| R1 | Monitor legacy dependencies and integration results. Test compatibility incrementally and defer features that cannot be integrated on schedule. |
| R2 | Use test migrations, validate source data, preserve backups, and establish recovery procedures. Monitor migration accuracy and completeness. |
| R3 | Review authentication, authorization, and token security throughout development. Test the handoff and resolve critical vulnerabilities before release. |
| R4 | Monitor milestones, dependencies, and schedule variance. Address delays and defer nonessential features when necessary to protect the initial release. |
| R5 | Monitor security testing and remediation. Assign corrective work and repeat testing to verify that significant weaknesses are resolved. |
| R6 | Monitor critical equipment and replacement needs. Maintain an equipment inventory and arrange replacements through operational resources. |

The project manager will coordinate regular reviews, ensure risk owners provide updates, and escalate risks that threaten project objectives. Consistent identification, analysis, response planning, and monitoring help project teams address uncertainty before it threatens delivery (Association for Project Management, 2020; Thomas, n.d.). Risk responses should also reflect the organizational and project context (Maruping et al., 2019).

## Testing, Acceptance, and Deployment

Testing will verify that the initial release meets its functional, technical, security, and operational requirements. The project team will complete testing before production release and document results and unresolved issues.

Acceptance activities will include:

- Verification of required authentication and account-permission behavior.
- Validation of migrated account data.
- Testing of application navigation and agreed initial-release functionality.
- Integration testing between Darfcloud and required legacy components.
- Security testing of token handling, authorization, and access controls.
- Verification of database operations and data integrity.
- Deployment testing, including restart and recovery procedures.
- Review of application logs and resolution or formal acceptance of significant defects.
- User feedback and stakeholder acceptance.

## Maintenance and Project Closeout

After deployment and acceptance, operational responsibility will transfer to the designated Operations team. Initial stabilization and maintenance are expected to begin in January 2027 and continue through the first quarter.

Ongoing responsibilities will include system monitoring, security updates, backup verification, recovery testing, account administration, and incident response. LAME will provide legacy-system documentation and compatibility support. PITA will help establish security monitoring, incident escalation, access-control reviews, and periodic validation of security controls.

Closeout will include formal acceptance, technical and operational documentation, transfer of responsibilities, and a lessons-learned review. The project manager will document unresolved issues and recommendations for future development. Ongoing maintenance and 2027 enhancements will be managed separately from the initial implementation budget and schedule.

## Conclusion

The Frosmear Legacy Modernization project will establish Darfcloud as a maintainable application platform using Docker, Django, and MySQL. A hybrid management approach provides structure for the project's scope, schedule, budget, stakeholder responsibilities, and risk controls while allowing iterative development and feedback.

The project has a $210,000 preliminary budget, a December 23, 2026 target delivery date, and a December 30 closeout deadline. LAME will address legacy compatibility and migration dependencies, while PITA will focus on security and data integrity. Their involvement throughout the project will help the team identify technical concerns early and coordinate solutions before deployment.

The initial release will be successful when the agreed functionality is tested, accepted, deployed, and transferred to Operations with the documentation and procedures needed to maintain it. This will provide SHAT with a foundation for future Darfcloud applications and enhancements.

## References

Association for Project Management. (2020). What is risk management?

Maruping, L. M., Venkatesh, V., Thong, J. Y. L., & Zhang, X. (2019). A risk mitigation framework for information technology projects: A cultural contingency perspective. *Journal of Management Information Systems, 36*(1), 120–157. EBSCOhost article

Peters, L. A. (2002). Eight planning strategies for delivering quality projects. Project Management Institute. https://www.pmi.org/learning/library/planning-strategies-delivering-quality-projects-1052

Rasmussen, N., & Niles, S. (2019). Data center projects: Project management. Schneider Electric, Data Center Science Center. https://www.facilitiesnet.com/whitepapers/pdfs/APC_083011.pdf

Project Management Institute. (2017). *Agile practice guide*. https://www.pmi.org/shop/p-/book/agile-practice-guide-%28english%29/00101602301

Ross, R., & Pillitteri, V. (2020). *Security and privacy controls for information systems and organizations* (NIST Special Publication 800-53, Revision 5). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.SP.800-53r5

Thomas, C. (n.d.). Five steps of the risk management process in 2025. 360Factors.


