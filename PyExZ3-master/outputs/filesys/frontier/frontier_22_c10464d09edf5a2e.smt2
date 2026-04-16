(set-logic ALL)
; Frontier Constraint ID: c10464d09edf5a2e
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1345)) (False)
(assert (not (not (= x 1345))))

(check-sat)
(get-model)
