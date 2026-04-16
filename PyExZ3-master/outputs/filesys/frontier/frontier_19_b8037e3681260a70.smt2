(set-logic ALL)
; Frontier Constraint ID: b8037e3681260a70
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1864)) (False)
(assert (not (= x 1864)))

; Query: ((== x 1865)) (False)
(assert (not (not (= x 1865))))

(check-sat)
(get-model)
