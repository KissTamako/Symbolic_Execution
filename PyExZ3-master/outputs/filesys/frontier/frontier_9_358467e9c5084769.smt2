(set-logic ALL)
; Constraint ID: 358467e9c5084769
; Generated at: 2026-04-16 11:42:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60223)) (False)
(assert (not (= x 60223)))

; Query: ((== x 60224)) (False)
(assert (not (not (= x 60224))))

(check-sat)
(get-model)
