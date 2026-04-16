(set-logic ALL)
; Constraint ID: cf73a5386b1f6aea
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59704)) (False)
(assert (not (= x 59704)))

; Query: ((== x 59705)) (False)
(assert (not (not (= x 59705))))

(check-sat)
(get-model)
