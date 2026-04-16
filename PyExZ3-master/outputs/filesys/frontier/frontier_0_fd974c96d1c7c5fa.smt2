(set-logic ALL)
; Frontier Constraint ID: fd974c96d1c7c5fa
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1612)) (False)
(assert (not (not (= x 1612))))

(check-sat)
(get-model)
