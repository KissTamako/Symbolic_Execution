(set-logic ALL)
; Constraint ID: 2b52e03250ec48b5
; Generated at: 2026-04-16 10:45:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59545)) (False)
(assert (not (= x 59545)))

; Query: ((== x 59546)) (False)
(assert (not (not (= x 59546))))

(check-sat)
(get-model)
