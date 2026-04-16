(set-logic ALL)
; Frontier Constraint ID: cb4174c8e41235b1
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2521)) (False)
(assert (not (not (= x 2521))))

(check-sat)
(get-model)
