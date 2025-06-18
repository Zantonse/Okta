#!/usr/bin/env python3
import os
import sys
import requests
import random
from faker import Faker

# ─── CONFIG ────────────────────────────────────────────────────────────────────
OKTA_ORG       = os.getenv("OKTA_ORG")
API_TOKEN      = os.getenv("OKTA_API_TOKEN")
EMAIL_DOMAIN   = os.getenv("COMPANY_EMAIL_DOMAIN", "example.com")

if not OKTA_ORG or not API_TOKEN:
    print("Please set OKTA_ORG and OKTA_API_TOKEN environment variables.")
    sys.exit(1)

HEADERS = {
    "Authorization": f"SSWS {API_TOKEN}",
    "Accept":        "application/json",
    "Content-Type":  "application/json"
}

faker = Faker()

# ─── DEPARTMENT → TITLE MAPPING ─────────────────────────────────────────────────
DEPT_TITLES = {
    "Engineering":           ["Software Engineer", "Frontend Engineer", "Backend Engineer", "SRE", "DevOps Engineer"],
    "Product":               ["Product Manager", "Product Owner", "Business Analyst", "UX Researcher"],
    "Data Science":          ["Data Scientist", "ML Engineer", "Data Analyst"],
    "Design":                ["UX Designer", "UI Designer", "Product Designer"],
    "Quality Assurance":     ["QA Engineer", "Test Engineer", "Automation Engineer"],
    "Sales":                 ["SDR", "Account Executive", "Sales Manager"],
    "Customer Success":      ["Customer Success Manager", "Technical Account Manager", "Support Specialist"],
    "Solutions Engineering": ["Solutions Engineer", "Pre-Sales Engineer", "Sales Engineer"],
    "Marketing":             ["Marketing Manager", "Content Strategist", "SEO Specialist", "Social Media Manager"],
    "Finance":               ["Finance Analyst", "Controller", "Revenue Operations Analyst"],
    "People Ops":            ["HR Manager", "People Ops Manager", "Talent Dev Specialist"],
    "Legal & Compliance":    ["Legal Counsel", "Privacy Officer", "Compliance Manager", "Risk Analyst"],
    "IT & Security":         ["IT Support Specialist", "Network Administrator", "Security Analyst", "GRC Manager"],
    "Operations":            ["Operations Manager", "Facilities Coordinator"],
    "Executive Office":      ["CEO", "CTO", "CFO", "COO", "CMO", "CISO", "Chief of Staff"]
}

# ─── DEPARTMENT → COST CENTER & ORG ─────────────────────────────────────────────
DEPT_COST_CENTER = {
    "Engineering":       "CC-ENG-1001",  "Product":     "CC-PROD-1002",
    "Data Science":      "CC-DS-1003",   "Design":      "CC-DES-1004",
    "Quality Assurance": "CC-QA-1005",   "Sales":       "CC-SALES-2001",
    "Customer Success":  "CC-CS-2002",   "Solutions Engineering":"CC-SE-2003",
    "Marketing":         "CC-MKT-3001",  "Finance":     "CC-FIN-4001",
    "People Ops":        "CC-HR-5001",   "Legal & Compliance":"CC-LC-6001",
    "IT & Security":     "CC-ITSEC-7001","Operations":  "CC-OPS-8002",
    "Executive Office":  "CC-EXEC-9001"
}

DEPT_ORGANIZATION = {
    "Engineering":       "Technology",     "Product":               "Technology",
    "Data Science":      "Technology",     "Design":                "Technology",
    "Quality Assurance": "Technology",     "Sales":                 "Commercial",
    "Customer Success":  "Commercial",     "Solutions Engineering": "Commercial",
    "Marketing":         "Marketing",      "Finance":               "Finance",
    "People Ops":        "People Ops",     "Legal & Compliance":    "Legal & Compliance",
    "IT & Security":     "IT & Security",  "Operations":            "Operations",
    "Executive Office":  "Executive Office"
}

# ─── MAJOR U.S. CITIES ───────────────────────────────────────────────────────────
CITIES = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
    "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte",
    "San Francisco", "Indianapolis", "Seattle", "Denver", "Washington"
]

# ─── MANAGER POOL (PLACEHOLDER EMAILS) ──────────────────────────────────────────
MANAGERS = [
    "enter.manager.email.1@yourcompany.com",
    "enter.manager.email.2@yourcompany.com",
    "enter.manager.email.3@yourcompany.com",
    "enter.manager.email.4@yourcompany.com"
]

# ─── HELPERS ────────────────────────────────────────────────────────────────────
def get_all_users():
    url = f"{OKTA_ORG}/api/v1/users?limit=200"
    while url:
        resp = requests.get(url, headers=HEADERS)
        resp.raise_for_status()
        for u in resp.json():
            yield u
        next_link = None
        for part in resp.headers.get("Link", "").split(","):
            if 'rel="next"' in part:
                next_link = part.split("<")[1].split(">")[0]
        url = next_link

def generate_profile_overrides(profile):
    upd = {}
    # ─── NAMES ───────────────────────────
    first = profile.get("firstName") or faker.first_name()
    last  = profile.get("lastName")  or faker.last_name()
    if not profile.get("firstName", "").strip(): upd["firstName"] = first
    if not profile.get("lastName", "").strip():  upd["lastName"]  = last

    # ─── LOGIN & EMAIL ───────────────────
    if not profile.get("login", "").strip():
        login = f"{first.lower()}.{last.lower()}@{EMAIL_DOMAIN}"
        upd["login"] = login
    else:
        login = profile["login"]
    if not profile.get("email", "").strip():
        upd["email"]       = login
        upd["secondEmail"] = f"{first.lower()}@{EMAIL_DOMAIN}"

    # ─── DEPARTMENT → TITLE ──────────────
    dept = profile.get("department", "").strip()
    if not dept:
        dept = random.choice(list(DEPT_TITLES.keys()))
        upd["department"] = dept
    if not profile.get("title", "").strip():
        upd["title"] = random.choice(DEPT_TITLES.get(dept, []))

    # ─── COST CENTER & ORG ───────────────
    cc  = DEPT_COST_CENTER.get(dept)
    org = DEPT_ORGANIZATION.get(dept)
    if cc  and not profile.get("costCenter", "").strip(): upd["costCenter"] = cc
    if org and not profile.get("organization", "").strip():upd["organization"] = org

    # ─── CITY ─────────────────────────────
    if not profile.get("city", "").strip():
        upd["city"] = random.choice(CITIES)

    # ─── MANAGER & MANAGERID ─────────────
    if not profile.get("manager", "").strip():
        mgr = random.choice(MANAGERS)
        upd["manager"]   = mgr
        upd["managerId"] = mgr

    return upd

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    updated = 0
    for user in get_all_users():
        # Only Okta-native users
        provider = user.get("credentials", {}) \
                       .get("provider", {}) \
                       .get("type", "")
        if provider != "OKTA":
            continue

        uid      = user["id"]
        profile  = user["profile"]
        overrides = generate_profile_overrides(profile)
        if not overrides:
            continue

        print(f"✏️ Updating {profile.get('login')} ({uid}): {overrides}")
        resp = requests.post(
            f"{OKTA_ORG}/api/v1/users/{uid}",
            headers=HEADERS,
            json={"profile": overrides}
        )
        resp.raise_for_status()
        updated += 1

    print(f"\n✅ Done. Updated {updated} user{'s' if updated!=1 else ''}.")

if __name__ == "__main__":
    main()
