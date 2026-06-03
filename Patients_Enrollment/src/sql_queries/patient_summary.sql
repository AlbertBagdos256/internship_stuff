-- Patient Financial Summary
-- Output
/*patient_id
first_name
last_name
state
total_encounters
total_claim_cost
total_payer_coverage
out_of_pocket_cost*/


WITH encounter_summary AS (
    SELECT "PATIENT", 
           COUNT("Id") AS total_encounters,
           SUM("TOTAL_CLAIM_COST") AS TOTAL_CLAIM_COST,
           SUM("PAYER_COVERAGE") AS total_payer_coverage
    FROM encounters
    GROUP BY "PATIENT"
)

SELECT "Id",
       "FIRST", 
       "LAST",
       "STATE",
       "HEALTHCARE_EXPENSES" - "HEALTHCARE_COVERAGE" AS total_expenses,
       es.TOTAL_CLAIM_COST,
       es.total_encounters,
       es.total_payer_coverage
FROM patients pt
INNER JOIN encounter_summary es ON pt."Id" = es."PATIENT"

