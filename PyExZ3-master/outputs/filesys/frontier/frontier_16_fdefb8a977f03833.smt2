(set-logic ALL)
; Frontier Constraint ID: fdefb8a977f03833
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 886)) (False)
(assert (not (not (= x 886))))

(check-sat)
(get-model)
