/* 
  QuickCart Reconciliation Report
  Objective: Establish a defensible source of truth for revenue.
*/

-- 1. Deduplicate: Pick the most recent successful payment per order
WITH clean_internal_payments AS (
    SELECT 
        order_id,
        amount_cents,
        ROW_NUMBER() OVER(PARTITION BY order_id ORDER BY attempted_at DESC) as attempt_rank
    FROM payments
    WHERE status = 'SUCCESS'
),

-- 2. Internal Revenue (Matching orders to valid payments)
internal_revenue AS (
    SELECT 
        SUM(p.amount_cents) / 100.0 AS total_expected_revenue
    FROM orders o
    JOIN clean_internal_payments p ON o.order_id = p.order_id
    WHERE o.is_test = 0 AND p.attempt_rank = 1
),

-- 3. Orphan Payments (Success payments with no order ID)
orphan_revenue AS (
    SELECT 
        SUM(amount_cents) / 100.0 AS total_orphan_money
    FROM payments
    WHERE order_id IS NULL AND status = 'SUCCESS'
),

-- 4. Bank Truth (Actual money in bank)
bank_truth AS (
    SELECT 
        SUM(settled_amount_cents) / 100.0 AS total_bank_settled
    FROM bank_settlements
    WHERE status = 'SETTLED'
)

-- FINAL SUMMARY REPORT
SELECT 
    ir.total_expected_revenue AS "Total Successful Sales",
    orph.total_orphan_money AS "Orphan Payments",
    bt.total_bank_settled AS "Bank Settled Amount",
    (ir.total_expected_revenue - bt.total_bank_settled) AS "Discrepancy Gap"
FROM internal_revenue ir, orphan_revenue orph, bank_truth bt;
