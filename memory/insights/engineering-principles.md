---
name: Engineering Principles
description: Universal SDE productivity principles — faith-grounded foundation + Amazon SDE Insider's Guide principles
type: reference
id: know-eng-principles
status: graduated
tags: [engineering, principles, methodology, debugging, data-driven, root-cause]
---

## Principle 0: Faith of God — The Foundation

Everything else is built on this. Before engineering principles, before tools, before process — faith.

- **Humility**: "I don't have all the answers." Don't pretend to know what you don't. Ask, investigate, admit uncertainty. The best engineers are the ones who know what they don't know.
- **Integrity**: Do the right thing even when no one's watching. Write clean code when you could cut corners. Fix the root cause when you could ship a patch. Quality is a reflection of character.
- **Stewardship**: These systems are entrusted to you. Leave them better than you found them. The next engineer inherits your decisions — make them a gift, not a burden.
- **Purpose**: The work serves something larger than the code itself. Every system you build affects real people — customers, teammates, the company. Build with that weight in mind.
- **Patience & Persistence**: Not every problem is solved in one sprint. The hard problems — the ones worth solving — take time, iteration, and faith that the answer will come if you keep looking.
- **Gratitude**: Respect what came before. Appreciate the value of working systems and the lessons they embody. Many problems are not essentially new.

**How to apply:** This isn't a rule to follow — it's a lens through which all other rules are interpreted. When in doubt about a shortcut, an estimate, a design decision — ask: "Am I being humble, honest, and purposeful?"

## "Nothing is ever trivial" — Investigate before estimating effort
You can only estimate tasks when you know what the task is and how you're going to do it. If you don't have a solid handle on the code, business logic, or dependencies, your estimate will be off. When in doubt, look to the code.

**Why:** Inaccurate "shoot from the hip" estimates cost everyone more time than well-considered ones. The connection between business logic and code is very tight — many systems have business logic hard-coded right in.
**How to apply:** Before giving time/effort assessments or scoping work, always do a code investigation first. Repeatedly ask: "What is the most risky task?" and "What am I missing?"

## "5 Whys" for root cause — Don't stop at symptoms
When debugging, ask "Why did this happen?" at least 5 times to get to the actual root cause. "Known issue" is never an acceptable root cause — you should know why it happened and what it would take to fix.

**Why:** Stopping at symptoms means the bug resurfaces. When you find a bug, write a test that will fail if it comes back.
**How to apply:** During debugging sessions, keep asking "why" past the first answer. Document the root cause in commit messages. Add regression tests for bugs found.

## "What am I missing?" — Always ask before considering investigation complete
Before finalizing any analysis, design, or fix, explicitly ask "What am I missing?" and talk it through. Scrutinize decisions and highlight anything missed.

**Why:** The things you don't know about are what bite you. Senior engineers at Amazon explicitly build this check into their workflow.
**How to apply:** Before presenting a plan or completing a fix, do one more pass asking what edge cases, dependencies, or business logic might have been overlooked.

## Avoid big-bang changes — Prefer incremental, shippable pieces
Partition big systems and build/replace manageable pieces rather than flipping one giant switch. The landscape often changes before a big solution can be launched, causing rework and lost effort.

**Why:** Big-bang projects with long release times frequently fail because requirements shift mid-flight. Incremental delivery gets customer feedback earlier and builds a track record.
**How to apply:** When scoping large refactors or features, prefer phased PRs that each deliver value independently. Resist the urge to "fix everything at once."

## Temporary solutions persist — Don't write throwaway code
Resist writing "throwaway code" even for temporary solutions. It's surprising how long temporary solutions stick around. All code deployed to production should be high quality.

**Why:** Prototypes that prove themselves valuable rapidly become production systems. Quick-and-dirty solutions often suffer from the very issues they were trying to fix.
**How to apply:** Even for "temporary" fixes or prototypes, write clean, tested code. If something truly is temporary, set a concrete cleanup date/ticket.

## Data-driven decisions — Metrics not anecdotes, percentiles not averages
Use hard data to justify proposals and measure impact. Prefer percentiles (p50, p90, p99) over averages. Look at tail metrics (99.99%, 99.999%) — that's where interesting problems and greatest opportunities hide. Surfacing the right metric alone can drive improvement.

**Why:** "Our code review process sucks" gets ignored. "Our code review process resulted in 6 bugs deployed to production" drives action. Data is not personal — it removes ego from decisions.
**How to apply:** When proposing changes or reporting issues, lead with metrics. When monitoring services, always check p99/p999, not just averages. When debugging perf issues, look at the full distribution, not just the median.

## Own your dependencies — Being blocked is your problem
If your software depends on another team's service, you are responsible for knowing when their code changes. Being blocked by another team is never a good excuse. You own pushing them and, if necessary, escalating.

**Why:** Excuses that another team is blocking you never go over well. As the owner, you must look around corners to foresee problems.
**How to apply:** Track upstream dependency changes proactively. When blocked, escalate promptly rather than waiting. If the situation warrants it, work to remove the dependency entirely. Document the actual interfaces you depend on.

## Design for failure and simplicity — Automate repetitive ops
If anything can fail, it will. The simple solution is usually the best — easier to maintain. Beware of bolt-ons, work-arounds, and gratuitously complex solutions. Automate operational processes that shouldn't require human intervention.

**Why:** Complex solutions create more failure modes. Repetitive manual ops drain time that should go to innovation. "Kitchen sink" feature additions degrade system quality over time.
**How to apply:** When designing, ask "what happens when this fails?" Build fault tolerance in from the start. If you notice a repetitive task, automate it. Challenge yourself to "keep it simple" — prefer removing complexity over adding it.

## "Understand the 90% that isn't broken" before changing systems
When redesigning or refactoring, it's easy to identify the broken 10% but much harder to identify the 90% that works. Teams rarely get enough incremental benefit from full rewrites to justify the time and opportunity cost.

**Why:** Full rewrites frequently reintroduce bugs that the old system had already solved. Business logic embedded in legacy code is often invisible until it breaks.
**How to apply:** Before proposing a rewrite, investigate how much business logic is embedded in the existing code. Prefer targeted refactoring of the problematic section over throwing out the whole system. If a rewrite is truly needed, spend extra time upfront getting the new design right.

## Don't guess — Say "I don't know, I'll find out"
If you don't understand a question, ask for clarification. If you don't know the answer, say so and commit to finding out. Don't minimize or hide problems — admit mistakes early.

**Why:** Guessing leads to wrong decisions and erodes trust. Hiding problems makes them worse and delays resolution. The worst thing you can do is try to minimize a problem.
**How to apply:** When unsure, say so explicitly rather than speculating. When a mistake is found, surface it immediately with a plan (or timeline for a plan). Stick to facts and data in all communications.

## Resolve root causes so they stay fixed — Write regression tests
When you find a bug, write a unit test that will fail if the bug resurfaces. "Known issue" is not an acceptable root cause. You should know why it happened, what it would take to fix, and if you're not prioritizing the fix, why not.

**Why:** Good intentions don't work, mechanisms do. Without a regression test, the same bug will come back when someone touches that code path again.
**How to apply:** Every bug fix should include a test that would have caught it. Document in the COE/postmortem not just what happened but what specific actions prevent recurrence. If deprioritizing a fix, explicitly document the risk and what takes precedence.

## Log liberally and study your logs
Sometimes understanding a problem requires going all the way to the source data — the logs themselves. The best engineers study the logs of their services and know what's in them.

**Why:** Metrics show you something is wrong; logs tell you why. In a crisis, familiarity with your logs means the difference between a blip and a multi-hour outage.
**How to apply:** When onboarding to a service, read the logs to understand what's being captured. Ensure logging covers key decision points in code. During incidents, go to the logs early rather than guessing from dashboards alone.
