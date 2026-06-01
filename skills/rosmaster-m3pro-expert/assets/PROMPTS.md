# Prompts

## Edit Chapters With LLM

```
Edit the Markdown documentation in the target folder so it reads like polished technical documentation while preserving the original technical meaning.

Scope:
- Do a full editorial pass, not just terminology cleanup. Rewrite awkward paragraphs, repeated setup text, headings, tables, captions, and instructions where needed.
- Match the polish level of neighboring cleaned courses: remove machine-translation phrasing, tighten flow, and make user-facing steps clear and direct.
- Preserve all technical facts: commands, code blocks, topic/message examples, terminal output, image links, filenames, paths, usernames, passwords, IP addresses, dimensions, ranges, IDs, and other numeric values.
- Keep operational context near commands, including which board, terminal, container, or host should run each command and what should happen afterward.
- Preserve code excerpts and command examples. If an output snippet is partial or truncated, label it as example or partial output instead of deleting it.
- Replace awkward machine-translation terms with clearer technical English, for example:
  - "car" -> "robot" when referring to the ROSMASTER platform generally
  - "motherboard" -> "mainboard"
  - "handle" -> "controller" or "gamepad"
  - "proxy" -> "agent" when referring to the ROS/micro-ROS agent
- Preserve existing document structure unless a small restructure improves readability.
- Create or update the section README using the linked-header style from sections 0 and 1: a short section overview, then one linked `##` heading per lesson with a concise summary.
- Update any relevant course/table-of-contents README when chapter names, section names, numbering, or folder coverage changes. Keep links accurate, include section numbers, and use clear chapter names.
- Use nearby repo docs first to fill obvious gaps. Use official/vendor docs only when necessary. Do not invent technical steps.
- Remove generated `README.json` metadata files in the same folders if they are not needed.
- After edits are done, create the section TOC and overview in README using the linked-header style from sections 0 and 1.

Verification:
- Check `git diff --check`.
- Confirm all local Markdown links and image links point to existing files, folders, or valid anchors.
- Confirm section README and top-level TOC links point to existing local Markdown files or folders.
- Confirm no unwanted `README.json` files remain in the target folder.
- Confirm Markdown code fences are balanced and there is no trailing whitespace.
- Spot-check the diff for accidental removal of code/output examples or board-specific run instructions.
- Spot-check the Markdown diff for depth: edits should show meaningful paragraph-level cleanup, not only global replacements such as `car` -> `robot` or `radar` -> `LiDAR`.
- Summarize changed files, verification results, and any external sources used.
```
