(set-logic ALL)
; Frontier Constraint ID: cbd9032e341c3056
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 733)) (False)
(assert (not (= x 733)))

; Query: ((== x 734)) (False)
(assert (not (not (= x 734))))

(check-sat)
(get-model)
