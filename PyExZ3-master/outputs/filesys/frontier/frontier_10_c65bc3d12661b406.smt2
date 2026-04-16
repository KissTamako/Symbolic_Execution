(set-logic ALL)
; Constraint ID: c65bc3d12661b406
; Generated at: 2026-04-16 04:08:23
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59251)) (False)
(assert (not (not (= x 59251))))

(check-sat)
(get-model)
