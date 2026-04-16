(set-logic ALL)
; Constraint ID: 2cea322d3d9f615a
; Generated at: 2026-04-16 04:18:59
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59329)) (False)
(assert (not (not (= x 59329))))

(check-sat)
(get-model)
