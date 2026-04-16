(set-logic ALL)
; Frontier Constraint ID: 3a263f710e757fb6
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1312)) (False)
(assert (not (not (= x 1312))))

(check-sat)
(get-model)
