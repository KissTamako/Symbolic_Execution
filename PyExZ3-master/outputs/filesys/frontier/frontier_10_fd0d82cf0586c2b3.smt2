(set-logic ALL)
; Frontier Constraint ID: fd0d82cf0586c2b3
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 727)) (False)
(assert (not (not (= x 727))))

(check-sat)
(get-model)
