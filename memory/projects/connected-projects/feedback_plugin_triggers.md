---
name: Plugin Auto-Trigger Rules
description: When to proactively invoke underused LinkedIn plugin skills (linkedin-frameworks, kafka-flink, library-specs, mp-rules, plugin-creator) during work
type: feedback
originSessionId: df52b556-67f3-4c28-b4ca-b09ad66f7f19
---
Proactively invoke these plugin skills in the right context — don't wait for the user to ask.

## Trigger Rules

### kafka-flink (linkedin-framework)
- **When**: Touching Kafka consumers, TrackerProcessor, topic configs, Samza/nearline processors in hp-ats-integration-mt
- **How**: Invoke `kafka-flink` skill before implementing to check patterns
- **Why**: hp-ats-integration-mt is heavily Kafka-based; framework guidance prevents infra mistakes

### linkedin-frameworks (linkedin-framework)
- **When**: Adding new Offspring factories, boot listeners, D2 client wiring, Rest.li resources, or DI patterns
- **How**: Invoke `linkedin-frameworks` skill to check correct patterns
- **Why**: Offspring/D2/Rest.li have LinkedIn-specific conventions that differ from standard Spring/gRPC patterns

### library-specs (spec-generation / fix)
- **When**: Adding or bumping dependencies in `product-spec.json`, or hitting version set conflicts during `mint build`
- **How**: Invoke `library-specs:spec-generation` for new deps, `library-specs:fix` for version conflicts
- **Why**: Specs document correct usage; version conflicts are common and have known resolution patterns

### copy-rule-file / unignore-file (mp-rules)
- **When**: Creating new MP modules, modifying `.gitignore`, or needing build rule customization
- **How**: Invoke the relevant mp-rules skill
- **Why**: MP rules have specific conventions; wrong rules cause hard-to-debug build failures

### linkedin-plugin-creator:plugin-creation
- **When**: User asks to create a new skill or plugin, or after `/integrate` identifies a gap worth filling
- **How**: Invoke `linkedin-plugin-creator:plugin-creation` for full scaffold with ACL, crew ownership, taxonomy
- **Why**: Ensures new plugins follow LinkedIn's plugin ecosystem conventions

## How to Apply
- Check these triggers during Phase 1 (Research) and Phase 4 (Execute) of the engineering pipeline
- Invoke the skill BEFORE writing code, not after
- Mention to the user: "Checking [skill] for patterns before implementing..."
- If the skill returns patterns that conflict with existing code, follow existing code patterns (consistency > correctness for conventions)
