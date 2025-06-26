#  Zainab's Task Management App – Full Test Plan

 

## 1. Overview

 

This test plan outlines the testing strategy used to validate the functionality, security, and robustness of Zainab's Task Management application built with Flask. It includes unit, integration, and security tests aligned with OWASP and DevOps best practices.

 

---

 

## 2. Test Categories

 

| Test Type           | Tool/Method Used         | Purpose                                      |

|---------------------|--------------------------|----------------------------------------------|

| Unit Testing        | `unittest`, `pytest`     | Validate routes, models, forms               |

| Property-Based      | `hypothesis`             | Edge-case testing for login/registration     |

| Integration Testing | `FlaskClient`            | Simulate full app flows                      |

| Security Testing    | Manual & automated       | Validate OWASP compliance (XSS, CSRF, Auth)  |

| Coverage Reporting  | `coverage report -m`            | Ensure 70%+ code coverage                    |

 

---

 

## 3. OWASP-Related Test Scenarios

 

| ID | Description                                           | Steps                                                                                   | Expected Result                               |

|----|-------------------------------------------------------|------------------------------------------------------------------------------------------|------------------------------------------------|

| OW1 | CSRF protection works                                 | Submit a form without a CSRF token                                                      | 403 Forbidden error                           |

| OW2 | Admin route access control                            | Logged-in user tries to access `/admin/users`                                            | Redirected with flash: “You do not have permission to access this page.”    |

| OW3 | Input sanitisation to prevent SQL injection           | Input `"' OR 1=1 --` in login or project fields                                         | Query fails safely, no data exposed           |

| OW4 | XSS prevention via comment input                      | Enter `<script>alert("XSS")</script>` into task title                                   | Escaped output shown as raw text              |

 

---

 

## 4. Functional Tests (CRUD)

 

### User Registration & Login

 

| Case ID | Description        | Steps                                               | Expected Result                            |

|---------|--------------------|------------------------------------------------------|---------------------------------------------|

| F1      | Valid Registration | Submit form with valid data                         | User created, redirected to dashboard       |

| F2      | Duplicate Email    | Register with existing email                        | Flash message: "Email already exists"       |

| F3      | Login Success      | Login with valid credentials                        | Redirect to dashboard, session active       |

| F4      | Login Failure      | Invalid credentials                                 | Flash: "Login failed. Check email and/or password."                |

 

### Project Management

 

| Case ID | Description             | Steps                                         | Expected Result                          |

|---------|-------------------------|-----------------------------------------------|-------------------------------------------|

| F5      | Create Project          | Admin or user creates valid project           | Project appears in list                   |

| F6      | Edit Project            | Edit name/description of existing project     | Changes saved and reflected               |

| F7      | Delete (admin only)     | Admin deletes project                         | Project confirmation box pops up -> project removed -> flash shown              |

 

### Task Management

 

| Case ID | Description           | Steps                                  | Expected Result                     |

|---------|-----------------------|----------------------------------------|--------------------------------------|

| F9      | Add Task              | Fill form with all fields              | Task created and listed              |

| F10     | Update Task           | Edit task title/description            | Task updated                         |

| F11     | Delete Task (admin)   | Admin clicks delete                    | Task confirmation box pops up -> task removed -> flash shown                         |
 

---

 

## 5. Metrics Tracked

 

| Metric                 | Target | Current   | Notes                            |

|------------------------|--------|-----------|----------------------------------|

| Code Coverage          | 80%    | ~75%      | Currently below, being improved  |

| Passing Tests          | 100%   | ~90%      | Fixing test data setup issues    |

| Critical Vulnerability | 0      | 0         | All mitigated via code/validation|

 

---

 

## 6. Test Artefacts Location

 

- `/tests/test_projects.py`: Core CRUD & auth tests

- `/tests/test_properties.py`: Property-based testing

- `coverage report`: In `htmlcov/index.html` when run locally

- Screenshot evidence: Can be found in the written assignment and VIVA presentation.

 

---

 

## 7. Run Tests Locally

 

```bash

# Activate virtual environment

source venv/bin/activate

 

# Run tests

pytest tests/

 

# Check coverage

coverage run -m pytest

coverage report

coverage html