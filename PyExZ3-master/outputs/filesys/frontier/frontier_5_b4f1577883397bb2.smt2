(set-logic ALL)
; Frontier Constraint ID: b4f1577883397bb2
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1168)) (False)
(assert (not (= x 1168)))

; Query: ((== x 1169)) (False)
(assert (not (not (= x 1169))))

(check-sat)
(get-model)
