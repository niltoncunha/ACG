# ACG Session Protocol

This protocol defines how a user interacts with an AI assistant after running ACG Structure Scout.

The user should not need to know which prompt to write next.

ACG should guide the session.

---

## User-Level Rule

The user only needs to provide:

```txt
I have this folder. Run ACG and tell me the safest next step.
```

or, after ACG has already generated `.acg/`:

```txt
Open .acg/ACG_MASTER.md and follow it exactly.
```

Everything else should be derived from ACG artifacts.

---

## Universal Interaction Loop

```txt
[00] User points to folder
       ↓
[01] ACG scans and writes .acg/
       ↓
[02] AI opens ACG_MASTER.md
       ↓
[03] AI reads required artifacts
       ↓
[04] AI reads only phase1_pack/
       ↓
[05] AI returns confirmation
       ↓
[06] AI proposes Phase 2 plan
       ↓
[07] Human approves or rejects
       ↓
[08] AI reads approved Phase 2 only
       ↓
[09] AI proposes bounded next action
       ↓
[10] Human approves execution or requests another map
```

---

## Required AI Behavior

The AI must not ask the user to invent technical prompts.

After reading `ACG_MASTER.md`, the AI must produce:

```txt
ACG-UNDERSTOOD: structure-scout
SCOPE: files actually read
RISKS: key risks before deeper processing
QUESTIONS: objective human approvals needed
NEXT: proposed bounded next step
```

If the user does not know what to do, the AI must choose the next safe ACG step, not ask an open-ended question.

---

## Generic Questions the AI Should Ask

These questions work for any codebase or file bundle.

### 1. Objective

```txt
What is the user's intended outcome?
```

Allowed answer classes:

```txt
understand
organize
refactor
debug
document
test
audit
migrate
extract
unknown
```

If the user does not know, default to:

```txt
understand + organize
```

### 2. Risk Zone

```txt
Which areas should remain untouched unless explicitly approved?
```

Default forbidden zones:

```txt
secrets
environment files
production config
infrastructure
migrations
database files
large exports
logs
archives
vendor/generated files
```

### 3. First Safe Step

```txt
What is the next smallest useful action?
```

Default:

```txt
Produce Phase 2 Reading Plan only.
Do not read new files yet.
```

### 4. Verification

```txt
How will success be checked outside the AI?
```

Default:

```txt
No promotion until external commands, human review, or CI evidence exists.
```

---

## Default Safe Mode

If the user gives no clear goal, ACG must default to:

```txt
Mode: orientation
Action: map and organize only
Edits: forbidden
Terminal assets: search-only
Next output: Phase 2 Reading Plan
```

The AI should not proceed to edits, refactors, migrations, or cleanup until the user approves a bounded plan.

---

## Phase 2 Plan Template

After Phase 1, the AI should automatically propose this without requiring the user to invent it:

```txt
## ACG Phase 2 Reading Plan

1. Exact files requested for Phase 2
2. Why each file is needed
3. What question each file should answer
4. Files explicitly excluded
5. Search-only or terminal assets that must remain closed
6. Human approvals needed
7. Stop and wait for approval
```

---

## Execution Template

Only after the human approves a bounded plan:

```txt
Approved for Phase 2 reading only.
Read only the approved list.
Do not open terminal/search-only assets.
Do not edit files.
Return what changed in your understanding and the next bounded recommendation.
```

---

## Non-Expert User Contract

ACG should assume the user may not know:

- how to prompt an AI;
- what files are safe;
- what files are dangerous;
- how to evaluate a codebase;
- how to judge whether the AI is hallucinating;
- how to know if a task is too broad.

Therefore ACG must provide:

```txt
single entrypoint
read order
forbidden zones
next safe action
approval points
evidence requirements
```

The method fails if it requires the user to be an expert prompt engineer.

---

## Principle

ACG is not just a file scanner.

ACG is a guided operating protocol for AI work over large projects.

The user should drive intent.
ACG should drive process.
The AI should follow the process.
