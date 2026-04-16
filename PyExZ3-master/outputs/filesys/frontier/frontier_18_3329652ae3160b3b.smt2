(set-logic ALL)
; Frontier Constraint ID: 3329652ae3160b3b
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2464)) (False)
(assert (not (not (= x 2464))))

(check-sat)
(get-model)
