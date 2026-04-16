(set-logic ALL)
; Frontier Constraint ID: f0bd3b93ce8090f7
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1183)) (False)
(assert (not (not (= x 1183))))

(check-sat)
(get-model)
