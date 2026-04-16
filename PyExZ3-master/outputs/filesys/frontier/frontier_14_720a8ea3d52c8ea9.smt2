(set-logic ALL)
; Constraint ID: 720a8ea3d52c8ea9
; Generated at: 2026-04-16 11:28:21
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59932)) (False)
(assert (not (not (= x 59932))))

(check-sat)
(get-model)
