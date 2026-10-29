# Customer Service Chatbot — Developer Project Handbook

**Repository:** https://github.com/build-aayan1219/customer_service_chatbot_LLM  
**Purpose:** End-to-end development context for developers and coding agents (including Cursor). This is a living project handbook, not a Task 2-only brief.

> **Source-of-truth rule:** This handbook summarizes known project history. Before coding, inspect the current repository, project documentation, requirements, tests, Git history, and current branch. If repository evidence differs from this handbook, trust the current repository and record the discrepancy. Do not invent requirements for tasks whose specifications are not present.

---

## 1. Project mission

Build and maintain a reliable customer-service chatbot that can answer from an approved knowledge base, handle customer conversations and evidence files, maintain a safe and updateable knowledge base, and progressively gain operational capabilities such as support-case workflows, analytics, and production-readiness controls as defined by the project's actual task specifications.

Core engineering principles:

- Ground answers in approved knowledge and customer-provided evidence.
- Never invent missing facts; clearly communicate uncertainty and request clarification.
- Protect customer data and credentials.
- Make file processing, knowledge-base updates, and background work observable and recoverable.
- Prefer small, tested changes over large rewrites.
- Preserve existing behavior and backward compatibility unless a requirement explicitly calls for a change.
- Verify work through automated tests and clear evidence, not by assuming that code presence means a requirement is complete.

## 2. Working rules for developers and Cursor

1. **Local-only by default:** never push, publish, merge, create a PR, or change remote branches unless the user explicitly asks.
2. Do not commit unless explicitly instructed.
3. Start by checking `git status`, the current branch, and existing diffs. Preserve user changes.
4. Read this handbook and the current repository documentation before implementation.
5. Do not start or claim a task is complete without locating its actual specification and acceptance criteria.
6. Do not replace existing modules with a second parallel implementation. Reuse current modules and established data structures where possible.
7. Do not expose `.env`, API keys, credentials, customer uploads, raw extracted text, or personal/payment information in logs, tests, reports, or commits.
8. Never run destructive operations on real conversation data, FAISS indexes, manifests, or pipeline state while testing. Use temporary directories and fixtures.
9. Do not install dependencies, change versions, or change the architecture without a clear technical reason. Explain necessary changes.
10. Add or update tests for each behavior change; do not weaken thresholds or tests just to obtain a pass.
11. Keep changes scoped to the active task. Do not combine unrelated UI redesign, cleanup, or future tasks with current work.
12. At the end, report exact files changed, test commands/results, remaining gaps, and whether any commit/push occurred.

## 3. Known architecture and technology

The project has historically used:

- Python
- Streamlit for the web UI
- LangChain for retrieval/LLM orchestration
- Google Gemini for model responses
- Hugging Face sentence-transformer embeddings
- FAISS for vector retrieval
- PDF/text and image extraction/OCR libraries depending on the installed requirements
- Environment variables for API keys and local configuration

Verify actual dependency versions and current architecture in `requirements.txt`, lock files, config, and imports. Do not assume historical package versions are still installed.

### Known modules (inspect before editing)

| File/module | Known responsibility | Development guidance |
|---|---|---|
| `src/config.py` | Configuration/settings | Centralize settings; keep secrets in environment variables. |
| `src/main.py` | Streamlit entry point and UI | Preserve existing UX flows; avoid UI redesign unless the active task requires it. |
| `src/langchain_helper.py` | Retrieval and LLM-answering path | Keep answers grounded; test normal RAG and attachment-related questions. |
| `src/chat_manager.py` | Chat/session logic | Preserve conversation/session behavior. |
| `src/analytics.py` | Analytics functionality | Inspect actual metrics/storage before extending. |
| `src/knowledge_base.py` | Knowledge-base update pipeline | Keep updates staged, quality-gated, versioned, and recoverable. |
| `src/conversation_files.py` | Conversation file upload/storage/manifests/index integration | Keep storage paths, hashes, manifests, and index references consistent. |
| `src/evidence_processor.py` | Evidence extraction/OCR | Preserve uncertainty and source provenance; do not invent values. |
| `src/task2_security.py` | Upload validation, security/privacy helpers | Validate actual content and handle untrusted inputs safely. |
| `src/background_queue.py` | Background processing queue | Test job transitions/status/retries deterministically. |
| `src/retention_manager.py` | Retention and cleanup | Ensure expiry removes stale references and is safe/idempotent. |
| `tests/` | Automated tests | Inspect existing coverage; add regression tests with each feature. |
| `knowledge_base/` | Data, pipeline state, versions, indexes, conversation manifests and possibly uploads | Treat as potentially sensitive runtime data. Avoid destructive test runs. |

The exact module list and responsibilities must be checked against the current tree. If a capability has no dedicated module, inspect existing service paths before adding one.

## 4. Current known project status

This is historical context, not a claim of current verified correctness:

- **Task 1:** a knowledge-base update pipeline exists in `src/knowledge_base.py` and `knowledge_base/pipeline/`. Prior work covered detecting new/modified documents, content hashes/duplicates, quarantine, versions/rollback, quality checks, scheduled execution, retry delays, and maintenance-window activation. Regression-test it rather than rewriting it by default.
- **Task 2:** evidence-file processing has modules for OCR/extraction, upload security, conversation file integration, background jobs, and retention. These need end-to-end validation and may have extraction-quality, file validation, duplicate-storage, background notification, and retention/index consistency gaps.
- **Tasks 3 onward:** their exact numbered requirements are not completely available in this summary. Cursor/developers must search the repository, README, task/specification JSON/Markdown/PDFs, issues, and user-provided documents for authoritative task descriptions. Do not guess their contents. If specifications cannot be found, ask the user to supply them before implementing those tasks.

Recent repository review previously found Task 2 modules and a small basic security test file. A prior queued PDF result had a perfect quality score despite obviously noisy structured fields, suggesting quality scoring needs stronger validation. A previous retention run logged a manifest-shape error. These are leads to verify in current code, not unquestionable facts.

## 5. Development lifecycle for every task

Use this repeatable workflow for Task 1, Task 2, and every later task:

### Phase A — Discover
1. Inspect `git status`, current branch, and diffs.
2. Read README, dependency files, config, source tree, tests, and all task/specification files.
3. Search recent commits/issues/task JSON files for acceptance criteria.
4. Trace the relevant end-to-end code path and data formats.
5. Write a short task plan with acceptance criteria and dependencies.
6. Identify data privacy, security, compatibility, and migration risks.

### Phase B — Establish a baseline
1. Run relevant existing tests before editing.
2. Record exact commands, environment constraints, pass/fail/skip counts, and errors.
3. Reproduce the bug/feature gap with a small test or fixture where possible.
4. Do not run tests that mutate real production-like knowledge-base data without isolating their paths.

### Phase C — Implement
1. Add focused tests before or alongside changes.
2. Make small changes in the existing architecture.
3. Validate inputs at boundaries and handle errors explicitly.
4. Keep business logic testable outside Streamlit where practical.
5. Use dependency injection/mocks for OCR, time, queue execution, and LLM/API calls where appropriate.
6. Preserve compatibility with existing manifests/indexes/config or implement a clear migration when required.
7. Keep customer data and secrets out of logs.

### Phase D — Verify
1. Run focused tests after each meaningful change.
2. Run related regression tests.
3. Run the full test suite.
4. Test failure cases and boundary conditions, not just the happy path.
5. Inspect final diffs for unrelated changes, secrets, personal data, generated files, and accidental state changes.
6. Report what was actually tested; distinguish passing tests from manual or unverified behavior.

### Phase E — Handoff
For each task, provide:
- Requirement-by-requirement completion status.
- Files changed and key design choices.
- Test commands and actual results.
- Remaining limitations, risks, and manual checks.
- Whether the work remains local or was committed/pushed (default: local only).
- A recommended next step; do not automatically start it.

---

## 6. Task 1 — Knowledge-base update pipeline

### Known requirements
1. Process only new or modified documents.
2. Detect duplicates.
3. Quarantine invalid files.
4. Maintain versions and support rollback.
5. Run quality tests before activating an update.
6. Reject updates that reduce accuracy or grounding.
7. Schedule updates at a configurable time.
8. Retry failed updates after 15, 30, and 60 minutes.
9. Activate approved updates only during the maintenance window.

### Known implementation
`src/knowledge_base.py` and `knowledge_base/pipeline/` contain the implementation and state/version artifacts. Previous work reportedly addressed scanning physical uploads missing from the manifest, candidate-vs-baseline quality comparisons, and CSV loading via pandas plus `langchain_core.documents.Document`.

### Execution plan
1. Locate task-specific tests and inspect pipeline state/schema.
2. Use temporary input directories and temporary pipeline state.
3. Test unchanged documents are skipped and modified/new documents are processed.
4. Test hash duplicate detection and invalid-file quarantine.
5. Test version snapshots and rollback.
6. Test candidate quality evaluation and rejection when accuracy/grounding regresses.
7. Test configurable schedule, 15/30/60-minute retry sequence, and maintenance-window-only activation with a fake clock.
8. Verify failures leave the active version unchanged.
9. Run Task 1 regression tests after changes to shared retrieval/storage.
10. Do not activate/rollback real versions during tests. Do not rewrite Task 1 as part of another task unless a proven shared defect requires it.

**Completion evidence:** automated tests for each requirement, safe isolated state, and a final report with actual results.

---

## 7. Task 2 — Customer evidence processing

### Known requirements
1. Handle customer messages and supported screenshots/images, invoices, PDFs, and product images.
2. Extract order IDs, dates, amounts, product information, and error codes where present.
3. Compare evidence with the customer's message.
4. Ask for clarification or a better file if evidence conflicts or image quality is low.
5. Never invent missing values.
6. Mask personal/payment data in logs.
7. Reject unsafe files and hidden prompt injections in images/documents.
8. If processing exceeds 30 seconds, use a background queue and notify the customer.
9. Delete uploaded files after the configured retention period.

### Known modules
`src/evidence_processor.py`, `src/task2_security.py`, `src/conversation_files.py`, `src/background_queue.py`, `src/retention_manager.py`, `src/langchain_helper.py`, `src/config.py`, and associated tests. Follow the real call graph before editing.

### Execution plan
1. Baseline the existing test suite.
2. Trace upload → validation → hash/deduplication → storage/manifest → extraction/OCR → quality/confidence → comparison/clarification → retrieval/answer → queue/status → retention/index cleanup.
3. Add tests for readable and blurred images, text/scanned/partially readable PDFs, missing fields, contradictory invoices, and attachment overview requests.
4. Improve structured extraction and quality scoring so noisy output cannot be assigned perfect confidence.
5. Use OCR fallback when PDF text is absent or materially incomplete/garbled; if uncertain, ask for a clearer file rather than guessing.
6. Ensure missing fields stay missing, contradictions are surfaced, and answers are grounded in source evidence.
7. Validate file size, extension, actual signature/magic bytes, malformed content, and unsafe inputs. Treat document content as untrusted and isolate prompt injection.
8. Mask PII/payment information before logging; test that raw sensitive values do not appear in captured logs.
9. Deduplicate by content hash and prevent different files with the same filename from overwriting each other.
10. Prove >30-second queue transition and customer-visible status with mocked time; do not sleep for 30 seconds in unit tests.
11. Make retention expiry remove stale files and manifest/index references, handle supported manifest shapes, and be idempotent.
12. Run Task 2 tests, Task 1 regressions, normal RAG regressions, attachment-inspection regressions, and the full suite.
13. Test with temporary directories/mocks; never delete real knowledge-base/conversation files during verification.

### Known risks to verify
- Earlier extraction results included noisy IDs/products with `evidence_quality = 1.0`.
- Partial PDF text may prevent OCR fallback.
- Original-filename storage may cause collisions.
- Extension checks may not verify the true file type.
- Retention has previously logged a list/dict manifest shape error.
- Queue presence does not prove delayed processing/status notifications work.
- Attachment-overview detection was previously expanded; protect it with tests.

**Completion evidence:** requirement-level automated coverage and actual passing results, or explicit documentation of external blockers and safe fallbacks.

---

## 8. Tasks 3 onward — requirements discovery and execution

**Important:** The complete authoritative specifications for Tasks 3 onward are not reproduced in this handbook. Do not invent task titles, requirements, APIs, data models, or acceptance criteria.

For each future task:
1. Search the repository for task specifications in README/docs, `task*.json`, Markdown/PDF files, issue templates, tests, and relevant Git history.
2. Extract the exact requirements and preserve their wording.
3. Identify dependencies on completed tasks and shared modules.
4. Ask the user to supply missing specifications if the repository does not contain them.
5. Convert each requirement into an implementation plan and acceptance test matrix.
6. Implement only the active task, keeping earlier tasks working.
7. Add tests for happy paths, edge cases, failure modes, privacy/security, and regressions.
8. Run focused tests, prior-task regression tests, and the full suite.
9. Update this handbook with verified status only; distinguish implemented, tested, partially verified, and not started.
10. Do not mark a task complete without evidence.

### Cross-task implementation rules
- Reuse the existing chat/session, retrieval, configuration, and storage architecture.
- Add new modules only when a distinct responsibility is justified and current code has no suitable home.
- Avoid schema changes without compatibility/migration tests.
- Keep operational behavior configurable where the specification requires it.
- Use stable, explicit status values for queued/running/succeeded/failed/expired states if required by a task.
- Make retry, cleanup, and update jobs safe to repeat.
- Ensure analytics/logging do not expose private data.
- Keep UI changes scoped to task requirements and preserve core chat behavior.
- Treat test failures as defects to investigate, not as reasons to remove or weaken tests.

---

## 9. Repository hygiene and privacy

A previous GitHub review observed potentially sensitive runtime artifacts in the repository tree, including conversation files, PDFs/DOCX uploads, logs, local databases, manifests, and indexes. Re-check current tracking status before acting.

- Do not automatically delete files from Git.
- Identify whether files are needed as public fixtures, examples, or private runtime data.
- Prefer synthetic/anonymized fixtures for tests.
- Consider adding appropriate ignore rules for runtime uploads/logs/databases/indexes after confirming intended repository policy.
- `.gitignore` does not remove files already tracked or erase historical Git commits. Any history cleanup is a separate, consequential operation requiring explicit approval.
- Never commit `.env`, credentials, real customer documents, or sensitive logs.

---

## 10. Cursor's general project prompt

Paste this prompt into Cursor when beginning a project-wide development session:

> Read `DEVELOPER_PROJECT_HANDBOOK.md` completely. Inspect the current repository and identify the active task's authoritative specification before editing. Start by checking Git status, branch, diffs, dependencies, documentation, task files, tests, and recent history. Preserve uncommitted work. Work locally only: do not commit, push, publish, merge, create a PR, or change remote branches unless I explicitly authorize it. Do not expose secrets or customer data, and do not run destructive tests on real runtime data. Implement only the task I name, using existing modules and small testable changes. If I have not named a task, first summarize the project structure, verified task status, missing specifications, and recommended next steps—do not start coding. For implementation, establish a test baseline, map the relevant call path, add/update regression tests, implement the smallest robust change, run focused and full tests, inspect the final diff, and report exact files, commands/results, gaps, and whether anything was committed/pushed. Treat unknown task requirements as unknown; search the repository or ask me instead of inventing them.

---

## 11. Verified status tracking template

Update this section only after inspecting the current repository and running relevant tests. Do not use a status label based on file existence alone.

| Task | Status | Evidence / tests | Remaining gaps |
|---|---|---|---|
| Task 1 — Knowledge-base update pipeline | Implemented historically; current verification required | Record current test commands/results | Regression coverage/state isolation as needed |
| Task 2 — Customer evidence processing | In progress; current verification required | Record extraction/security/queue/retention test results | Record any uncovered requirement |
| Task 3 | Specification must be located | Link/file/test references | Ask user if unavailable |
| Task 4+ | Specification must be located | Link/file/test references | Ask user if unavailable |

**Status vocabulary:** Not started · In progress · Implemented, unverified · Partially verified · Verified by tests · Blocked. Always include the evidence supporting the status.
