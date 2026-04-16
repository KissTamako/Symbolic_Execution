(set-logic ALL)
; Constraint ID: 36d263430ed2a6af
; Generated at: 2026-04-16 04:18:59
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59332)) (False)
(assert (not (not (= x 59332))))

(check-sat)
(get-model)
