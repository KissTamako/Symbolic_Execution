(set-logic ALL)
; Frontier Constraint ID: 023faa825a71ebfc
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1171)) (False)
(assert (not (not (= x 1171))))

(check-sat)
(get-model)
