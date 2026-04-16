(set-logic ALL)
; Constraint ID: 4e796954eaaf4015
; Generated at: 2026-04-16 11:14:00
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59866)) (False)
(assert (not (not (= x 59866))))

(check-sat)
(get-model)
