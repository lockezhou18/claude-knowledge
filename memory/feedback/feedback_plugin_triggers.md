---
name: Plugin Auto-Trigger Rules
description: When to proactively invoke underused LinkedIn plugin skills (linkedin-frameworks, kafka-flink, library-specs, mp-rules, plugin-creator) during work
type: feedback
---

Proactively invoke these plugin skills in the right context — don't wait for the user to ask.

### kafka-flink (linkedin-framework)
- **When**: Touching Kafka consumers, TrackerProcessor, topic configs, Samza/nearline processors
- **How**: Invoke `kafka-flink` skill before implementing to check patterns
- **Why**: Many MPs are Kafka-based; framework guidance prevents infra mistakes

### linkedin-frameworks (linkedin-framework)
- **When**: Adding new Offspring factories, boot listeners, D2 client wiring, Rest.li resources, or DI patterns
- **How**: Invoke `linkedin-frameworks` skill to check correct patterns
- **Why**: Offspring/D2/Rest.li have LinkedIn-specific conventions that differ from standard Spring/gRPC

### library-specs (spec-generation / fix)
- **When**: Adding or bumping dependencies in `product-spec.json`, or hitting version set conflicts during `mint build`
- **How**: `library-specs:spec-generation` for new deps, `library-specs:fix` for version conflicts
- **Why**: Specs document correct usage; version conflicts have known resolution patterns

### copy-rule-file / unignore-file (mp-rules)
- **When**: Creating new MP modules, modifying `.gitignore`, or needing build rule customization
- **How**: Invoke the relevant mp-rules skill
- **Why**: MP rules have specific conventions; wrong rules cause hard-to-debug build failures

### linkedin-plugin-creator:plugin-creation
- **When**: User asks to create a new skill or plugin, or after `/integrate` identifies a gap
- **How**: Invoke for full scaffold with ACL, crew ownership, taxonomy
- **Why**: Ensures new plugins follow LinkedIn's plugin ecosystem conventions

**How to apply:** Check these triggers during Phase 1 (Research) and Phase 4 (Execute). Invoke BEFORE writing code. If skill patterns conflict with existing code, follow existing code (consistency > correctness for conventions).
