(set-logic ALL)
; Frontier Constraint ID: b04b0b324bfce6a2
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2473)) (False)
(assert (not (= x 2473)))

; Query: ((== x 2474)) (False)
(assert (not (not (= x 2474))))

(check-sat)
(get-model)
