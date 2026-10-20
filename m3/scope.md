# Scope Management – 3D Printer Webpage Development

Schumann Hudson Acquisition & Technology (SHAT) has been hired by a 3D printing company to manage the development and deployment of a customer-facing webpage showcasing its 3D printers, filaments, and spools. The project needs clearly defined boundaries because requests for online ordering, customer accounts, and product reviews could significantly expand the scope. We must establish what the client will receive while allowing flexibility during development.

## Scope Management Process

We will begin by working with the client to define requirements for product descriptions, images, specifications, navigation, search, and responsive design. The team will document assumptions, constraints, exclusions, and acceptance criteria in a scope statement. A work breakdown structure (WBS) will divide the work into manageable deliverables, including design, product content, development, security testing, and deployment. These practices support the project management principles of tailoring the approach to the project and focusing on its intended outcomes (Project Management Institute [PMI], 2021).

Inputs will include the project charter, stakeholder requirements, existing product information, organizational policies, and technical constraints. Tools and techniques will include stakeholder interviews, requirements workshops, prototypes, and decomposition of deliverables. Outputs will include the scope statement, requirements documentation, WBS, scope baseline, and acceptance criteria. Requests for additional features will be documented, evaluated for their impacts on cost and schedule, and prioritized rather than automatically added to the project.

My experience with the Darfcloud modernization project demonstrates why identifying dependencies matters. We recently completed a sprint that backported authentication to the legacy Frosmear application. The task appeared relatively contained, but it highlighted dependencies involving existing accounts, permissions, and the complexities of user migration. Those lessons reinforced the value of evaluating how a change affects surrounding systems before planning the next increment. We would apply the same approach by identifying dependencies early and revisiting the plan as new information emerges.

## Project Lifecycle and Development Approach

An iterative, agile approach would allow us to deliver working portions of the website and gather client feedback throughout development. Initial planning would establish the requirements and product backlog. The first sprint could deliver the basic site structure and navigation, while later sprints could add product pages, responsive layouts, search functionality, and content. Sprint reviews would allow stakeholders to identify problems before they become expensive to correct.

A project management platform would track requirements and tasks, while Git would manage source code. Automated tests and a staging environment would help verify changes before production deployment. Each feature would have measurable acceptance criteria, and the team would review the remaining scope, dependencies, and priorities at the end of each sprint.

## Security and Deployment Considerations

Security must be part of the scope from the beginning. We will recommend HTTPS, least-privilege access, secure administrative authentication, and protection against common web vulnerabilities. The team will review and document firewall rules, network configurations, certificates, and patching procedures for the client's infrastructure. Documented network design and configuration practices can help reduce avoidable infrastructure problems (Cisco, 2024).

The deployment plan will include development, testing, staging, and production environments. The team will test functionality, browser compatibility, performance, and security before release. Backups, monitoring, documented configurations, and a rollback procedure should be in place before production changes begin. Secure development practices should be integrated throughout the lifecycle rather than postponed until release (Souppaya et al., 2022).

## Conclusion

Effective scope management will help us deliver the webpage without allowing uncontrolled feature requests to expand the project. Agile development provides flexibility through short iterations and stakeholder feedback, while a scope baseline, acceptance criteria, and change management maintain accountability. Lessons from the Frosmear authentication sprint reinforce that even small features can expose dependencies affecting later work. Applying that lesson will help us deliver a secure, functional website within the agreed scope.

## References

Cisco. (2024, August 27). *Cisco cloud campus LAN design guide*. https://www.cisco.com/c/en/us/solutions/collateral/enterprise/design-zone-campus/cloud-campus-lan-design-guide.html

Project Management Institute. (2021). *A guide to the project management body of knowledge (PMBOK® guide)* (7th ed.).

Souppaya, M., Scarfone, K., & Dodson, D. (2022). *Secure software development framework (SSDF) version 1.1: Recommendations for mitigating the risk of software vulnerabilities (NIST SP 800-218).* National Institute of Standards and Technology. https://doi.org/10.6028/NIST.SP.800-218
