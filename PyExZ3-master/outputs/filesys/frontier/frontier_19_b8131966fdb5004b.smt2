(set-logic ALL)
; Constraint ID: b8131966fdb5004b
; Generated at: 2026-04-16 11:43:57
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60313)) (False)
(assert (not (= x 60313)))

; Query: ((== x 60314)) (False)
(assert (not (not (= x 60314))))

(check-sat)
(get-model)
