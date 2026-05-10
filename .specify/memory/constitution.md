<!--
SYNC IMPACT REPORT
==================
Version change: (template) → 1.0.0
Bump rationale: Initial seed of the constitution from the shared base
template at `../../.spec-kit-shared/constitution-base.md`. Project-specific
principles still need to be filled in (see placeholder sections below).
The "Spec Lifecycle" section is adopted verbatim from the shared base.

Modified principles: none

Added sections:
- Core Principles (placeholders)
- Operational Constraints
- Development Workflow & Quality Gates
- Spec Lifecycle
- Governance

Removed sections: none

Templates requiring updates:
- ✅ N/A — initial seed; downstream templates not yet affected.

Follow-up TODOs:
- Replace the placeholder principles (`### I. [PRINCIPLE_NAME]`, etc.) with
  the project's real, non-negotiable rules.
-->

# vps-uploader Constitution

> **Note**: This file was seeded from the shared base constitution template
> at `../../.spec-kit-shared/constitution-base.md`. Adapt the placeholder
> principles to the project's real, non-negotiable rules. The "Spec
> Lifecycle" section is intentionally identical across projects — keep it
> verbatim.

## Core Principles

### I. [PRINCIPLE_NAME]

[PRINCIPLE_DESCRIPTION — what the rule is, what it forbids/requires.]

**Rationale**: [Why this rule exists in concrete user/maintainer terms.]

### II. [PRINCIPLE_NAME]

[PRINCIPLE_DESCRIPTION]

**Rationale**: [Why.]

### III. [PRINCIPLE_NAME]

[PRINCIPLE_DESCRIPTION]

**Rationale**: [Why.]

### IV. [PRINCIPLE_NAME]

[PRINCIPLE_DESCRIPTION]

**Rationale**: [Why.]

### V. [PRINCIPLE_NAME]

[PRINCIPLE_DESCRIPTION]

**Rationale**: [Why.]

## Operational Constraints

[Technology stack constraints, deployment topology, storage choices,
auth model, cost limits, OS targets, or any other non-negotiable
operational rule. Replace this paragraph with concrete bullet points.]

## Development Workflow & Quality Gates

- **Spec-Kit flow is mandatory**: Every non-trivial feature MUST go through
  `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` →
  `/speckit-implement`. Bug fixes and trivial tweaks MAY skip the flow.
- **Constitution Check gate**: `/speckit-plan` MUST include a Constitution
  Check section that explicitly evaluates the plan against each principle
  above. Violations MUST be either resolved or recorded in the plan's
  Complexity Tracking table with a justification.
- **Test-first enforcement**: For any task touching logic the project
  marks as critical (e.g. orchestration, payments, data integrity), the
  task list MUST schedule the failing test before the implementation task.
- **PR review discipline**: Every PR MUST be reviewed against this
  constitution. Reviewers MUST reject changes that silently violate a
  principle without an accepted deviation in the plan.

## Spec Lifecycle

Every `specs/<NNN>-*/spec.md` MUST carry a `**Status**` field whose value is
one of the following, and only one:

- **`Draft`** — initial state. The spec is being written or clarified;
  `/speckit-plan` MUST NOT be run against it yet.
- **`Ready`** — the spec is frozen and ready for `/speckit-plan`. No further
  scope changes are expected without bumping back to `Draft`.
- **`In Progress`** — `/speckit-plan` and/or `/speckit-tasks` have produced
  artifacts and implementation has started. `tasks.md` has at least one
  checked task.
- **`Blocked: <reason>`** — work is paused. The reason MUST be a short
  inline string (e.g. `Blocked: waiting on upstream API`); no trailing
  prose. Specs in this state MUST be revisited before any new feature is
  started by the same maintainer.
- **`Done (YYYY-MM-DD)`** — implementation merged to `main` and verified.
  The date is the merge date, not the spec creation date.
- **`Abandoned (YYYY-MM-DD)`** — the spec was dropped without being
  implemented. Kept for history; MUST NOT be deleted.

**Transition rules**:

- Status changes MUST be committed in the same commit that reflects the
  underlying state change (e.g. the merge commit for `Done`, the
  `/speckit-plan` commit for `In Progress`).
- Skipping forward is allowed (`Draft` → `Done` for trivial specs) but
  skipping backward (e.g. `Done` → `Draft`) requires a new spec number; the
  old one stays in `Done` or transitions to `Abandoned`.
- If the project surfaces a specs index (e.g. an auto-synced section in the
  README), that index MUST reflect the allowed values defined here; any
  change to this list MUST be propagated to the indexer.

**Rationale**: Without a fixed vocabulary, status drifts into ad-hoc
free-form strings ("WIP", "todo", "shipped", empty) that defeat the
README sync and make the specs index unreadable. A small closed set keeps
the surface scannable at a glance.

## Governance

This constitution supersedes ad-hoc practices and informal conventions.
When a tension arises between this document and a specific plan, the
constitution wins unless the plan documents an explicit, justified
deviation in its Complexity Tracking table.

**Amendment procedure**: Amendments are made by editing
`.specify/memory/constitution.md` via a pull request that (a) describes the
change, (b) bumps the version per the policy below, and (c) updates the
Sync Impact Report comment at the top of the file. Breaking changes (MAJOR
bumps) MUST include a migration note for affected in-flight features.

**Versioning policy** (semantic versioning applied to governance):

- **MAJOR**: A principle is removed, redefined in a way that invalidates
  prior compliance, or replaced.
- **MINOR**: A new principle or section is added, or an existing principle
  is materially expanded.
- **PATCH**: Wording, clarifications, typo fixes, or non-semantic
  refinements.

**Compliance review**: Every PR review MUST confirm the change does not
violate the constitution. The reviewer's approval is implicit confirmation
of compliance; explicit notes are required only when a deviation is being
accepted.

**Version**: 1.0.0 | **Ratified**: 2026-05-10 | **Last Amended**: 2026-05-10
