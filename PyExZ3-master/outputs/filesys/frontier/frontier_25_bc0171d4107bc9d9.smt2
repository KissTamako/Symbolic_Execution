(set-logic ALL)
; Frontier Constraint ID: bc0171d4107bc9d9
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1648)) (False)
(assert (not (= x 1648)))

; Query: ((== x 1649)) (False)
(assert (not (not (= x 1649))))

(check-sat)
(get-model)
