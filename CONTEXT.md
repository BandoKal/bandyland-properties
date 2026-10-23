# BandyLand Properties Workspace Context

Updated October 22, 2026. This reference summarizes the two supplied files for project execution. Source proposals are planning context, not proof of completed work, approved spending, signed agreements, or final owner decisions.

## Sources

- **Business plan:** [Goslin Branch Rental Business Plan](sources/Goslin_Branch_Rental_Business_Plan.docx), internally dated October 9, 2026. References use section names and appendix task numbers.
- **Budget:** [Bandy Budget](sources/Bandy_Budget.xlsx), containing Budget, Rental, BandyWorks, and Property Equipment sheets. Cached values and formulas were inspected without modifying the workbook.
- Earlier ChatGPT shares remain unread because login was required: [conversation 1](https://chatgpt.com/share/6ada6fce-d778-83e9-a263-f32d7dc6efe5), [conversation 2](https://chatgpt.com/share/6ada6ff8-e520-83ea-b414-e09a3e938647). No facts below rely on them.

The user clarified that the reserve should start with $9,000 and grow to $18,000 by retaining a portion of otherwise available owner draw. The split percentage is still pending. The workbook must distinguish initial funding from the eventual target and still needs the plan's startup estimates reconciled. Legal, tax, market, and equipment claims are source assertions, not independently revalidated advice.

## Objective and property

The plan proposes converting 948 Goslin Branch Road to a rental while retaining the existing mortgage. It describes three bedrooms, two bathrooms, approximately 2,327 square feet on 2.64 acres, a garage conversion, and a pool that will remain closed. Privacy, acreage, and finished space support the positioning; lack of a garage, grounds maintenance, and pool restrictions may limit demand. The goal is modest income, reserve building, and retaining the property for possible future appreciation.

The cited September 2026 mortgage balance is $167,603.73 at 4.250% fixed, maturing April 2047. The monthly payment is $1,343.71 including $313 escrow; approximately $437.11 of the cited payment reduces principal. The $659,000 value is a source reference, not a current appraisal. [Plan: Property and Debt Economics; mortgage table.]

## Unconfirmed decisions

1. Confirm the owner-draw retention percentage, startup costs, contingency and distribution rules, then reconcile the workbook. The user approved a $9,000 initial reserve and $18,000 target.
2. Choose a manager or deliberate first-lease self-management trial. The workbook assumes self-management but does not establish a signed decision.
3. Confirm project start, work already completed, owners, and capacity. October 22, 2026 is the proposed schedule anchor; no completion is inferred.
4. Record actual listing and lease dates. November 6 is a proposed marketing target after readiness, not a commitment.
5. Confirm scope. The prepared backlog includes rental, BandyWorks Phase 0, and property equipment as separate workstreams unless narrowed by the user.

## Rental economics

| Item | Source planning assumption |
| --- | --- |
| Opening rent | $3,595 monthly |
| Fallback rent | $3,195 monthly |
| Floor requiring a renewed decision below it | $2,995 monthly |
| Professional management | 9% of rent |
| Monthly reserve allocations | Vacancy 5%; routine repairs 8%; capital replacement 5%; turnover 4% |
| Fixed additional allowances | Insurance increase $125; closed pool $100; Fair Partnership $75 monthly |
| Fallback managed cash | $560.84 monthly |
| Fallback self-managed cash | $848.39 monthly before extra retention |
| Self-management ramp | Retain the avoided $287.55 management fee monthly for six months; remaining cash is $560.84 |

These are modeled outputs, not guaranteed income. Current insurance is partly included in escrow; replace the incremental $125 allowance with the confirmed change rather than adding the entire premium again. Keep startup funding separate from recurring rent-funded reserves. [Plan: Three Rent Scenarios, Two Management Paths; Rental!C24:C50.]

## Funding conflict requiring resolution

**Owner clarification:** $9,000 is the initial seed reserve; $18,000 is the long-term reserve target. A portion of otherwise available owner distributions will build the difference. Do not budget $18,000 as the initial contribution. The retention percentage, calculation timing and post-target/replenishment rules remain undecided. See `planning/funding-policy.md`.

| Item | Business plan | Workbook |
| --- | ---: | ---: |
| Core rental reserve | $9,000 | $18,000 |
| Identified startup work | $11,310 estimates | Unquoted; blank costs produce zero totals |
| Preparation allowance | $2,000 additional cushion | $2,000 reduced as quotes are entered |
| Rental funding | $22,310 | $20,000 cached total |

Plan startup estimates: release $500; legal review $660; tax/accounting $800; inspections $1,500; pool $2,800; repairs $2,500; cleaning/exterior $1,150; photos/marketing $350; initial utilities/insurance $450; other startup $600. These total $11,310, plus $2,000 preparation and $9,000 retained reserve. Replace estimates with quotes or invoices. [Plan: Startup Funding Before Lease Up.]

`Rental!C6` is `MAX(0,2000-SUM(E10:E19))`. Entering the plan's $11,310 costs and changing the reserve to $9,000 would therefore produce $20,310, not $22,310: the workbook consumes the cushion. Reconciliation must address both inputs and the allowance formula. The source workbook remains unchanged. [Rental!C4:C6, C9, E10:E19.]

Estimated RSU proceeds of $96,290 fund rental $20,000, BandyWorks $12,000, property equipment $20,000, and residual emergency cash $44,290. The $26,000 emergency reference is described as three months of stated $4,000 biweekly income, not a verified household expense reserve. Confirm actual net proceeds and the appropriate emergency target. Substituting rental funding of $22,310 with all else unchanged gives a calculated $41,980 emergency residual, $15,980 above the reference. This illustration is not an approved revision. [Budget!B5:B16.]

## Accounts and distributions

The revised plan calls for a property operating/reserve account, a separate insured tenant-deposit account, and monthly bookkeeping. Tenant deposits cannot count as reserves, income, or benefit funding. The preferred reserve is $9,000 before lease signing. The alternative begins with at least $6,000: below $6,000, no distributions; from $6,000–$8,999, no more than $200 monthly after obligations and known 90-day costs; at $9,000 or above, eligible excess may be distributed quarterly after funding known 90-day expenses. Late rent, an insurance claim, a repair above $1,000, or a reserve shortfall stops distributions. Confirm this policy against the conflicting workbook before adopting it. [Plan: Reserve Before Income; appendix Task 3.]

## Rental launch prerequisites

- **Brokerage:** the plan reports an exclusive sale listing with Realty Executives Hometown Living through December 31, 2026 and Amanda Anderson as designated agent. Obtain a signed release/amendment, costs, prior-buyer/protection terms, surviving fee rights, advertising removal, and sign/lockbox arrangements before advertising for rent. A withdrawn online listing alone is insufficient. [Existing Listing Agreement; appendix Task 1.]
- **Coverage and lender:** confirm landlord coverage, vacant-period coverage, effective dates, pool conditions, vendor scope, servicer instructions, lender requirements, and escrow change. [Appendix Task 2.]
- **Operations:** establish accounts, reserve funding, ledger, verified autopay transition, primary/backup owner, emergency method, vendors, and rental platform. Compare two management proposals including placement, renewal, repair, inspection, and tenant-program fees. [Appendix Tasks 3–4.]
- **Tax records:** collect closing and improvement records and have an adviser establish conversion-date value, building/land allocation, rental start, depreciation, and later-sale planning dates. Actual residence dates are needed before calculating any sale deadline. [Tax Treatment and Implementation; appendix Task 5.]
- **Readiness:** inspect alarms, locks, rails, electrical, plumbing, water heater, HVAC, appliances, septic, pests, drainage, trees, and pool. Classify repairs, obtain quotes, complete work/cleanup, and retain invoices, sign-offs, and dated photos. [Appendix Task 6.]
- **Lease:** obtain professional review of consistent screening, business terms, lawn and closed-pool clauses, optional services, tenant benefits, notices, deposit handling, and move-in records; configure the platform. [Appendix Task 7.]

Source checklists do not authorize the agent to sign, spend, transfer funds, contact third parties, or choose tenants. Such actions remain distinct from the user's request to organize the project.

## Marketing and placement

After prerequisites, publish complete terms, professional photos, a floor plan if available, and broad distribution at $3,595. Log qualified inquiries, showings, applications, and feedback. Review after seven days; no automatic cut solely because a lease is unsigned. At day 14, moving to $3,195 requires no complete application and local comparison or repeated qualified feedback identifying price as the obstacle. Allow at least seven days at fallback. Below $2,995 requires both owners to revisit holding versus selling. Screening criteria stay consistent. [Plan: How and When to Change the Asking Rent; appendix Task 8.]

Before possession, complete screening, signed lease/addenda, cleared funds in correct accounts, insurance evidence, utilities, notices, condition report/photos, key log, and scheduled inspection. Keep applicant personal and screening records in the approved rental system rather than issue bodies. [Appendix Task 9.]

## Optional services and tenant benefits

Base terms assign routine lawn care, trash arrangements, and interior cleanliness to the tenant. Optional lawn, trash, cleaning, pest, or filter services need written quotes, a dependable vendor schedule, and an addendum; source pricing is cost plus 10%–15%. Pool access remains unavailable unless the insurer and pool professional approve a separate plan. [Optional Lease Services.]

The proposed Fair Partnership program budgets $75 monthly/$900 annually for $75 quarterly credits (up to $300 yearly), a $400 annual capital/renewal benefit, an owner-funded bonus of 3% of the original deposit, and $104 yearly for rent reporting. Reporting requires voluntary consent, privacy, correction/dispute procedures, and no promised score increase. Benefits confer no ownership and never draw on the security deposit. Ordinary wear and good-faith repair reporting do not disqualify tenants. Review cash-bonus tax treatment and evaluate the program after the first year. [Fair Partnership Credit and Capital Program.]

Check the actual deposit and platform fee: maximum benefits total $899.85 with a $3,195 deposit, but $911.85 with a $3,595 deposit, exceeding the $900 allowance. Deposit equal to rent is only an illustration, not a confirmed lease term.

## BandyWorks Phase 0

Budget ceiling $12,000; listed subtotal $8,930.42; remaining installation/cost buffer $3,069.58. Tax/freight are blank and prices are snapshots. Scope includes xTool P2S laser, saw/stand, drill press, candidate wet tile saw, benches/carts/storage, exhaust, dust collection, stone containment, existing K1 Max supplies, stone/acrylic/wood/brass/packaging prototypes, electrical/lighting, fire protection, and software. The printer is already owned. UV laser/CNC and the earlier $27,000 plan are excluded. Confirm suitability, airflow, whole-system filtration, electrical work, installation, and the unpriced operating reserve before purchases. [BandyWorks!A9:H59.]

## Property equipment

Combined $20,000 allowance covers mower, woods vehicle, small box trailer, accessories, safety/storage, and initial maintenance. Costs are unquoted; zero formula outputs do not mean free purchases. Confirm requirements, compatibility, delivered cost, and combined spending before buying. [Property Equipment!A4:F28.]

## Execution references

The user created and selected [BandyLand project 7](https://github.com/users/BandoKal/projects/7/views/2) as the active project. Its project collection returns all 43 issues. It supersedes project 5 for ongoing work and the daily list. Issue F01 is being worked through interactively: the $9,000 seed and $18,000 target are confirmed; the draw-retention percentage, startup scope, contingency and detailed distribution rules remain pending.

- `planning/tasks.json`: prepared issue definitions, proposed dates, dependencies, sources, and completion checklists.
- `TASKS.md`: readable schedule, including event-based operations.
- `DAILY_TODO.md`: today's list with source freshness explicitly stated.
- `planning/github-project.json`: destination and publication state; blank IDs mean setup is incomplete.

After publication, GitHub becomes the task-status authority. Rebase dates on actual listing, fallback, and lease events instead of assuming target events occurred.
