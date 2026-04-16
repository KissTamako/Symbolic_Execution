(set-logic ALL)
; Constraint ID: 9a27a5b18f31cb25
; Generated at: 2026-04-16 11:42:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60226)) (False)
(assert (not (= x 60226)))

; Query: ((== x 60227)) (False)
(assert (not (not (= x 60227))))

(check-sat)
(get-model)
