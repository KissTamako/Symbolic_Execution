(set-logic ALL)
; Frontier Constraint ID: 8bc817d25dec4ef5
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1036)) (False)
(assert (not (not (= x 1036))))

(check-sat)
(get-model)
