(set-logic ALL)
; Frontier Constraint ID: 42fe716a36db2613
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 730)) (False)
(assert (not (not (= x 730))))

(check-sat)
(get-model)
