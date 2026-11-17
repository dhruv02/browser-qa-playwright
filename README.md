# Playwright UI Test Automation — Retail Demo Store

![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.13-blue) ![Playwright](https://img.shields.io/badge/Playwright-Chromium-2ea44f)

An independent **browser-automation portfolio project**, not a live commercial store. It includes a working, static HTML/JavaScript retail storefront and an end-to-end **Playwright + pytest** suite built with a Page Object Model.

## What it demonstrates

- Browser E2E testing with **Python, Playwright, pytest**
- Role-based locators and robust web-first assertions
- Page Object Model (`pages/store_page.py`)
- Parametrized search/form validation tests
- Cart calculations, updates, persistence, user journeys, responsive mobile view
- Browser-context isolation to prevent cross-test state leakage
- Local HTTP fixture: tests do not require any external website
- GitHub Actions test matrix on Python 3.12 and 3.13
- JUnit XML and failure screenshots

## Run on Windows (VS Code / PowerShell)

```powershell
cd D:\Projects\browser-qa-playwright
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe -m pytest -v
```

**Tip:** Your first browser install downloads Chromium; this is expected. Python 3.12 or 3.13 is recommended.

## Run the demo store manually

```powershell
.\.venv\Scripts\python.exe -m http.server 8000 --directory demo_store
```

Then open <http://localhost:8000> in your browser. No payments, credentials, or real customer records are involved.

## Example test categories

| Category | Tested behavior |
| --- | --- |
| Catalog | Loads 4 items, semantic heading, page title |
| Search | Mixed case, category filters, no matches |
| Cart | Add, increment, decrement, clear, accurate totals |
| Checkout | Missing cart, short names, invalid email, happy path |
| Persistence | Cart survives refresh; isolated across browser contexts |
| Responsive | Mobile viewport remains usable without horizontal overflow |

## Project structure

```text
browser-qa-playwright/
├── demo_store/           # Self-contained demo website (HTML, CSS, JavaScript)
├── pages/store_page.py   # Page Object Model
├── tests/conftest.py     # Local server + browser fixtures
├── tests/test_store_ui.py
├── .github/workflows/e2e.yml
├── requirements.txt
└── README.md
```

## GitHub Actions

Every push and pull request runs Chromium tests and uploads JUnit reports and failure screenshots. Open **Actions → Playwright browser E2E tests** to view results.

## Notes / limitations

- This is a deliberately small **synthetic demo storefront** for test automation, not a production e-commerce service.
- Checkout does not process payment or send real orders.
- For the strongest resume claim, only report a passing CI status **after** the public workflow succeeds.

## Resume bullet (after verified CI)

> Developed a Python Playwright/pytest UI test framework using Page Object Model, automated cart and checkout user journeys, and integrated Chromium browser tests with GitHub Actions CI.
