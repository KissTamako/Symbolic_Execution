(set-logic ALL)
; Frontier Constraint ID: a1cdc6830d0d819a
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1474)) (False)
(assert (not (not (= x 1474))))

(check-sat)
(get-model)
