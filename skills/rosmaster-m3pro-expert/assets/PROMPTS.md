# Prompts

## Edit chapters with LLM:

```
Edit the Markdown documentation in the target folder to improve the English while preserving technical meaning.

Scope:
- Do a full editorial pass, not only a terminology cleanup. Rewrite awkward paragraphs, repeated setup text, headings, tables, captions, and instructions so they read like clear technical documentation while preserving technical meaning.
- Match the polish depth used in already-cleaned neighboring courses: tighten flow, remove machine-translation phrasing, improve sentence structure, and clarify user-facing steps wherever the original prose is awkward or repetitive.
- Keep all command blocks, image links, filenames, paths, usernames, passwords, IP addresses, and technical values accurate.
- Preserve code excerpts, command examples, topic/message examples, and terminal output snippets. If an output snippet is partial or truncated, label it as an example or partial output instead of deleting it.
- Preserve operational context near commands, such as which board/terminal/container to use and what should happen after the command runs. Shorten duplicated wording only when the remaining text still gives the user enough context to run the step safely.
- Replace awkward machine-translation terms with clearer technical English, for example:
  - "car" -> "robot" when referring to the ROSMASTER platform generally
  - "motherboard" -> "mainboard"
  - "handle" -> "controller" or "gamepad"
  - "proxy" -> "agent" when referring to the ROS/micro-ROS agent
- Preserve existing document structure unless a small restructure improves readability.
- Update the relevant course/table-of-contents README when chapter names, section names, numbering, or folder coverage changes. Keep TOC links accurate, include section numbers, and use clear chapter names.
- Use official/vendor docs or nearby repo docs to fill obvious gaps, but do not invent technical steps.
- If required information is missing in the source chapter, fill the gap using common technical knowledge or targeted web search, and keep added details practical and verifiable.
- Remove generated `README.json` metadata files in the same folders if they are not needed.

Verification:
- Check `git diff --check`.
- Confirm all local Markdown image links still point to existing files.
- Confirm TOC links point to existing local Markdown files or folders.
- Confirm no unwanted `README.json` files remain in the target folder.
- Spot-check the diff for accidental removal of code/output examples or board-specific run instructions.
- Spot-check the Markdown diff for depth: the prose should show meaningful paragraph-level editing, not just global replacements such as `car` -> `robot` or `radar` -> `LiDAR`.
- Summarize changed files and any external sources used.
```
