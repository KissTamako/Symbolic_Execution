(set-logic ALL)
; Frontier Constraint ID: 8e52298175c5707e
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1045)) (False)
(assert (not (not (= x 1045))))

(check-sat)
(get-model)
