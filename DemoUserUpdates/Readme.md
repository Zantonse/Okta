Okta Bulk User Attribute Updater

Enrich missing or inconsistent profile fields for every Okta‑native user in your org with one command.

Features

Zero‑touch enrichment – Iterates through all Okta users and patches only the attributes that are blank or malformed.

Realistic sample data – Leverages the Faker library to create believable names, emails, and cities so demos look genuine.

Department‑aware mappings – Generates titles, cost centers, and organizations that align to each department.

Manager assignment – Fills both manager and managerId from a configurable pool of addresses.

Idempotent – Already‑populated attributes are left untouched, making it safe to rerun.

Prerequisites

Requirement

Notes

Python ≥ 3.8

Tested on 3.9 and 3.12

Okta API token

Needs okta.users.read and okta.users.manage scopes

Packages

pip install -r requirements.txt (installs requests and Faker)

Environment Variables

Variable

Description

OKTA_ORG

Your Okta org base URL, e.g. https://acme.okta.com

OKTA_API_TOKEN

API token with the scopes listed above

COMPANY_EMAIL_DOMAIN

Optional. Defaults to example.com

Quick Start

# 1. Export required variables
export OKTA_ORG="https://acme.okta.com"
export OKTA_API_TOKEN="00aBcD..."

# 2. Install deps
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. Run the script
python okta_update_attributes.py

How It Works

Pagination – Fetches users in batches of 200 via /api/v1/users.

Filtering – Skips any accounts where credentials.provider.type ≠ OKTA.

Enrichment – Calls generate_profile_overrides() to build a minimal payload containing only missing fields.

Partial Update – Sends POST /api/v1/users/{id} with { "profile": overrides }.

See the inline comments in okta_update_attributes.py for implementation details. fileciteturn0file0

Customisation

Department Lists – Tweak DEPT_TITLES, DEPT_COST_CENTER, and DEPT_ORGANIZATION at the top of the script.

City Pool – Replace the CITIES list with locales relevant to your workforce.

Managers – Populate the MANAGERS list with real manager emails.

Add command‑line flags (e.g. --dry-run, --dept Engineering) to tailor output volume.

Safety Checklist

☑ Test in a sandbox first☑ Take a backup (GET /api/v1/users)☑ Communicate upcoming changes to stakeholders☑ Use Okta System Log to verify success

Contributing

Pull requests are welcome! Please open an issue first to discuss your proposed change.

License

MIT © 2025 Craig Verzosa

