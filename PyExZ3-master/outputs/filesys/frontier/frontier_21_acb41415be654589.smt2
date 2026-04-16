(set-logic ALL)
; Constraint ID: acb41415be654589
; Generated at: 2026-04-16 04:08:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59266)) (False)
(assert (not (= x 59266)))

; Query: ((== x 59267)) (False)
(assert (not (not (= x 59267))))

(check-sat)
(get-model)
