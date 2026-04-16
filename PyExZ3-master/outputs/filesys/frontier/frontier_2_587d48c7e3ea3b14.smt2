(set-logic ALL)
; Constraint ID: 587d48c7e3ea3b14
; Generated at: 2026-04-16 10:43:23
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59464)) (False)
(assert (not (not (= x 59464))))

(check-sat)
(get-model)
