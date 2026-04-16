(set-logic ALL)
; Constraint ID: 61bd1800a7f6ca68
; Generated at: 2026-04-16 10:43:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59461)) (False)
(assert (not (= x 59461)))

; Query: ((== x 59462)) (False)
(assert (not (not (= x 59462))))

(check-sat)
(get-model)
