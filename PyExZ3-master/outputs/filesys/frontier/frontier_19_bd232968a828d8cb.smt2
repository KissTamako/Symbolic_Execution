(set-logic ALL)
; Frontier Constraint ID: bd232968a828d8cb
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2464)) (False)
(assert (not (= x 2464)))

; Query: ((== x 2465)) (False)
(assert (not (not (= x 2465))))

(check-sat)
(get-model)
