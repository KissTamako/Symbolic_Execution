(set-logic ALL)
; Constraint ID: 3dac11385442528b
; Generated at: 2026-04-16 11:28:21
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59938)) (False)
(assert (not (not (= x 59938))))

(check-sat)
(get-model)
