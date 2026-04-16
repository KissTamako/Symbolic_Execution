(set-logic ALL)
; Constraint ID: 2808d792bd202a54
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60076)) (False)
(assert (not (= x 60076)))

; Query: ((== x 60077)) (False)
(assert (not (not (= x 60077))))

(check-sat)
(get-model)
