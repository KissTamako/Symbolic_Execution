(set-logic ALL)
; Frontier Constraint ID: fa08765dbc1b4786
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1480)) (False)
(assert (not (= x 1480)))

; Query: ((== x 1481)) (False)
(assert (not (not (= x 1481))))

(check-sat)
(get-model)
