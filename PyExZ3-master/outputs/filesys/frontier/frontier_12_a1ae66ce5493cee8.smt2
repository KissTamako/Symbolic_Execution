(set-logic ALL)
; Frontier Constraint ID: a1ae66ce5493cee8
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1705)) (False)
(assert (not (not (= x 1705))))

(check-sat)
(get-model)
