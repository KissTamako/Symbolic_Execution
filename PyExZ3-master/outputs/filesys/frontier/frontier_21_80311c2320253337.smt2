(set-logic ALL)
; Constraint ID: 80311c2320253337
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59641)) (False)
(assert (not (= x 59641)))

; Query: ((== x 59642)) (False)
(assert (not (not (= x 59642))))

(check-sat)
(get-model)
