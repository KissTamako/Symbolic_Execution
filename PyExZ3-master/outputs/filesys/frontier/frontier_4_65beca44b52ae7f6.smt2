(set-logic ALL)
; Frontier Constraint ID: 65beca44b52ae7f6
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1693)) (False)
(assert (not (not (= x 1693))))

(check-sat)
(get-model)
