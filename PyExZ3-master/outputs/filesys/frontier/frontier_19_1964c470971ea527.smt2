(set-logic ALL)
; Constraint ID: 1964c470971ea527
; Generated at: 2026-04-16 12:01:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60688)) (False)
(assert (not (= x 60688)))

; Query: ((== x 60689)) (False)
(assert (not (not (= x 60689))))

(check-sat)
(get-model)
