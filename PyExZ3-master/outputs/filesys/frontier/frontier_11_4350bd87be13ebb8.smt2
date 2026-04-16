(set-logic ALL)
; Frontier Constraint ID: 4350bd87be13ebb8
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1327)) (False)
(assert (not (= x 1327)))

; Query: ((== x 1328)) (False)
(assert (not (not (= x 1328))))

(check-sat)
(get-model)
