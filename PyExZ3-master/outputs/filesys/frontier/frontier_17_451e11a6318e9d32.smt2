(set-logic ALL)
; Constraint ID: 451e11a6318e9d32
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60385)) (False)
(assert (not (= x 60385)))

; Query: ((== x 60386)) (False)
(assert (not (not (= x 60386))))

(check-sat)
(get-model)
