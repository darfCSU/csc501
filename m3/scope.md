# Scope Management – 3D Printer Webpage Development

Schumann Hudson Acquisition & Technology (SHAT) has been hired to develop and deploy a customer-facing webpage showcasing a 3D printing company's printers, filaments, and spools. The project needs clear boundaries because requests for online ordering, customer accounts, or product reviews could expand the scope. We must define what the client will receive and how changes will be evaluated.

## Scope Management Process

The team will begin by working with the client to define requirements for product descriptions, images, specifications, navigation, search, and responsive design. The team will document assumptions, constraints, exclusions, and acceptance criteria in a scope statement. A work breakdown structure (WBS) will divide the work into manageable deliverables, including design, product content, development, security testing, and deployment. These practices support the project management principles of tailoring the approach to the project and focusing on its intended outcomes (Project Management Institute [PMI], 2021).

Inputs will include the project charter, stakeholder requirements, existing product information, organizational policies, and technical constraints. Tools and techniques will include stakeholder interviews, requirements workshops, prototypes, and decomposition of deliverables. Outputs will include the scope statement, requirements documentation, WBS, scope baseline, and acceptance criteria. Requests for additional features will be documented, evaluated for their impacts on cost and schedule, and prioritized rather than automatically added to the project.

The experience with the Darfcloud modernization project demonstrated why identifying dependencies matters. We recently completed a sprint that backported authentication to the legacy Frosmear application. The task appeared relatively straightforward, but it highlighted dependencies involving existing accounts, permissions, and the complexities of user migration. Those lessons reinforced the value of evaluating how a change affects surrounding systems before planning the next increment. We would apply the same approach by identifying dependencies early and revisiting the plan as new information emerges.

## Project Lifecycle and Development Approach

An iterative, agile approach would allow the team to deliver working features and gather feedback throughout development. Planning would establish requirements, priorities, and a product backlog. The first sprint could deliver the basic layout and navigation; later sprints could add product pages, responsive design, and search. Sprint reviews would give stakeholders opportunities to identify problems before they become expensive to fix.

A project management platform would track tasks and requirements, while Git would manage source code. Automated tests and a staging environment would help verify changes before production deployment. Each feature would have measurable acceptance criteria, and the team would review priorities, dependencies, and remaining scope at the end of each sprint.

## Security and Deployment Considerations

Security requirements must be included in the scope from the beginning. The team should implement HTTPS, least-privilege access, secure administrative authentication, and protections against common web vulnerabilities. It should review firewall rules, network configuration, certificates, and patching procedures. Documented network design and configuration practices help reduce infrastructure risks (Cisco, 2024).

Deployment should use separate development, testing, staging, and production environments. Before release, the team will test functionality, browser compatibility, performance, and security. Backups, monitoring, documented configurations, and a rollback procedure should be ready before deployment. Secure development practices should be integrated throughout the lifecycle rather than postponed until release (Souppaya et al., 2022).

## Conclusion

Effective scope management will deliver a secure, functional webpage without uncontrolled feature growth. Agile iterations allow flexibility, while the scope baseline, acceptance criteria, and change control keep the project accountable. The Darfcloud authentication sprint demonstrated that even small changes can affect surrounding systems. Applying that lesson will help the team manage dependencies and deliver the agreed product.

## References

Cisco. (2024, August 27). *Cisco cloud campus LAN design guide*. https://www.cisco.com/c/en/us/solutions/collateral/enterprise/design-zone-campus/cloud-campus-lan-design-guide.html

Project Management Institute. (2021). *A guide to the project management body of knowledge (PMBOK® guide)* (7th ed.).

Souppaya, M., Scarfone, K., & Dodson, D. (2022). *Secure software development framework (SSDF) version 1.1: Recommendations for mitigating the risk of software vulnerabilities* (NIST SP 800-218). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.SP.800-218
