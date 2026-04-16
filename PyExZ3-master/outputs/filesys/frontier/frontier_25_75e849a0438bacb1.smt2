(set-logic ALL)
; Frontier Constraint ID: 75e849a0438bacb1
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 448)) (False)
(assert (not (= x 448)))

; Query: ((== x 449)) (False)
(assert (not (not (= x 449))))

(check-sat)
(get-model)
