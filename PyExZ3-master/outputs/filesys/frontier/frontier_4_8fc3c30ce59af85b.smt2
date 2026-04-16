(set-logic ALL)
; Frontier Constraint ID: 8fc3c30ce59af85b
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1018)) (False)
(assert (not (not (= x 1018))))

(check-sat)
(get-model)
