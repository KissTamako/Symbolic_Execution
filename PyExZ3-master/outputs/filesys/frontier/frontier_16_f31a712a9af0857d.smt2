(set-logic ALL)
; Frontier Constraint ID: f31a712a9af0857d
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 511)) (False)
(assert (not (not (= x 511))))

(check-sat)
(get-model)
