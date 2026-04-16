(set-logic ALL)
; Constraint ID: b09ea1b9f6902e8d
; Generated at: 2026-04-16 11:43:57
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60289)) (False)
(assert (not (= x 60289)))

; Query: ((== x 60290)) (False)
(assert (not (not (= x 60290))))

(check-sat)
(get-model)
