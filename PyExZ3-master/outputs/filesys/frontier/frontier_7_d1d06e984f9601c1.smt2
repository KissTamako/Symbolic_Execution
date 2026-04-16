(set-logic ALL)
; Constraint ID: d1d06e984f9601c1
; Generated at: 2026-04-16 11:28:21
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59920)) (False)
(assert (not (= x 59920)))

; Query: ((== x 59921)) (False)
(assert (not (not (= x 59921))))

(check-sat)
(get-model)
