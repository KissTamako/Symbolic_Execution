(set-logic ALL)
; Constraint ID: a4436faf7d1a2ff6
; Generated at: 2026-04-16 11:42:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60229)) (False)
(assert (not (= x 60229)))

; Query: ((== x 60230)) (False)
(assert (not (not (= x 60230))))

(check-sat)
(get-model)
