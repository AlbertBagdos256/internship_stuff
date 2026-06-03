import pandas as pd
import pyodbc
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=prod-sql;"
    "DATABASE=enrollment;"
    "UID=svc_user;"
    "PWD=Welcome123"
)

today = datetime.now()

members = pd.read_sql("""
SELECT *
FROM MemberEnrollment
WHERE EnrollmentDate >= '2024-01-01'
""", conn)

billing = pd.read_sql("""
SELECT *
FROM PremiumBilling
""", conn)

providers = pd.read_sql("""
SELECT *
FROM ProviderAssignments
""", conn)

members["FirstName"] = members["FirstName"].fillna("")
members["LastName"] = members["LastName"].fillna("")

for i in range(len(members)):
    members.loc[i, "FirstName"] = (
        str(members.loc[i, "FirstName"])
        .replace("1","")
        .replace("2","")
        .replace("3","")
        .replace("4","")
        .replace("5","")
        .replace("6","")
        .replace("7","")
        .replace("8","")
        .replace("9","")
    )

for i in range(len(members)):
    members.loc[i, "LastName"] = (
        str(members.loc[i, "LastName"])
        .replace("1","")
        .replace("2","")
        .replace("3","")
        .replace("4","")
        .replace("5","")
        .replace("6","")
        .replace("7","")
        .replace("8","")
        .replace("9","")
    )

billing["Amount"] = billing["Amount"].fillna(0)

for i in range(len(billing)):
    if billing.loc[i, "Amount"] < 0:
        billing.loc[i, "Amount"] = 0

merged = pd.merge(
    members,
    billing,
    on="MemberID",
    how="left"
)

merged2 = pd.merge(
    merged,
    providers,
    on="MemberID",
    how="left"
)

merged2["EnrollmentDate"] = pd.to_datetime(
    merged2["EnrollmentDate"]
)

merged2["BillingDate"] = pd.to_datetime(
    merged2["BillingDate"]
)

merged2["DaysToBill"] = (
    merged2["BillingDate"]
    - merged2["EnrollmentDate"]
).dt.days

active_members = merged2[
    merged2["Status"] == "ACTIVE"
]

inactive_members = merged2[
    merged2["Status"] == "INACTIVE"
]

active_count = len(active_members)
inactive_count = len(inactive_members)

state_report = []

states = merged2["State"].unique()

for s in states:

    subset = merged2[
        merged2["State"] == s
    ]

    active = len(
        subset[
            subset["Status"] == "ACTIVE"
        ]
    )

    inactive = len(
        subset[
            subset["Status"] == "INACTIVE"
        ]
    )

    billed = len(
        subset[
            subset["Amount"] > 0
        ]
    )

    unbilled = len(
        subset[
            subset["Amount"] == 0
        ]
    )

    avg_days = subset["DaysToBill"].mean()

    row = {
        "State": s,
        "Active": active,
        "Inactive": inactive,
        "Billed": billed,
        "Unbilled": unbilled,
        "AvgDaysToBill": avg_days
    }

    state_report.append(row)

report = pd.DataFrame(state_report)

reconciliation = []

for state in report["State"]:

    r = report[
        report["State"] == state
    ]

    active = int(r["Active"].iloc[0])
    billed = int(r["Billed"].iloc[0])

    if abs(active - billed) > 50:

        reconciliation.append({
            "State": state,
            "Difference": active - billed
        })

reconciliation_df = pd.DataFrame(
    reconciliation
)

report.to_excel(
    f"EnrollmentReport_{today.strftime('%Y%m%d')}.xlsx",
    index=False
)

reconciliation_df.to_excel(
    f"Reconciliation_{today.strftime('%Y%m%d')}.xlsx",
    index=False
)

if len(reconciliation_df) > 0:

    body = reconciliation_df.to_html()

    msg = MIMEText(
        body,
        "html"
    )

    msg["Subject"] = "Enrollment Mismatch"

    server = smtplib.SMTP(
        "mail.company.com",
        25
    )

    server.sendmail(
        "etl@company.com",
        ["manager@company.com"],
        msg.as_string()
    )

    server.quit()

print("finished")