# Test Cases — Invoice OCR System

| ID | Component | Test Scenario | Expected Result | Status |
|---|---|---|---|---|
| TC-001 | Parser | Extract invoice number | Correct invoice number extracted | PASS |
| TC-002 | Parser | Extract order information | Order information detected | PASS |
| TC-003 | Parser | Extract date | Date information detected | PASS |
| TC-004 | Parser | Extract total | Total information detected | PASS |
| TC-005 | Parser | Preserve raw OCR text | Original text preserved | PASS |
| TC-006 | Validator | Existing file | Validation succeeds | PASS |
| TC-007 | Validator | Missing file | FileNotFoundError raised | PASS |
| TC-008 | Validator | Empty path | ValueError raised | PASS |
| TC-009 | Validator | Invalid image extension | ValueError raised | PASS |
| TC-010 | Validator | Invalid PDF extension | ValueError raised | PASS |
| TC-011 | Image Processor | Valid image processing | Invoice data returned | PASS |
| TC-012 | Image Processor | Missing image | FileNotFoundError raised | PASS |
| TC-013 | Regression | Run complete pytest suite | All tests pass | PASS |

## Test Execution

Command:

```bash
pytest -v