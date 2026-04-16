(set-logic ALL)
; Frontier Constraint ID: 43da9bf401dea762
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 523)) (False)
(assert (not (not (= x 523))))

(check-sat)
(get-model)
